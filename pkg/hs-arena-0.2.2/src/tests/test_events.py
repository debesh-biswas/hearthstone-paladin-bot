"""Event stream details: divine_shield_lost, for a shield popped by a hit and for one removed by Silence."""

from hs_arena._fp import init_engine
from hs_arena.deck import Deck
from hs_arena.engine import Engine
from hs_arena.sdk.text import event_text

SQUIRE = "EX1_008"  # Argent Squire: 1 mana 1/1 Divine Shield
OWL = "CS2_203"  # Ironbeak Owl: 3 mana, Battlecry: Silence a minion


def _shielded_enemies(view):
    return [m["entity_id"] for m in view["opponent"]["board"] if m["divine_shield"]]


def _policy(engine, i, phase):
    """Paladin: play Argent Squires. Mage: Ironbeak Owl, then Fireblast, on shielded enemy minions."""
    if phase == "mulligan":
        return {"type": "mulligan", "replace": []}
    view = engine.view(i)
    legal = engine.legal_actions(i)
    shielded = _shielded_enemies(view)
    for t in legal:
        card = next((c for c in view["you"]["hand"] if c["entity_id"] == t.get("card")), None)
        if t["type"] == "play_card" and card and card["card_id"] == SQUIRE:
            return {"type": "play_card", "card": t["card"]}
        if t["type"] == "play_card" and card and card["card_id"] == OWL and shielded:
            return {"type": "play_card", "card": t["card"], "target": shielded[0]}
    for t in legal:
        if t["type"] == "hero_power" and shielded and t.get("targets"):
            return {"type": "hero_power", "target": shielded[-1]}
    return {"type": "end_turn"}


def test_divine_shield_lost_is_reported_for_hits_and_silence():
    init_engine()
    engine = Engine(Deck("PALADIN", (SQUIRE,) * 30), Deck("MAGE", (OWL,) * 30), seed=11, max_turns=16)
    engine.take_public_events()
    lost = {"hit": 0, "silence": 0}
    while not engine.over:
        i, phase = engine.pending()
        before = {m["entity_id"]: m["divine_shield"] for p in (1, 2) for m in engine.view(p)["you"]["board"]}
        action = _policy(engine, i, phase)
        assert engine.step(i, action).accepted
        events = engine.take_public_events()
        after = {m["entity_id"]: m["divine_shield"] for p in (1, 2) for m in engine.view(p)["you"]["board"]}
        reported = [e["entity_id"] for e in events if e["event"] == "divine_shield_lost"]
        # every shield that disappeared from a minion still on the board is reported exactly once
        gone = sorted(eid for eid, had in before.items() if had and after.get(eid) is False)
        assert sorted(reported) == gone, (action, events)
        if gone and action["type"] == "hero_power":
            lost["hit"] += 1
            # the absorbed hit dealt no damage, so the shield event is the only trace of it
            assert not [e for e in events if e["event"] == "damage" and e["entity_id"] in gone]
        elif gone and action["type"] == "play_card":
            lost["silence"] += 1
        for e in events:
            if e["event"] == "divine_shield_lost":
                assert event_text(e, lambda p: f"P{p}") == f"Argent Squire #{e['entity_id']} (P{e['player']}) loses Divine Shield."
    assert lost["hit"] >= 1 and lost["silence"] >= 1, lost


SHIELD_BLOCK = "EX1_606"  # 3 mana: gain 5 armor, draw a card
FIREBALL = "CS2_029"  # 4 mana: deal 6 damage


def _armor_policy(engine, i, phase):
    """Warrior: Shield Block and Armor Up!. Mage: Fireball and Fireblast at the enemy hero."""
    if phase == "mulligan":
        return {"type": "mulligan", "replace": []}
    view = engine.view(i)
    enemy = view["opponent"]["hero"]["entity_id"]
    for t in engine.legal_actions(i):
        if t["type"] == "play_card":
            return {"type": "play_card", "card": t["card"], "target": enemy if t.get("targets") else None}
        if t["type"] == "hero_power":
            return {"type": "hero_power", "target": enemy if t.get("targets") else None}
    return {"type": "end_turn"}


