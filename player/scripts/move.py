"""Print the action for the pending decision as one JSON line: {"seq": N, "action": {...}}.

Reads game/state.json (or the path in argv[1]). In the main phase it plans our whole turn with a small model of
the board (attacks, shields, taunts, our cards' effects), scores where each plan ends and returns the first step of
the best one; the next decision plans again from the real state. Uses only what our seat can see.
Anything the plan proposes that is not in legal_actions is never sent; on any error the course greedy bot decides.
"""

import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECK_PATH = ROOT / "deck.json"

BEAM = 24
MAX_STEPS = 20
FACE_DAMAGE_PER_TURN = {"HUNTER": 2, "MAGE": 1, "DRUID": 1, "ROGUE": 1}

W = {
    "face": 0.5,             # per point of enemy health removed
    "our_hp": 5.0,           # x sqrt(our health): losing health hurts more when low
    "hand_base": 0.0,        # card in hand = hand_base + hand_per_cost * cost
    "hand_per_cost": 0.5,
    "draw": 3.0,             # unknown drawn card
    "enemy_minion": 1.5,     # enemy board counts more than ours (it attacks first)
    "taunt": 1.0,
    "weapon": 0.6,           # x attack x durability
    "dead_next_turn": 60.0,  # their visible damage + reach >= our health
    "danger": 5.0,           # x (their visible damage + reach) / our health
    "reach": 3,              # damage we assume an opponent with cards in hand can add from hand
    "our_clock": 12.0,       # our board alone threatens lethal next turn
    "overload": 1.0,         # per mana locked next turn
    "secret": 3.0,           # a Secret we put up (its trigger is not modelled)
}

# Mulligan per deck (deck.json "name"), from each deck's guide. "always": keep; "with_early": keep if an
# "always" card costing <= 2 is kept; "second": keep going second with an early card; "one_four": keep at most
# one of these (first match), when going second or with an early card.
MULLIGAN = {
    "aggro-paladin": {"always": {"EX1_008", "NEW1_019", "EX1_362", "EX1_096", "EX1_066"},
                      "with_early": {"CS2_087", "EX1_382", "EX1_556", "EX1_019"},
                      "second": {"CS2_097", "CS2_182"}},
    "steady-paladin": {"always": {"EX1_008", "EX1_010", "NEW1_019", "EX1_096", "EX1_066", "EX1_556"},
                       "with_early": {"EX1_362", "EX1_382", "EX1_019", "EX1_590"},
                       "second": {"CS2_097", "CS2_182"}},
    "counter-paladin": {"always": {"EX1_008", "EX1_010", "NEW1_019", "EX1_096", "EX1_066", "EX1_556"},
                        "with_early": {"EX1_362", "EX1_382", "EX1_590", "EX1_363"},
                        "second": {"CS2_097"}},
    "control-paladin": {"always": {"NEW1_020", "EX1_066", "EX1_096", "EX1_382", "EX1_556", "CS2_117"},
                        "with_early": set(), "second": set(),
                        "one_four": ["CS2_097", "CS2_093", "CS2_179"]},
    # The next three follow the KEEP lists of their own pilots (decks/<name>/scripts/move.py).
    "burst-shaman": {"always": {"EX1_008", "EX1_010", "EX1_096", "EX1_238"},
                     "with_early": {"EX1_556", "CS2_117", "EX1_258"}, "second": set()},
    "infernal-warlock": {"always": {"CS2_065", "NEW1_021", "EX1_058", "EX1_066"},
                         "with_early": {"EX1_556", "CS2_117"}, "second": set()},
    "pressure-hunter": {"always": {"EX1_008", "EX1_010", "CS2_120", "EX1_531", "EX1_096"},
                        "with_early": {"EX1_556", "NEW1_031", "EX1_536"}, "second": set()},
}

