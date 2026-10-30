"""Self-check of the planner's card model: python tools/test_move.py (silent on success)."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "player" / "scripts"))
import move  # noqa: E402

RNG = random.Random(0)


def minion(eid, cid, atk, hp, **kw):
    return {"id": eid, "cid": cid, "atk": atk, "hp": hp, "max": hp, "taunt": False, "ds": False, "stealth": False,
            "wf": False, "poison": False, "left": 1, "sd": 0, "silenced": False, **kw}


def card(eid, cid, ctype, cost, atk=0, hp=0):
    return {"id": eid, "cid": cid, "cost": cost, "type": ctype, "atk": atk, "hp": hp, "dur": 2}


def state(own=(), enemy=(), hand=(), mana=10, hp=20):
    return {"mana": mana, "hp": hp, "max_hp": 30, "armor": 0, "opp_hp": 30, "opp_armor": 0, "opp_immune": False,
            "own": list(own), "enemy": list(enemy), "hand": list(hand), "weapon": None, "hero_left": 1,
            "hp_ready": False, "opp_weapon": 0, "opp_class": "MAGE", "opp_hand": 3, "draws": 0, "next_id": -1,
            "hero_bonus": 0, "hp_cost": 2, "hp_kind": "recruit", "demons": 0, "overload": 0, "secrets": 0}


# Sea Giant: 10 - minions on the battlefield
s = state(own=[minion(1, "x", 1, 1)] * 3, enemy=[minion(2, "y", 1, 1)] * 2, hand=[card(9, "EX1_586", "MINION", 5, 8, 8)])
assert move.cost(s, s["hand"][0]) == 5

# Blood Knight takes every shield: +3/+3 each
s = state(own=[minion(1, "EX1_008", 1, 1, ds=True)], enemy=[minion(2, "y", 2, 2, ds=True)],
          hand=[card(9, "EX1_590", "MINION", 3, 3, 3)])
s = move.apply(s, ("play", 9, None), RNG)
knight = next(m for m in s["own"] if m["id"] == 9)
assert (knight["atk"], knight["hp"]) == (9, 9) and not any(m["ds"] for m in s["own"] + s["enemy"])

# Equality, then Wild Pyromancer's ping, clears every minion (including a 1/1 with a shield losing it first)
s = state(own=[minion(1, "NEW1_020", 3, 2)], enemy=[minion(2, "y", 5, 7), minion(3, "z", 1, 1, ds=True)],
          hand=[card(9, "EX1_619", "SPELL", 4)])
s = move.apply(s, ("play", 9, None), RNG)
assert not s["own"] and [m["ds"] for m in s["enemy"]] == [False]

# Cairne leaves Baine; Cult Master draws for the friendly death
s = state(own=[minion(1, "EX1_110", 4, 5), minion(2, "EX1_595", 4, 2)], enemy=[minion(3, "y", 6, 6)])
s = move.apply(s, ("attack", 1, 3), RNG)
assert [m["cid"] for m in s["own"]] == ["EX1_595", "EX1_110t"] and s["draws"] == 1

# Lay on Hands on our hero: heal 8 (capped) and draw 3
s = move.apply(state(hand=[card(9, "EX1_354", "SPELL", 8)], hp=25), ("play", 9, "me"), RNG)
assert s["hp"] == 30 and s["draws"] == 3

# Truesilver heals before the hit; Dread Corsair then costs 0
s = state(hand=[card(8, "CS2_097", "WEAPON", 4, 4), card(9, "NEW1_022", "MINION", 4, 3, 3)],
          enemy=[minion(3, "y", 3, 4)], hp=20)
s = move.apply(s, ("play", 8, None), RNG)
assert move.cost(s, s["hand"][0]) == 0
s = move.apply(s, ("attack", "me", 3), RNG)
assert s["hp"] == 19 and not s["enemy"] and s["weapon"]["dur"] == 1

# Lava Burst with Bloodmage Thalnos: 6 to the face, Overload 2, Unbound Elemental grows
s = state(own=[minion(1, "EX1_012", 1, 1, sd=1), minion(2, "EX1_258", 2, 4)], hand=[card(9, "EX1_241", "SPELL", 3)])
s = move.apply(s, ("play", 9, "hero"), RNG)
assert s["opp_hp"] == 24 and s["overload"] == 2 and s["own"][1]["atk"] == 3

# Unleash the Hounds: one charging 1/1 per enemy minion; a Hound dying grows Scavenging Hyena
s = state(own=[minion(1, "EX1_531", 2, 2)], enemy=[minion(2, "y", 1, 1), minion(3, "z", 3, 3)],
          hand=[card(9, "EX1_538", "SPELL", 3)])
s = move.apply(s, ("play", 9, None), RNG)
hound = [m for m in s["own"] if m["cid"] == "EX1_538t"]
assert len(hound) == 2 and all(h["left"] == 1 for h in hound)
s = move.apply(s, ("attack", hound[0]["id"], 3), RNG)
assert (s["own"][0]["atk"], s["own"][0]["hp"]) == (4, 3)

# Savannah Highmane leaves two 2/2 Hyenas
s = state(own=[minion(1, "EX1_534", 6, 5)], enemy=[minion(3, "y", 8, 8)])
s = move.apply(s, ("attack", 1, 3), RNG)
assert [m["cid"] for m in s["own"]] == ["EX1_534t", "EX1_534t"]

# Hellfire hits our own hero too; Life Tap costs 2 health and draws
s = move.apply(state(hand=[card(9, "CS2_062", "SPELL", 4)], hp=20), ("play", 9, None), RNG)
assert s["hp"] == 17 and s["opp_hp"] == 27
s = move.apply(state(hp=20) | {"hp_ready": True, "hp_kind": "tap"}, ("power",), RNG)
assert s["hp"] == 18 and s["draws"] == 1

# Lord Jaraxxus: our hero becomes 15 health with a 3/8 weapon and the Infernal hero power
s = move.apply(state(hand=[card(9, "EX1_323", "MINION", 9, 3, 15)], hp=8), ("play", 9, None), RNG)
assert s["hp"] == 15 and s["weapon"]["dur"] == 8 and s["hp_kind"] == "infernal" and not s["own"]

# Rockbiter on a minion is temporary: the evaluation does not keep the +3
m = minion(1, "x", 2, 2)
s = move.apply(state(own=[m], hand=[card(9, "CS2_045", "SPELL", 2)]), ("play", 9, 1), RNG)
assert s["own"][0]["atk"] == 5 and move.mval(s["own"][0]) == move.mval(m)

# Zoo: Abusive Sergeant's +2 is temporary; Flame Imp costs 3 health; Soulfire hits for 4 and discards a card
m = minion(1, "x", 2, 2)
s = move.apply(state(own=[m], hand=[card(8, "CS2_188", "MINION", 1, 1, 1), card(9, "EX1_319", "MINION", 1, 3, 2),
                                    card(7, "EX1_308", "SPELL", 1), card(6, "y", "MINION", 1, 1, 1)], hp=20), ("play", 8, 1), RNG)
assert s["own"][0]["atk"] == 4 and move.mval(s["own"][0]) == move.mval(m)
s = move.apply(s, ("play", 9, None), RNG)
assert s["hp"] == 17
s = move.apply(s, ("play", 7, "hero"), RNG)
assert s["opp_hp"] == 26 and len(s["hand"]) == 0

# An enemy Doomsayer wipes both boards at the start of their turn: adding a minion into it gains little
s = state(enemy=[minion(2, "NEW1_021", 0, 7)])
big = state(own=[minion(1, "x", 5, 5)], enemy=[minion(2, "NEW1_021", 0, 7)])
assert move.evaluate(big) - move.evaluate(s) < 0.5 * move.mval(minion(1, "x", 5, 5))