def test_armor_is_reported_in_damage_and_armor_gained_events():
    init_engine()
    engine = Engine(Deck("WARRIOR", (SHIELD_BLOCK,) * 30), Deck("MAGE", (FIREBALL,) * 30), seed=5, max_turns=30)
    engine.take_public_events()
    seen = {"gained": 0, "full": 0, "partial": 0, "none": 0}
    while not engine.over:
        i, phase = engine.pending()
        heroes = {engine.view(p)["you"]["hero"]["entity_id"]: engine.view(p)["you"]["hero"] for p in (1, 2)}
        track = {eid: [h["health"], h["armor"]] for eid, h in heroes.items()}
        if phase == "main":  # only the player on turn has spendable mana
            assert engine.view(i)["opponent"]["mana"] == 0
            assert engine.view(3 - i)["you"]["mana"] == 0
        assert engine.step(i, _armor_policy(engine, i, phase)).accepted
        for e in engine.take_public_events():
            if e.get("entity_id") not in track:
                continue
            health, armor = track[e["entity_id"]]
            if e["event"] == "damage":
                absorbed = e["armor_absorbed"]
                assert e["armor_after"] == armor - absorbed and e["health_after"] == health - (e["amount"] - absorbed), e
                seen["full" if absorbed == e["amount"] else "partial" if absorbed else "none"] += 1
                line = event_text(e, lambda p: f"P{p}")
                assert (f"({absorbed} absorbed by armor)" in line) == bool(absorbed), line
                if absorbed:
                    assert line.endswith(f", health {e['health_after']}, armor {e['armor_after']}."), line
                track[e["entity_id"]] = [e["health_after"], e["armor_after"]]
            elif e["event"] == "armor_gained":
                assert e["armor_after"] == armor + e["amount"], e
                assert event_text(e, lambda p: f"P{p}").endswith(f"gains {e['amount']} armor from {e['source']['name']} "
                                                                 f"#{e['source']['entity_id']}, armor {e['armor_after']}.")
                seen["gained"] += 1
                track[e["entity_id"]][1] = e["armor_after"]
            elif e["event"] == "heal":
                track[e["entity_id"]][0] = e["health_after"]
        if not engine.over:  # the events alone reproduce every hero's health and armor
            for p in (1, 2):
                h = engine.view(p)["you"]["hero"]
                assert track[h["entity_id"]] == [h["health"], h["armor"]], (h, track)
    assert seen["gained"] and seen["full"] and seen["partial"], seen


YETI = "CS2_182"  # Chillwind Yeti: 4 mana 4/5, no Charge
SHADOWSTEP = "EX1_144"  # 0 mana: return a friendly minion to your hand; it costs (2) less


def test_minion_returned_to_hand_has_summoning_sickness_when_replayed():
    """Regression (vendored fireplace patch 4): an awake minion returned to hand and played again must not attack."""
    init_engine()
    engine = Engine(Deck("ROGUE", (YETI, SHADOWSTEP) * 15), Deck("WARRIOR", (YETI,) * 30), seed=5, max_turns=30)
    bounced, replayed = None, False
    while not engine.over and not replayed:
        i, phase = engine.pending()
        if phase == "mulligan":
            engine.step(i, {"type": "mulligan", "replace": []})
            continue
        view, legal = engine.view(i), engine.legal_actions(i)
        hand = {c["entity_id"]: c["card_id"] for c in view["you"]["hand"]}
        awake = [m["entity_id"] for m in view["you"]["board"] if m["can_attack"]]
        plays = {t["card"]: t for t in legal if t["type"] == "play_card"}
        action = {"type": "end_turn"}
        if i == 1 and bounced in plays:
            action = {"type": "play_card", "card": bounced}
        elif i == 1 and awake and bounced is None:
            step = next((t for c, t in plays.items() if hand[c] == SHADOWSTEP and awake[0] in t["targets"]), None)
            if step:
                bounced = awake[0]
                action = {"type": "play_card", "card": step["card"], "target": bounced}
        elif i == 1:
            yeti = next((c for c in plays if hand[c] == YETI), None)
            if yeti is not None:
                action = {"type": "play_card", "card": yeti}
        assert engine.step(i, action).accepted, action
        if action["type"] == "play_card" and action["card"] == bounced and "target" not in action:
            replayed = True
            minion = next(m for m in engine.view(1)["you"]["board"] if m["entity_id"] == bounced)
            assert not minion["can_attack"]
            assert bounced not in [t["attacker"] for t in engine.legal_actions(1) if t["type"] == "attack"]
    assert replayed, "the scenario never happened; adjust the seed"