# Model targets the planner tries for cards that take one (the protocol's own target list is checked before sending).
TARGETS = {
    "EX1_362": "own_unshielded", "EX1_019": "own", "CS2_087": "own", "CS2_092": "own", "EX1_363": "own",
    "EX1_382": "enemy_attacker", "CS2_094": "enemy_or_face", "CS2_117": "heal", "EX1_354": "heal",
    "EX1_561": "heroes",
    "EX1_238": "enemy_or_face", "EX1_241": "enemy_or_face", "DS1_185": "enemy_or_face", "EX1_539": "enemy_or_face",
    "CS2_042": "enemy_or_face", "EX1_245": "enemy", "EX1_246": "enemy", "EX1_302": "enemy", "CS2_203": "enemy",
    "EX1_309": "enemy", "CS2_045": "own_or_me", "EX1_303": "own", "DS1_070": "own_beast",
}
SPELLS_UNTARGETED = {"CS2_093", "EX1_384", "EX1_619", "GAME_005", "EX1_248", "EX1_259", "EX1_317", "CS2_062",
                     "EX1_312", "DS1_184", "EX1_611", "EX1_610", "NEW1_031", "EX1_538"}
SECRETS = {"EX1_611", "EX1_610"}
OVERLOAD = {"EX1_238": 1, "EX1_241": 2, "EX1_259": 2, "EX1_248": 2, "EX1_567": 2}
DAMAGE_SPELLS = {"CS2_094": 3, "EX1_238": 3, "EX1_241": 5, "DS1_185": 2, "EX1_539": 3, "EX1_302": 1}
# Card data has no minion race; these are the Beasts our lists can put on the board.
BEASTS = {"CS2_120", "EX1_531", "CS2_203", "EX1_028", "EX1_534", "EX1_534t", "EX1_538t", "NEW1_032", "NEW1_033",
          "NEW1_034", "DS1_175", "CS2_171", "CS2_172", "CS2_237", "DS1_178", "EX1_543"}
TOKENS = {"skele21": (2, 1), "EX1_110t": (4, 5), "CS2_101t": (1, 1),  # Damaged Golem, Baine, Silver Hand Recruit
          "EX1_534t": (2, 2), "EX1_538t": (1, 1), "EX1_tk11": (2, 3),  # Highmane Hyena, Hound, Spirit Wolf
          "totem": (0, 2), "EX1_tk34": (6, 6), "hexfrog": (0, 1)}        # average basic totem, Infernal, Frog
COMPANIONS = [("NEW1_032", 4, 4, {"taunt": True}), ("NEW1_033", 2, 4, {}), ("NEW1_034", 4, 2, {"left": 1})]
KEYWORDS = {"TAUNT": "taunt", "DIVINE_SHIELD": "ds", "STEALTH": "stealth", "WINDFURY": "wf", "POISONOUS": "poison"}

try:
    from hs_arena import cards as _cards
    CATALOG = _cards.load()
except Exception:  # card data is a convenience; the planner still runs without keywords for new minions
    CATALOG = {}


# ------------------------------------------------------------------------------------------- state model

def _minion(m, own):
    attacks = 0
    if own and m.get("can_attack") and not m.get("frozen"):
        attacks = 2 if m.get("windfury") else 1
    return {"id": m["entity_id"], "cid": m.get("card_id"), "atk": m["attack"], "hp": m["health"],
            "max": m.get("max_health", m["health"]), "taunt": m.get("taunt", False),
            "ds": m.get("divine_shield", False), "stealth": m.get("stealth", False),
            "wf": m.get("windfury", False), "poison": m.get("poisonous", False), "left": attacks,
            "sd": m.get("spell_damage", 0), "silenced": m.get("silenced", False)}


def load(state):
    you, opp = state["you"], state["opponent"]
    weapon = you.get("weapon")
    hero = you["hero"]
    power = you["hero_power"]
    return {
        "mana": you["mana"], "hp": hero["health"] + hero["armor"], "max_hp": hero["max_health"],
        "armor": hero["armor"], "opp_hp": opp["hero"]["health"] + opp["hero"]["armor"],
        "opp_armor": opp["hero"]["armor"], "opp_immune": opp["hero"].get("immune", False),
        "own": [_minion(m, True) for m in you["board"]],
        "enemy": [_minion(m, False) for m in opp["board"]],
        "hand": [{"id": c["entity_id"], "cid": c["card_id"], "cost": c["cost"], "type": c["type"],
                  "atk": c.get("attack", 0), "hp": c.get("health", 0), "dur": c.get("durability", 2)}
                 for c in you["hand"]],
        "weapon": ({"atk": weapon["attack"], "dur": weapon["durability"], "cid": weapon["card_id"],
                    "wf": weapon["card_id"] == "EX1_567"} if weapon else None),
        "hero_left": 0 if hero.get("frozen") or (weapon and not hero.get("can_attack")) else 1,
        "hero_bonus": max(0, hero.get("attack", 0) - (weapon["attack"] if weapon else 0)),
        "hp_ready": bool(power.get("usable")), "hp_cost": power.get("cost", 2),
        "hp_kind": _power_kind(power.get("name", ""), hero.get("hero_class")),
        "opp_weapon": (opp.get("weapon") or {}).get("attack", 0),
        "opp_class": opp["hero"].get("hero_class"), "opp_hand": opp.get("hand_size", 0),
        "demons": sum(n for cid, n in (you.get("deck_remaining_counts") or {}).items() if cid in ("CS2_065", "EX1_323")),
        "draws": 0, "next_id": -1, "overload": 0, "secrets": 0,
    }


