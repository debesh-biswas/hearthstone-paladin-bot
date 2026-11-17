"""Built-in greedy bot (PLANNING.md §7.3): deterministic, no search, generic over decks.

Each decision scores every concrete candidate built from the legal-action templates and plays the best one;
it ends the turn when no candidate scores above 0. Ties go to the earlier candidate (template order), so the
bot is deterministic given the game seed. All weights live in greedy_config.json.
"""

from __future__ import annotations

import math
import re
from typing import Any

from .. import cards as cards_mod
from .._fileio import load_json
from .._resources import GREEDY_CONFIG
from ..deck import Deck
from .base import Decision, Player

INF = math.inf
_HARMFUL_RE = re.compile(r"\b(deal|damage|destroy|silence|transform|freeze|return|swap|take control)\b", re.I)


def load_config(path=GREEDY_CONFIG) -> dict[str, Any]:
    return load_json(path)


class GreedyBot(Player):
    kind = "greedy"

    def __init__(self, name: str, deck: Deck, config: dict[str, Any] | None = None):
        super().__init__(name, deck)
        self.cfg = config or load_config()
        self.catalog = cards_mod.load()
        self.first_player: int | None = None

    # ----------------------------------------------------------------------------------- valuation

    def value(self, m: dict[str, Any]) -> float:
        w = self.cfg["value"]
        return (
            m.get("attack", 0)
            + m.get("health", 0)
            + w["taunt"] * bool(m.get("taunt"))
            + w["divine_shield"] * bool(m.get("divine_shield"))
            + w["windfury"] * bool(m.get("windfury"))
            + w["stealth"] * bool(m.get("stealth"))
        )

    def hand_minion_value(self, card: dict[str, Any]) -> float:
        mech = set(self.catalog.get(card["card_id"], {}).get("mechanics", []))
        return self.value(
            {
                "attack": card.get("attack", 0),
                "health": card.get("health", 0),
                "taunt": "TAUNT" in mech,
                "divine_shield": "DIVINE_SHIELD" in mech,
                "windfury": "WINDFURY" in mech,
                "stealth": "STEALTH" in mech,
            }
        )

    # ----------------------------------------------------------------------------------- decide

    def decide(self, state: dict[str, Any]) -> Decision:
        for ev in state.get("events") or []:
            if ev.get("event") == "game_start":
                self.first_player = ev.get("first_player")
        phase = state["phase"]
        legal = state["legal_actions"]
        if phase == "mulligan":
            return Decision("action", self._mulligan(state, legal[0]))
        if phase == "choice":
            t = next(t for t in legal if t["type"] == "choose")
            best = self._best_option(state, t["options"])
            return Decision("action", {"type": "choose", "options": [best]})
        best_score, best_action = 0.0, {"type": "end_turn"}
        for score, action in self._candidates(state, legal):
            if score > best_score:
                best_score, best_action = score, action
        return Decision("action", best_action)

    def _mulligan(self, state, t) -> dict[str, Any]:
        cfg = self.cfg["mulligan"]
        hand = {c["entity_id"]: c for c in state["you"]["hand"]}
        going_second = len(t["options"]) >= 4 or (self.first_player is not None and self.first_player != state["player"])
        replace = []
        kept_four = False
        for eid in t["options"]:
            cost = hand[eid]["cost"] if eid in hand else 99
            if cost <= cfg["keep_max_cost"]:
                continue
            if cost == 4 and going_second and cfg["keep_one_four_drop_when_second"] and not kept_four:
                kept_four = True
                continue
            replace.append(eid)
        return {"type": "mulligan", "replace": replace}

    def _best_option(self, state, options) -> int:
        best, best_score = options[0]["entity_id"], -INF
        for o in options:
            if o.get("type") == "MINION":
                s = self.hand_minion_value(o)
            else:
                s = self._spell_card_score(state, o.get("card_id"), o.get("cost", 0))
            if s > best_score:
                best, best_score = o["entity_id"], s
        return best

    def _spell_card_score(self, state, card_id, cost) -> float:
        """Rough score of a spell card regardless of targets (used for Discover picks)."""
        spec = self.cfg["spells"].get(card_id)
        if spec is None:
            return self.cfg["play"]["unknown_untargeted"]
        kind = spec["kind"]
        if kind in ("damage", "random_damage", "aoe"):
            return spec.get("damage", 0)
        if kind == "hard_removal":
            return self.cfg["play"]["hard_removal_min_value"]
        if kind == "draw":
            return self.cfg["play"]["draw_spell"]
        return self.cfg["play"]["unknown_untargeted"]

    # ----------------------------------------------------------------------------------- candidates

    def _ctx(self, state):
        you, opp = state["you"], state["opponent"]
        ctx = {
            "you": you,
            "opp": opp,
            "own": {m["entity_id"]: m for m in you["board"]},
            "enemy": {m["entity_id"]: m for m in opp["board"]},
            "own_hero": you["hero"]["entity_id"],
            "enemy_hero": opp["hero"]["entity_id"],
            "spell_damage": sum(m.get("spell_damage", 0) for m in you["board"]),
            "hand": {c["entity_id"]: c for c in you["hand"]},
            "hero_class": you["hero"].get("hero_class"),
        }
        return ctx

    def _candidates(self, state, legal):
        ctx = self._ctx(state)
        lethal = self._lethal(state, legal, ctx)
        if lethal is not None:
            yield INF, lethal
            return
        for t in legal:
            tt = t["type"]
            if tt == "play_card":
                yield from self._play_candidates(state, t, ctx)
            elif tt == "attack":
                yield from self._attack_candidates(t, ctx)
            elif tt == "hero_power":
                yield from self._hero_power_candidates(state, t, ctx)

    def _lethal(self, state, legal, ctx):
        enemy_hp = ctx["opp"]["hero"]["health"] + ctx["opp"]["hero"]["armor"]
        if ctx["opp"]["hero"].get("immune"):
            return None
        eh = ctx["enemy_hero"]
        mana = ctx["you"]["mana"]
        face_attacks = [t for t in legal if t["type"] == "attack" and eh in t["targets"]]
        attack_dmg = 0
        for t in face_attacks:
            if t["attacker"] == ctx["own_hero"]:
                attack_dmg += ctx["you"]["hero"]["attack"]
            else:
                attack_dmg += ctx["own"].get(t["attacker"], {}).get("attack", 0)
        # castable face damage: spells (best damage per mana first), then hero power
        burn = []
        for t in legal:
            if t["type"] != "play_card" or t.get("choose"):
                continue
            card = ctx["hand"].get(t["card"])
            spec = self.cfg["spells"].get(card["card_id"]) if card else None
            if not spec:
                continue
            dmg = spec.get("damage", 0) + ctx["spell_damage"]
            if spec["kind"] == "damage" and not spec.get("minion_only") and t["targets"] and eh in t["targets"]:
                burn.append((dmg, card["cost"], {"type": "play_card", "card": t["card"], "target": eh}))
            elif spec["kind"] == "random_damage" and not ctx["enemy"]:
                burn.append((dmg, card["cost"], {"type": "play_card", "card": t["card"]}))
        hp_t = next((t for t in legal if t["type"] == "hero_power"), None)
        hp_dmg = self.cfg["hero_power_damage"].get(ctx["hero_class"], 0)
        if hp_t is not None and hp_dmg:
            hp_cost = ctx["you"]["hero_power"]["cost"]
            if hp_t["targets"] is None and ctx["hero_class"] == "HUNTER":
                burn.append((hp_dmg, hp_cost, {"type": "hero_power"}))
            elif hp_t["targets"] and eh in hp_t["targets"]:
                burn.append((hp_dmg, hp_cost, {"type": "hero_power", "target": eh}))
        burn.sort(key=lambda b: (-(b[0] / max(b[1], 0.5)), b[1]))
        spent, burn_dmg, plan = 0, 0, []
        for dmg, cost, action in burn:
            if spent + cost <= mana:
                spent += cost
                burn_dmg += dmg
                plan.append(action)
        if attack_dmg + burn_dmg < enemy_hp:
            return None
        if plan:
            return plan[0]  # spells (and hero power) first
        if face_attacks:
            return {"type": "attack", "attacker": face_attacks[0]["attacker"], "target": eh}
        return None

    def _attack_candidates(self, t, ctx):
        cfg = self.cfg["trade"]
        attacker_id = t["attacker"]
        is_hero = attacker_id == ctx["own_hero"]
        a = ctx["you"]["hero"] if is_hero else ctx["own"].get(attacker_id)
        if a is None:
            return
        for target in t["targets"]:
            if target == ctx["enemy_hero"]:
                yield self.cfg["face"]["per_attack"] * a["attack"], {"type": "attack", "attacker": attacker_id, "target": target}
                continue
            m = ctx["enemy"].get(target)
            if m is None:
                continue
            kills = a["attack"] >= m["health"] and not m.get("divine_shield")
            if is_hero:
                taken = m["attack"]
                if kills:
                    score = self.value(m) + cfg["kill_and_survive_bonus"] - cfg["hero_damage_taken"] * taken
                else:
                    score = cfg["chip_dealt"] * (0 if m.get("divine_shield") else a["attack"]) - cfg["chip_taken"] * taken
            else:
                dies = m["attack"] >= a["health"] and not a.get("divine_shield") and m["attack"] > 0
                if kills and not dies:
                    score = self.value(m) + cfg["kill_and_survive_bonus"]
                elif kills and dies:
                    score = self.value(m) - self.value(a)
                    if score <= 0:
                        continue
                else:
                    dealt = 0 if m.get("divine_shield") else min(a["attack"], m["health"])
                    taken = 0 if a.get("divine_shield") else min(m["attack"], a["health"])
                    score = cfg["chip_dealt"] * dealt - cfg["chip_taken"] * taken
            yield score, {"type": "attack", "attacker": attacker_id, "target": target}

    def _enemy_minion_targets(self, targets, ctx):
        return [ctx["enemy"][x] for x in (targets or []) if x in ctx["enemy"]]

    def _own_targets(self, targets, ctx):
        return [ctx["own"][x] for x in (targets or []) if x in ctx["own"]]

    def _targeted_effect(self, targets, ctx, text, cost, base_score):
        """Pick a target for a targeted battlecry / unknown targeted spell using its text."""
        if _HARMFUL_RE.search(text or ""):
            enemies = self._enemy_minion_targets(targets, ctx)
            if enemies:
                best = max(enemies, key=self.value)
                return base_score, best["entity_id"]
            if ctx["enemy_hero"] in targets:
                return base_score, ctx["enemy_hero"]
            return None
        own = self._own_targets(targets, ctx)
        if own:
            best = max(own, key=lambda m: (m["attack"], self.value(m)))
            return base_score, best["entity_id"]
        if ctx["own_hero"] in targets:
            return base_score, ctx["own_hero"]
        return None

    def _damage_spell(self, dmg, targets, ctx, cost, minion_only=False):
        p = self.cfg["play"]
        best = None
        for m in self._enemy_minion_targets(targets, ctx):
            if dmg >= m["health"] and not m.get("divine_shield"):
                s = self.value(m) - p["damage_spell_cost_penalty"] * cost
                if best is None or s > best[0]:
                    best = (s, m["entity_id"])
        if best is not None:
            return best
        if not minion_only and ctx["enemy_hero"] in (targets or []):
            return p["damage_spell_face"] * dmg, ctx["enemy_hero"]
        return None

    def _aoe_score(self, dmg, hits_own, ctx, cost):
        killed = sum(self.value(m) for m in ctx["enemy"].values() if dmg >= m["health"] and not m.get("divine_shield"))
        lost = 0.0
        if hits_own:
            lost = sum(self.value(m) for m in ctx["own"].values() if dmg >= m["health"] and not m.get("divine_shield"))
        return killed - lost - self.cfg["play"]["aoe_cost_penalty"] * cost

    def _spell_effect(self, state, card_id, text, cost, targets, ctx):
        """(score, target) for casting a spell with the given targets, or None if not worth it."""
        p = self.cfg["play"]
        spec = self.cfg["spells"].get(card_id)
        kind = spec["kind"] if spec else None
        if kind == "damage":
            return self._damage_spell(spec["damage"] + ctx["spell_damage"], targets, ctx, cost, spec.get("minion_only", False))
        if kind == "random_damage":
            return p["damage_spell_face"] * (spec["damage"] + ctx["spell_damage"]), None
        if kind == "aoe":
            return self._aoe_score(spec["damage"] + ctx["spell_damage"], spec.get("hits_own", False), ctx, cost), None
        if kind == "draw":
            return (p["draw_spell"] if len(ctx["you"]["hand"]) < p["draw_spell_max_hand"] else 0.0), None
        if kind == "hard_removal":
            enemies = self._enemy_minion_targets(targets, ctx)
            if not enemies:
                return None
            best = max(enemies, key=self.value)
            if self.value(best) < p["hard_removal_min_value"]:
                return None
            return self.value(best) - p["hard_removal_cost_penalty"] * cost, best["entity_id"]
        if kind == "buff":
            if not targets:
                return p["buff_spell"], None
            return self._targeted_effect(targets, ctx, "", cost, p["buff_spell"] + 0.1 * cost)
        if kind == "coin":
            mana = ctx["you"]["mana"]
            if any(c["cost"] == mana + 1 for c in ctx["you"]["hand"] if c["card_id"] != card_id):
                return p["coin_enables_play"], None
            return None
        # unknown spell
        if targets:
            if _HARMFUL_RE.search(text or "") or not self._own_targets(targets, ctx):
                return self._damage_spell(p["unknown_targeted_damage"] + ctx["spell_damage"], targets, ctx, cost)
            return self._targeted_effect(targets, ctx, text, cost, p["buff_spell"])
        return p["unknown_untargeted"], None

    def _play_candidates(self, state, t, ctx):
        card = ctx["hand"].get(t["card"])
        if card is None:
            return
        p = self.cfg["play"]
        options = t.get("choose")
        variants = (
            [(o["card_id"], o.get("text", ""), o.get("targets"), o["entity_id"]) for o in options]
            if options
            else [(card["card_id"], card.get("text", ""), t.get("targets"), None)]
        )
        for card_id, text, targets, choose in variants:
            action: dict[str, Any] = {"type": "play_card", "card": t["card"]}
            if choose is not None:
                action["choose"] = choose
            if card["type"] == "MINION":
                score = self.hand_minion_value(card) + p["minion_cost_bonus"] * card["cost"]
                if options:
                    score += 0.5  # Choose One minion: prefer the variant chosen first; both are usually fine
                if targets:
                    pick = self._targeted_effect(targets, ctx, text, card["cost"], score)
                    if pick is None:
                        continue
                    score, action["target"] = pick
            elif card["type"] == "WEAPON":
                if ctx["you"]["weapon"] is not None:
                    score = 0.1
                else:
                    score = p["weapon_per_stat"] * card.get("attack", 0) * card.get("durability", 0) + 0.1 * card["cost"]
                if targets:
                    pick = self._targeted_effect(targets, ctx, text, card["cost"], score)
                    if pick is None:
                        continue
                    score, action["target"] = pick
            else:
                eff = self._spell_effect(state, card_id, text, card["cost"], targets, ctx)
                if eff is None:
                    continue
                score, target = eff
                if targets:
                    if target is None:
                        continue
                    action["target"] = target
            yield score, action

    def _hero_power_candidates(self, state, t, ctx):
        hc = ctx["hero_class"]
        cfg = self.cfg["hero_power"]
        targets = t.get("targets")
        if t.get("choose"):
            yield cfg["default"], {"type": "hero_power", "choose": t["choose"][0]["entity_id"], **(
                {"target": t["choose"][0]["targets"][0]} if t["choose"][0].get("targets") else {})}
            return
        dmg = self.cfg["hero_power_damage"].get(hc)
        if hc == "MAGE" and targets:
            r = self._damage_spell(dmg + 0, targets, ctx, ctx["you"]["hero_power"]["cost"])
            if r is not None:
                yield r[0], {"type": "hero_power", "target": r[1]}
            return
        if hc == "HUNTER":
            yield self.cfg["play"]["damage_spell_face"] * dmg, {"type": "hero_power"}
            return
        if hc == "WARLOCK":
            you = ctx["you"]
            if len(you["hand"]) < cfg["life_tap_max_hand"] and you["hero"]["health"] >= cfg["life_tap_min_health"]:
                yield cfg["default"], {"type": "hero_power"}
            return
        if hc == "PRIEST" and targets:
            own = [ctx["you"]["hero"]] + list(ctx["own"].values())
            damaged = [
                c for c in own if c["entity_id"] in targets and c.get("max_health", c["health"]) - c["health"] >= cfg["heal_min_missing"]
            ]
            if damaged:
                best = min(damaged, key=lambda c: (c["health"], c["entity_id"]))
                yield cfg["default"], {"type": "hero_power", "target": best["entity_id"]}
            return
        if targets:
            yield cfg["default"], {"type": "hero_power", "target": targets[0]}
        else:
            yield cfg["default"], {"type": "hero_power"}