def _power_kind(name, hero_class):
    name = name.lower()
    for key, kind in (("reinforce", "recruit"), ("life tap", "tap"), ("steady shot", "shot"),
                      ("totemic", "totem"), ("inferno", "infernal")):
        if key in name:
            return kind
    return {"PALADIN": "recruit", "WARLOCK": "tap", "HUNTER": "shot", "SHAMAN": "totem"}.get(hero_class)


def clone(s):
    c = dict(s)
    c["own"] = [dict(m) for m in s["own"]]
    c["enemy"] = [dict(m) for m in s["enemy"]]
    c["hand"] = list(s["hand"])
    if s["weapon"]:
        c["weapon"] = dict(s["weapon"])
    return c


def cost(s, c):
    """Current cost, re-derived for cards whose cost changes during our turn."""
    if c["cid"] == "EX1_586":  # Sea Giant: 1 less per other minion on the battlefield
        return max(0, 10 - len(s["own"]) - len(s["enemy"]))
    if c["cid"] == "NEW1_022":  # Dread Corsair: 1 less per attack of our weapon
        return max(0, 4 - (s["weapon"]["atk"] if s["weapon"] else 0))
    return c["cost"]


def _spell_damage(s):
    return sum(m["sd"] for m in s["own"])


# ------------------------------------------------------------------------------------------- simulation

def _hit(m, dmg):
    if dmg <= 0:
        return
    if m["ds"]:
        m["ds"] = False
    else:
        m["hp"] -= dmg


def _heal(s, target, n):
    if target == "me":
        s["hp"] = min(s["hp"] + n, s["max_hp"] + s["armor"])
    elif target is not None:
        target["hp"] = min(target["hp"] + n, target["max"])


def _damage(s, target, t, dmg):
    """Damage to the enemy hero ("hero"), our hero ("me") or a minion."""
    if target == "hero":
        s["opp_hp"] -= dmg
    elif target == "me":
        s["hp"] -= dmg
    elif t is not None:
        _hit(t, dmg)


def _silence(m):
    base = CATALOG.get(m["cid"], {})
    m.update(taunt=False, ds=False, stealth=False, wf=False, poison=False, sd=0, silenced=True)
    if base.get("attack") is not None:
        m["atk"] = min(m["atk"], base["attack"])
        m["max"] = min(m["max"], base["health"])
        m["hp"] = min(m["hp"], m["max"])


def _cleanup(s, rng):
    """Remove the dead; run our deathrattles, Cult Master and Scavenging Hyena."""
    dead_own = [m for m in s["own"] if m["hp"] <= 0]
    s["enemy"] = [m for m in s["enemy"] if m["hp"] > 0]
    if not dead_own:
        return
    s["own"] = [m for m in s["own"] if m["hp"] > 0]
    if any(m["cid"] == "EX1_595" for m in s["own"]):
        s["draws"] += len(dead_own)
    beasts = sum(m["cid"] in BEASTS for m in dead_own)
    for h in s["own"]:
        if h["cid"] == "EX1_531" and not h["silenced"]:
            h["atk"] += 2 * beasts
            h["hp"] += beasts
            h["max"] += beasts
    for m in dead_own:
        if m["silenced"]:
            continue
        if m["cid"] in ("EX1_096", "EX1_012"):
            s["draws"] += 1
        elif m["cid"] == "EX1_383":
            s["weapon"] = {"atk": 5, "dur": 3, "cid": "EX1_383t", "wf": False}
        elif m["cid"] in ("EX1_556", "EX1_110"):
            if len(s["own"]) < 7:
                _summon(s, rng, _token(s, "skele21" if m["cid"] == "EX1_556" else "EX1_110t"))
        elif m["cid"] == "EX1_534":
            for _ in range(2):
                if len(s["own"]) < 7:
                    _summon(s, rng, _token(s, "EX1_534t"))


def _token(s, cid, **kw):
    atk, hp = TOKENS[cid]
    return _new(s, cid, atk, hp, **kw)


def _new(s, cid, atk, hp, **kw):
    s["next_id"] -= 1
    m = {"id": s["next_id"], "cid": cid, "atk": atk, "hp": hp, "max": hp, "taunt": False, "ds": False,
         "stealth": False, "wf": False, "poison": False, "left": 0, "sd": 0, "silenced": False}
    m.update(kw)
    return m


def _summon(s, rng, m):
    """Put a minion on our board; Knife Jugglers (other than it) each hit a random enemy character."""
    s["own"].append(m)
    for j in s["own"]:
        if j["cid"] == "NEW1_019" and j is not m and not j["silenced"]:
            t = rng.choice([e for e in s["enemy"] if e["hp"] > 0] + ["hero"])
            if t == "hero":
                s["opp_hp"] -= 1
            else:
                _hit(t, 1)
    _cleanup(s, rng)


def _find(s, eid):
    for side in ("own", "enemy"):
        for m in s[side]:
            if m["id"] == eid:
                return side, m
    return None, None


def _targets(s, kind, enemies):
    if kind == "own":
        return [m["id"] for m in s["own"]]
    if kind == "own_unshielded":
        return [m["id"] for m in s["own"] if not m["ds"]]
    if kind == "own_beast":
        return [m["id"] for m in s["own"] if m["cid"] in BEASTS]
    if kind == "own_or_me":
        return [m["id"] for m in s["own"] if m["left"] > 0] + ["me"]
    if kind == "enemy":
        return [m["id"] for m in enemies]
    if kind == "enemy_attacker":
        return [m["id"] for m in enemies if m["atk"] > 1] or [m["id"] for m in enemies][:1]
    if kind == "enemy_or_face":
        return [m["id"] for m in enemies] + ["hero"]
    if kind == "heal":
        hurt = [m for m in s["own"] if m["hp"] < m["max"]]
        return ["me"] + ([max(hurt, key=lambda m: m["max"] - m["hp"])["id"]] if hurt else [])
    if kind == "heroes":
        return ["hero", "me"]
    return []


def _hero_attack(s):
    return (s["weapon"]["atk"] if s["weapon"] else 0) + s["hero_bonus"]


def gen(s):
    """Candidate actions in the model: ("play", card, target) / ("attack", attacker, target) / ("power",)."""
    acts = []
    enemies = [m for m in s["enemy"] if not m["stealth"]]
    taunts = [m for m in enemies if m["taunt"]]
    attack_targets = [m["id"] for m in (taunts or enemies)] + ([] if taunts or s["opp_immune"] else ["hero"])
    for m in s["own"]:
        if m["left"] > 0 and m["atk"] > 0:
            acts += [("attack", m["id"], t) for t in attack_targets]
    if s["hero_left"] > 0 and _hero_attack(s) > 0:
        acts += [("attack", "me", t) for t in attack_targets]
    room = len(s["own"]) < 7
    seen = set()
    for c in s["hand"]:
        if cost(s, c) > s["mana"] or c["cid"] in seen:
            continue
        seen.add(c["cid"])  # identical copies give identical plans
        cid = c["cid"]
        if c["type"] == "MINION" and not room and cid != "EX1_323":
            continue
        tg = _targets(s, TARGETS.get(cid), enemies)
        if tg:
            acts += [("play", c["id"], t) for t in tg]
        elif c["type"] in ("MINION", "WEAPON") or cid in SPELLS_UNTARGETED:
            if cid != "GAME_005" or any(cost(s, o) == s["mana"] + 1 for o in s["hand"]):
                acts.append(("play", c["id"], None))
    if s["hp_ready"] and s["mana"] >= s["hp_cost"] and (room or s["hp_kind"] not in ("recruit", "totem", "infernal")):
        acts.append(("power",))
    return acts


def _battlecry(s, rng, cid, t, target, kw, c):
    if cid == "EX1_362" and t:
        t["ds"] = True
    elif cid == "EX1_019" and t:
        t["atk"] += 1
        t["hp"] += 1
        t["max"] += 1
    elif cid == "EX1_382" and t:
        t["atk"] = 1
    elif cid == "EX1_066":
        s["opp_weapon"] = 0
    elif cid == "EX1_590":
        shields = sum(m["ds"] for m in s["own"] + s["enemy"])
        for m in s["own"] + s["enemy"]:
            m["ds"] = False
        kw["atk"], kw["hp"] = c["atk"] + 3 * shields, c["hp"] + 3 * shields
    elif cid == "CS2_117":
        _heal(s, "me" if target == "me" else t, 3)
    elif cid == "DS1_055":
        _heal(s, "me", 2)
        for m in s["own"]:
            _heal(s, m, 2)
    elif cid == "CS2_088":
        _heal(s, "me", 6)
    elif cid == "NEW1_041":
        small = [m for m in s["enemy"] if m["atk"] <= 2]
        if small:
            rng.choice(small)["hp"] = 0
    elif cid == "EX1_561":
        if target == "hero":
            s["opp_hp"] = 15 + s["opp_armor"]
        elif target == "me":
            s["hp"] = 15 + s["armor"]
    elif cid == "CS2_042":
        _damage(s, target, t, 3)
    elif cid == "CS2_203" and t:
        _silence(t)
    elif cid == "DS1_070" and t:
        t["atk"] += 2
        t["hp"] += 2
        t["max"] += 2
        t["taunt"] = True
    elif cid in ("EX1_058", "EX1_093") and s["own"]:  # we play at the right end: one neighbour
        n = s["own"][-1]
        n["taunt"] = True
        if cid == "EX1_093":
            n["atk"] += 1
            n["hp"] += 1
            n["max"] += 1
    elif cid == "EX1_043":
        kw["hp"] = c["hp"] + len(s["hand"])
    elif cid == "EX1_012":
        kw["sd"] = 1


def _spell(s, rng, cid, t, target):
    sd = _spell_damage(s)
    if cid in DAMAGE_SPELLS:
        dmg = DAMAGE_SPELLS[cid] + sd
        if cid == "EX1_539" and any(m["cid"] in BEASTS for m in s["own"]):
            dmg += 2
        if cid == "EX1_302" and t and not t["ds"] and t["hp"] <= dmg:
            s["draws"] += 1
        _damage(s, target, t, dmg)
        if cid == "CS2_094":
            s["draws"] += 1
    elif cid == "CS2_087" and t:
        t["atk"] += 3
    elif cid == "CS2_092" and t:
        t["atk"] += 4
        t["hp"] += 4
        t["max"] += 4
    elif cid == "EX1_363" and t:
        t["wis"] = True
    elif cid == "CS2_093":
        for m in s["enemy"]:
            _hit(m, 2 + sd)
        s["opp_hp"] -= 2 + sd
    elif cid == "EX1_384":
        for _ in range(8):
            x = rng.choice([m for m in s["enemy"] if m["hp"] > 0] + ["hero"])
            if x == "hero":
                s["opp_hp"] -= 1
            else:
                _hit(x, 1)
    elif cid == "EX1_619":
        for m in s["own"] + s["enemy"]:
            m["hp"] = m["max"] = 1
    elif cid == "EX1_354":
        _heal(s, "me" if target == "me" else t, 8)
        s["draws"] += 3
    elif cid == "GAME_005":
        s["mana"] += 1
    elif cid == "CS2_045":  # Rockbiter: +3 attack this turn
        if target == "me":
            s["hero_bonus"] += 3
        elif t:
            t["atk"] += 3
            t["tmp"] = t.get("tmp", 0) + 3
    elif cid == "EX1_245" and t:
        _silence(t)
        _hit(t, 1 + sd)
    elif cid == "EX1_246" and t:
        t.update(cid="hexfrog", atk=0, hp=1, max=1, taunt=True, ds=False, stealth=False, wf=False, poison=False,
                 sd=0, silenced=True)
    elif cid == "EX1_248":
        for _ in range(2):
            if len(s["own"]) < 7:
                _summon(s, rng, _token(s, "EX1_tk11", taunt=True))
    elif cid == "EX1_259":
        for m in s["enemy"]:
            _hit(m, rng.choice((2, 3)) + sd)
    elif cid == "EX1_317":
        s["draws"] += 2 if s["demons"] else 0
        for _ in range(2 - min(2, s["demons"])):  # no demon left: a 1/1 Worthless Imp is drawn instead
            s["draws"] += 0.3
    elif cid == "CS2_062":
        for m in s["own"] + s["enemy"]:
            _hit(m, 3 + sd)
        s["hp"] -= 3 + sd
        s["opp_hp"] -= 3 + sd
    elif cid == "EX1_303" and t:
        dmg = t["atk"]
        t["hp"] = 0
        for m in s["enemy"]:
            _hit(m, dmg)
    elif cid == "EX1_309" and t:
        t["hp"] = 0
        _heal(s, "me", 3)
    elif cid == "EX1_312":
        for m in s["own"] + s["enemy"]:
            m["hp"] = 0
    elif cid == "DS1_184":
        s["draws"] += 1
    elif cid in SECRETS:
        s["secrets"] += 1
    elif cid == "NEW1_031":
        if len(s["own"]) < 7:
            pick, atk, hp, kw = rng.choice(COMPANIONS)
            _summon(s, rng, _new(s, pick, atk, hp, **kw))
    elif cid == "EX1_538":
        for _ in range(min(len(s["enemy"]), 7 - len(s["own"]))):
            _summon(s, rng, _token(s, "EX1_538t", left=1))
    _cleanup(s, rng)
    for _ in [m for m in s["own"] if m["cid"] == "NEW1_020" and not m["silenced"]]:  # Pyromancer: 1 to ALL minions
        for m in s["own"] + s["enemy"]:
            _hit(m, 1)
        _cleanup(s, rng)


def _power(s, rng):
    s["mana"] -= s["hp_cost"]
    s["hp_ready"] = False
    kind = s["hp_kind"]
    if kind == "recruit":
        _summon(s, rng, _token(s, "CS2_101t"))
    elif kind == "totem":
        _summon(s, rng, _token(s, "totem"))
    elif kind == "infernal":
        _summon(s, rng, _token(s, "EX1_tk34"))
    elif kind == "tap":
        s["hp"] -= 2
        s["draws"] += 1
    elif kind == "shot":
        s["opp_hp"] -= 2


def apply(s, act, rng):
    s = clone(s)
    kind = act[0]
    if kind == "power":
        _power(s, rng)
        return s
    if kind == "attack":
        _, a_id, t_id = act
        t = None if t_id == "hero" else _find(s, t_id)[1]
        t_atk = 0 if t is None else t["atk"]
        if a_id == "me":
            w = s["weapon"]
            if w and w["cid"] == "CS2_097":
                _heal(s, "me", 2)
            atk = _hero_attack(s)
            if t is None:
                s["opp_hp"] -= atk
            else:
                _hit(t, atk)
                s["hp"] -= t_atk
            s["hero_left"] -= 1
            if w:
                w["dur"] -= 1
                if w["dur"] <= 0:
                    s["weapon"] = None
        else:
            a = _find(s, a_id)[1]
            a["left"] -= 1
            a["stealth"] = False
            if a.get("wis"):
                s["draws"] += 1
            if t is None:
                s["opp_hp"] -= a["atk"]
            else:
                _hit(t, a["atk"])
                if a["poison"] and t["hp"] < t["max"]:
                    t["hp"] = 0
                _hit(a, t_atk)
                if t["poison"] and t_atk > 0 and a["hp"] < a["max"]:
                    a["hp"] = 0
        _cleanup(s, rng)
        return s
    _, card_id, target = act
    c = next(x for x in s["hand"] if x["id"] == card_id)
    s["hand"] = [x for x in s["hand"] if x["id"] != card_id]
    s["mana"] -= cost(s, c)
    cid = c["cid"]
    if cid in OVERLOAD:
        s["overload"] += OVERLOAD[cid]
        for m in s["own"]:
            if m["cid"] == "EX1_258" and not m["silenced"]:  # Unbound Elemental
                m["atk"] += 1
                m["hp"] += 1
                m["max"] += 1
    t = None if target in (None, "hero", "me") else _find(s, target)[1]
    if cid == "EX1_323":  # Lord Jaraxxus replaces our hero: 15 health, a 3/8 weapon, Infernal hero power
        s.update(hp=15, max_hp=15, armor=0, hp_kind="infernal", hp_ready=True)
        s["weapon"] = {"atk": 3, "dur": 8, "cid": "EX1_323w", "wf": False}
        return s
    if c["type"] == "MINION":
        mech = CATALOG.get(cid, {}).get("mechanics", [])
        kw = {v: True for k, v in KEYWORDS.items() if k in mech}
        if "CHARGE" in mech:
            kw["left"] = 2 if "WINDFURY" in mech else 1
        _battlecry(s, rng, cid, t, target, kw, c)
        m = _new(s, cid, kw.pop("atk", c["atk"]), kw.pop("hp", c["hp"]), **kw)
        m["id"] = c["id"]  # the card keeps its entity id on the board
        _summon(s, rng, m)
        return s
    if c["type"] == "WEAPON":
        s["weapon"] = {"atk": c["atk"], "dur": c["dur"], "cid": cid, "wf": cid == "EX1_567"}
        if cid == "EX1_567" and s["hero_left"] == 1:
            s["hero_left"] = 2
        return s
    _spell(s, rng, cid, t, target)
    return s


# ------------------------------------------------------------------------------------------- evaluation

def mval(m):
    atk = m["atk"] - m.get("tmp", 0)
    v = atk + m["hp"] if atk > 0 else 0.5 * m["hp"]
    if m["taunt"]:
        v += W["taunt"]
    if m["ds"]:
        v += 1 + 0.5 * atk
    if m["wf"]:
        v += 0.5 * atk
    if m["poison"]:
        v += 2
    if m.get("wis"):
        v += 1.5
    return v


def evaluate(s):
    if s["opp_hp"] <= 0:
        return 1e6 + s["hp"]
    if s["hp"] <= 0:
        return -1e6
    v = W["face"] * (30 - s["opp_hp"]) + W["our_hp"] * math.sqrt(max(s["hp"], 0))
    doom = any(m["cid"] == "NEW1_021" and not m["silenced"] for m in s["own"])
    if doom:  # Doomsayer clears both boards at the start of our next turn (unless they kill it first)
        v -= 0.3 * sum(mval(m) for m in s["enemy"])
    else:
        v += sum(mval(m) for m in s["own"]) - W["enemy_minion"] * sum(mval(m) for m in s["enemy"])
    v += sum(W["hand_base"] + W["hand_per_cost"] * c["cost"] for c in s["hand"]) + W["draw"] * s["draws"]
    v += W["draw"] * sum(m["cid"] == "EX1_575" and not m["silenced"] for m in s["own"])  # Mana Tide draws at end
    v += W["secret"] * s["secrets"] - W["overload"] * s["overload"]
    if s["weapon"]:
        v += W["weapon"] * s["weapon"]["atk"] * s["weapon"]["dur"]
    # their next turn: every enemy minion attacks; our taunts soak some of it
    their = sum(m["atk"] * (2 if m["wf"] else 1) for m in s["enemy"]) + s["opp_weapon"]
    their += FACE_DAMAGE_PER_TURN.get(s["opp_class"], 0)
    their -= sum(m["hp"] + (m["atk"] if m["ds"] else 0) for m in s["own"] if m["taunt"])
    reach = W["reach"] if s["opp_hand"] else 0
    if max(their, 0) + reach >= s["hp"]:
        v -= W["dead_next_turn"]
    v -= W["danger"] * (max(their, 0) + reach) / max(s["hp"], 1)  # graded: how close their next turn gets
    # our next turn: does our board alone threaten lethal?
    if not doom:
        ours = sum((m["atk"] - m.get("tmp", 0)) * (2 if m["wf"] else 1) for m in s["own"])
        ours += s["weapon"]["atk"] * (2 if s["weapon"]["wf"] else 1) if s["weapon"] else 0
        ours -= sum(m["hp"] for m in s["enemy"] if m["taunt"])
        if ours >= s["opp_hp"]:
            v += W["our_clock"]
    return v


def _key(s):
    return (s["mana"], s["hp"], s["opp_hp"], s["hp_ready"], s["hero_left"], s["hero_bonus"], s["draws"],
            s["overload"], s["secrets"],
            tuple(sorted((m["atk"], m["hp"], m["ds"], m["left"], m["taunt"]) for m in s["own"])),
            tuple(sorted((m["id"], m["atk"], m["hp"], m["ds"], m["taunt"]) for m in s["enemy"])),
            tuple(c["id"] for c in s["hand"]), tuple(s["weapon"].values()) if s["weapon"] else None)


def plan(state):
    """Beam search over our turn. Returns [(score, first_action)] best first, end_turn included."""
    rng = random.Random(state["seq"])
    root = load(state)
    best = {("end",): evaluate(root)}
    frontier = [(root, None)]
    for _ in range(MAX_STEPS):
        children, seen = [], set()
        for s, first in frontier:
            for act in gen(s):
                child = apply(s, act, rng)
                k = _key(child)
                if k in seen:
                    continue
                seen.add(k)
                f = first or act
                v = evaluate(child)
                if v > best.get(f, -math.inf):
                    best[f] = v
                children.append((v, child, f))
        if not children:
            break
        children.sort(key=lambda x: -x[0])
        frontier = [(c, f) for _, c, f in children[:BEAM]]
    return sorted(((v, f) for f, v in best.items()), key=lambda x: -x[0])


# ------------------------------------------------------------------------------------------- decisions

def to_action(state, act):
    """Turn a model action into a protocol action, or None if legal_actions does not allow it."""
    legal = state["legal_actions"]
    me, eh = state["you"]["hero"]["entity_id"], state["opponent"]["hero"]["entity_id"]
    ids = {"hero": eh, "me": me}
    if act[0] == "end":
        return {"type": "end_turn"}
    if act[0] == "power":
        t = next((t for t in legal if t["type"] == "hero_power"), None)
        return {"type": "hero_power"} if t and not t.get("targets") else None
    if act[0] == "attack":
        att, tgt = ids.get(act[1], act[1]), ids.get(act[2], act[2])
        ok = any(t["type"] == "attack" and t["attacker"] == att and tgt in t["targets"] for t in legal)
        return {"type": "attack", "attacker": att, "target": tgt} if ok else None
    _, card, target = act
    target = ids.get(target, target)
    t = next((t for t in legal if t["type"] == "play_card" and t["card"] == card), None)
    if t is None or t.get("choose"):
        return None
    if t.get("targets"):
        if target not in t["targets"]:
            return None
        return {"type": "play_card", "card": card, "target": target}
    return {"type": "play_card", "card": card}


def mulligan(state, deck_name):
    rule = MULLIGAN.get(deck_name, MULLIGAN["aggro-paladin"])
    t = next(t for t in state["legal_actions"] if t["type"] == "mulligan")
    hand = {c["entity_id"]: c for c in state["you"]["hand"]}
    cards = [hand[e] for e in t["options"] if e in hand]
    second = len(t["options"]) >= 4
    early = any(c["card_id"] in rule["always"] and c["cost"] <= 2 for c in cards)
    kept_four = False
    replace = []
    for c in cards:
        cid = c["card_id"]
        keep = cid in rule["always"] or (early and cid in rule["with_early"])
        keep = keep or (second and early and cid in rule["second"])
        if not keep and not kept_four and cid in rule.get("one_four", []) and (second or early):
            # first match in priority order among the hand's candidates
            best = min((x for x in cards if x["card_id"] in rule["one_four"]),
                       key=lambda x: rule["one_four"].index(x["card_id"]))
            keep = kept_four = best is c
        if not keep:
            replace.append(c["entity_id"])
    return {"type": "mulligan", "replace": replace}


def _deck():
    return json.loads(DECK_PATH.read_text(encoding="utf-8"))


def greedy(state):
    from hs_arena.agents.greedy_bot import GreedyBot
    from hs_arena.deck import load_deck
    return GreedyBot("fallback", load_deck(str(DECK_PATH))).decide(state).action


def decide(state):
    phase = state["phase"]
    if phase == "deck_submission":
        deck = _deck()
        return {"type": "submit_deck", "hero_class": deck["hero_class"], "cards": deck["cards"]}
    try:
        if phase == "mulligan":
            return mulligan(state, _deck().get("name"))
        if phase == "main":
            for _, act in plan(state):
                action = to_action(state, act)
                if action:
                    return action
    except Exception as e:  # never lose a decision to a bug in the planner
        print(f"planner error: {e!r}", file=sys.stderr)
    return greedy(state)


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("game/state.json")
    state = json.loads(path.read_text(encoding="utf-8"))
    if state["phase"] == "game_over":
        print(json.dumps({"seq": state["seq"], "game_over": True, "result": state["result"]}))
        return
    W.update(_deck().get("weights", {}))  # this deck's tuned weights (tools/selfplay.py)
    print(json.dumps({"seq": state["seq"], "action": decide(state)}))


if __name__ == "__main__":
    main()
