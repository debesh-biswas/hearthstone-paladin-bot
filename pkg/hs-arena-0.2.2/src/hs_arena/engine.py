"""Wrapper around the vendored fireplace engine.

Responsibilities: start a seeded game from two decks, decide whose decision is pending, render per-player state
views and legal-action templates, validate concrete actions against those templates (with protocol error
codes), apply them, and produce the event stream (private per player + public for the replay).

Events come from (a) the explicit action being applied, (b) fireplace manager hooks (damage, heal, draw,
fatigue, summon, death, turn start) and (c) a diff of the visible state before/after the action (secrets,
weapons, minions that entered/left the board without a summon/death event).
"""

from __future__ import annotations

import traceback
from collections import Counter
from types import SimpleNamespace
from dataclasses import dataclass
from typing import Any

from ._fp import init_engine
from .cards import plain_text
from .deck import Deck
from .protocol import ACTION_TYPES, PHASE_ACTIONS

__all__ = ["Engine", "EngineCrash", "StepResult", "Event"]


class EngineCrash(Exception):
    """The engine raised while applying an action that passed validation: the game is voided."""

    def __init__(self, message: str, card_ids: list[str], tb: str, action: Any):
        super().__init__(message)
        self.card_ids = card_ids
        self.traceback = tb
        self.action = action


@dataclass
class StepResult:
    accepted: bool
    error: str | None = None
    message: str = ""


@dataclass
class Event:
    data: dict[str, Any]
    owner: int | None = None  # if set, only this player sees `data`
    public: dict[str, Any] | None = None  # what everybody else sees (None: hidden)

    def view(self, player: int | None) -> dict[str, Any] | None:
        if self.owner is None or self.owner == player:
            return self.data
        return self.public


class _Reject(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


class _Observer:
    """fireplace manager observer turning engine actions into events."""

    def __init__(self, engine: "Engine"):
        self.engine = engine

    def action_start(self, type, source, index, target):
        pass

    def action_end(self, type, source):
        pass

    def game_step(self, step, next_step):
        pass

    def new_entity(self, entity):
        pass

    def start_game(self):
        pass

    def turn(self, player):
        pass

    def game_action(self, action, source, *args):
        self.engine._on_game_action(action, source, args)

    def targeted_action(self, action, source, target, *args):
        self.engine._on_targeted_action(action, source, target, args)


class Engine:
    def __init__(self, deck1: Deck, deck2: Deck, seed: int, *, max_turns: int | None = None):
        init_engine()
        from ._vendor.fireplace import actions as fp_actions
        from ._vendor.fireplace.game import Game
        from ._vendor.fireplace.player import Player
        from hearthstone.enums import CardType, PlayState, Zone

        # action classes used for isinstance checks (a namespace of classes, so the engine can be deep-copied)
        self._A = SimpleNamespace(
            **{n: getattr(fp_actions, n) for n in ("MulliganChoice", "Discover", "Death", "BeginTurn", "Damage", "Heal", "Draw", "Fatigue", "Summon", "LosesDivineShield", "GainArmor")}
        )
        self._CardType = CardType
        self._PlayState = PlayState
        self._Zone = Zone
        self.seed = seed
        self.max_turns = max_turns
        self.decks = (deck1, deck2)
        self._p = [
            Player("Player1", list(deck1.cards), deck1.hero_id),
            Player("Player2", list(deck2.cards), deck2.hero_id),
        ]
        self.game = Game(players=tuple(self._p), seed=seed)
        self.events: list[Event] = []
        self._cursor = {1: 0, 2: 0}
        self._public_cursor = 0
        self.over = False
        self.winner: int | None = None
        self.reason: str | None = None
        self._conceded: int | None = None
        self._seen: set[int] = set()  # entity ids that were ever in a hand or in play (public graveyard rule)
        self._action_emitted: set[int] = set()  # entities announced by summon/play/death during the current action
        self._shield_emitted: set[int] = set()  # minions announced by divine_shield_lost during the current action
        self._armor: dict[int, int] = {}  # hero entity id -> armor as of the last event (for armor_absorbed)
        self.game.start()
        self.game.manager.register(_Observer(self))
        self.first_player = self.idx(self.game.player1)
        self._emit({"event": "game_start", "first_player": self.first_player})
        self._mark_seen()

    # ------------------------------------------------------------------------------------------- helpers

    def idx(self, player) -> int:
        return 1 if player is self._p[0] else 2

    def player(self, i: int):
        return self._p[i - 1]

    @property
    def turn(self) -> int:
        return int(self.game.turn)

    def _emit(self, data: dict[str, Any], owner: int | None = None, public: dict[str, Any] | None = None) -> None:
        self.events.append(Event(data, owner, public))

    def add_event(self, data: dict[str, Any]) -> None:
        """Public event added by the runner (illegal_action, agent_failure)."""
        self._emit(data)

    def take_events(self, i: int) -> list[dict[str, Any]]:
        """Events since the previous call for player i, in i's view."""
        out = []
        for ev in self.events[self._cursor[i]:]:
            v = ev.view(i)
            if v is not None:
                out.append(v)
        self._cursor[i] = len(self.events)
        return out

    def take_public_events(self) -> list[dict[str, Any]]:
        out = []
        for ev in self.events[self._public_cursor:]:
            v = ev.view(None)
            if v is not None:
                out.append(v)
        self._public_cursor = len(self.events)
        return out

    @staticmethod
    def _name(entity) -> str:
        return str(entity.data.name)

    def _type_name(self, entity) -> str:
        return self._CardType(int(entity.type)).name

    @staticmethod
    def _class_name(entity) -> str:
        from hearthstone.enums import CardClass

        return CardClass(int(entity.data.card_class)).name

    def _ref(self, entity) -> dict[str, Any] | None:
        if entity is None:
            return None
        return {"entity_id": entity.entity_id, "card_id": entity.id, "name": self._name(entity)}

    def _text(self, entity) -> str:
        try:
            return plain_text(entity.description)
        except Exception:  # dynamic text failed: fall back to the static card text
            return plain_text(getattr(entity.data, "description", ""))

    def _mark_seen(self) -> None:
        for pl in self._p:
            for c in pl.hand:
                self._seen.add(c.entity_id)
            for c in pl.field:
                self._seen.add(c.entity_id)
            for c in pl.secrets:
                self._seen.add(c.entity_id)
            if pl.weapon is not None:
                self._seen.add(pl.weapon.entity_id)

    # ------------------------------------------------------------------------------------------- pending

    def pending(self) -> tuple[int, str]:
        """(player, phase) of the decision the engine is waiting for. Only valid while not over."""
        MulliganChoice = self._A.MulliganChoice
        for i, pl in enumerate(self._p, 1):
            if isinstance(pl.choice, MulliganChoice):
                return i, "mulligan"
        cur = self.game.current_player
        if cur.choice is not None:
            return self.idx(cur), "choice"
        if cur.opponent.choice is not None:
            return self.idx(cur.opponent), "choice"
        return self.idx(cur), "main"

    # ------------------------------------------------------------------------------------------- views

    def _hero_view(self, pl) -> dict[str, Any]:
        h = pl.hero
        return {
            "entity_id": h.entity_id,
            "card_id": h.id,
            "name": self._name(h),
            "hero_class": self._class_name(h),
            "health": int(h.health),
            "max_health": int(h.max_health),
            "armor": int(h.armor),
            "attack": int(h.atk),
            "can_attack": bool(h.can_attack()),
            "frozen": bool(h.frozen),
            "immune": bool(h.immune),
        }

    def _hero_power_view(self, pl, usable: bool) -> dict[str, Any] | None:
        hp = pl.hero.power
        if hp is None:
            return None
        return {
            "entity_id": hp.entity_id,
            "card_id": hp.id,
            "name": self._name(hp),
            "cost": int(hp.cost),
            "usable": bool(usable),
            "text": _strip_prefix(self._text(hp), "Hero Power "),
        }

    def _weapon_view(self, pl) -> dict[str, Any] | None:
        w = pl.weapon
        if w is None:
            return None
        return {
            "entity_id": w.entity_id,
            "card_id": w.id,
            "name": self._name(w),
            "attack": int(w.atk),
            "durability": int(w.durability),
        }

    def _minion_view(self, m) -> dict[str, Any]:
        return {
            "entity_id": m.entity_id,
            "card_id": m.id,
            "name": self._name(m),
            "attack": int(m.atk),
            "health": int(m.health),
            "max_health": int(m.max_health),
            "can_attack": bool(m.can_attack()),
            "taunt": bool(m.taunt),
            "divine_shield": bool(m.divine_shield),
            "frozen": bool(m.frozen),
            "stealth": bool(m.stealthed),
            "windfury": bool(m.windfury),
            "charge": bool(m.charge),
            "poisonous": bool(m.poisonous),
            "deathrattle": bool(m.has_deathrattle),
            "spell_damage": int(m.spellpower or 0),
            "silenced": bool(m.silenced),
            "text": self._text(m),
        }

    def _hand_view(self, c, playable: bool) -> dict[str, Any]:
        CardType = self._CardType
        v: dict[str, Any] = {
            "entity_id": c.entity_id,
            "card_id": c.id,
            "name": self._name(c),
            "type": self._type_name(c),
            "cost": int(c.cost),
        }
        if c.type == CardType.MINION:
            v["attack"] = int(c.atk)
            v["health"] = int(c.health)
        elif c.type == CardType.WEAPON:
            v["attack"] = int(c.atk)
            v["durability"] = int(c.durability)
        v["text"] = self._text(c)
        v["playable"] = bool(playable)
        return v

    def _graveyard(self, pl) -> list[dict[str, str]]:
        CardType = self._CardType
        return [
            {"card_id": c.id, "name": self._name(c)}
            for c in pl.graveyard
            if c.type in (CardType.MINION, CardType.SPELL, CardType.WEAPON) and c.entity_id in self._seen
        ]

    def _player_view(self, pl, own: bool, templates: list[dict[str, Any]]) -> dict[str, Any]:
        playable_ids = {t["card"] for t in templates if t["type"] == "play_card"}
        hp_usable = any(t["type"] == "hero_power" for t in templates)
        v: dict[str, Any] = {
            "hero": self._hero_view(pl),
            "hero_power": self._hero_power_view(pl, hp_usable if own else False),
            "weapon": self._weapon_view(pl),
            "mana": int(pl.mana) if pl is self.game.current_player else 0,
            "max_mana": int(pl.max_mana),
            "overloaded": int(pl.overload_locked),
            "overload_next_turn": int(pl.overloaded),
        }
        if own:
            v["hand"] = [self._hand_view(c, c.entity_id in playable_ids) for c in pl.hand]
        else:
            v["hand_size"] = len(pl.hand)
        v["board"] = [self._minion_view(m) for m in pl.field]
        if own:
            v["secrets"] = [{"entity_id": s.entity_id, "card_id": s.id, "name": self._name(s)} for s in pl.secrets]
        else:
            v["secrets_count"] = len(pl.secrets)
        v["deck_remaining"] = len(pl.deck)
        if own:
            v["deck_remaining_counts"] = dict(sorted(Counter(c.id for c in pl.deck).items()))
        v["fatigue"] = int(pl.fatigue_counter)
        v["graveyard"] = self._graveyard(pl)
        return v

    def _choice_info(self, pl, phase: str) -> dict[str, Any] | None:
        if phase == "mulligan":
            return {"kind": "mulligan", "source": None}
        if phase == "choice":
            ch = pl.choice
            src = getattr(ch, "source", None)
            kind = "discover" if isinstance(ch, self._A.Discover) else "choice"
            ref = self._ref(src) if src is not None and hasattr(src, "data") and getattr(src, "data", None) else None
            return {"kind": kind, "source": ref}
        return None

    def view(self, i: int) -> dict[str, Any]:
        """State view for player i: turn, phase, you, opponent, choice, legal_actions."""
        pl = self.player(i)
        if self.over:
            phase = "game_over"
            templates: list[dict[str, Any]] = []
        else:
            pi, phase = self.pending()
            if pi != i:
                phase = "waiting"
                templates = []
            else:
                templates = self.legal_actions(i)
        return {
            "turn": self.turn,
            "phase": phase,
            "you": self._player_view(pl, True, templates),
            "opponent": self._player_view(pl.opponent, False, []),
            "choice": self._choice_info(pl, phase),
            "legal_actions": templates,
        }

    # ------------------------------------------------------------------------------------------- legal actions

    def _option_view(self, c) -> dict[str, Any]:
        v = {"entity_id": c.entity_id, "card_id": c.id, "name": self._name(c), "type": self._type_name(c)}
        if hasattr(c, "cost"):
            try:
                v["cost"] = int(c.cost)
            except Exception:
                pass
        if c.type == self._CardType.MINION:
            v["attack"] = int(c.atk)
            v["health"] = int(c.health)
        v["text"] = self._text(c)
        return v

    def _choose_options(self, parent, check_playable) -> list[dict[str, Any]]:
        opts = []
        parent_targets = parent.play_targets
        for opt in parent.choose_cards:
            if not check_playable(opt):
                continue
            if opt.requires_target():
                targets = sorted(t.entity_id for t in opt.play_targets if t in parent_targets)
                if not targets:
                    continue
            else:
                targets = None
            opts.append(
                {
                    "entity_id": opt.entity_id,
                    "card_id": opt.id,
                    "name": self._name(opt),
                    "text": self._text(opt),
                    "targets": targets,
                }
            )
        return opts

    def _play_template(self, pl, card) -> dict[str, Any] | None:
        if not card.is_playable():
            return None
        positions = list(range(len(pl.field) + 1)) if card.type == self._CardType.MINION else None
        if card.must_choose_one:
            opts = self._choose_options(card, lambda o: o.is_playable())
            if not opts:
                return None
            return {"type": "play_card", "card": card.entity_id, "targets": None, "positions": positions, "choose": opts}
        if card.requires_target():
            targets = sorted(t.entity_id for t in card.play_targets)
            if not targets:
                return None
        else:
            targets = None
        return {"type": "play_card", "card": card.entity_id, "targets": targets, "positions": positions, "choose": None}

    def _hero_power_template(self, pl) -> dict[str, Any] | None:
        hp = pl.hero.power
        if hp is None or not hp.is_usable():
            return None
        if hp.must_choose_one:
            opts = self._choose_options(hp, lambda o: True)
            if not opts:
                return None
            return {"type": "hero_power", "targets": None, "choose": opts}
        if hp.requires_target():
            targets = sorted(t.entity_id for t in hp.play_targets)
            if not targets:
                return None
            return {"type": "hero_power", "targets": targets}
        return {"type": "hero_power", "targets": None}

    def legal_actions(self, i: int) -> list[dict[str, Any]]:
        """Action templates for player i (empty unless i's decision is pending)."""
        if self.over:
            return []
        pi, phase = self.pending()
        if pi != i:
            return []
        pl = self.player(i)
        if phase == "mulligan":
            ch = pl.choice
            options = [c.entity_id for c in ch.cards]
            return [
                {"type": "mulligan", "options": options, "min": 0, "max": min(int(ch.max_count), len(options))},
                {"type": "concede"},
            ]
        if phase == "choice":
            ch = pl.choice
            options = [self._option_view(c) for c in ch.cards]
            return [
                {"type": "choose", "options": options, "min": int(ch.min_count), "max": int(ch.max_count)},
                {"type": "concede"},
            ]
        out: list[dict[str, Any]] = []
        for card in pl.hand:
            t = self._play_template(pl, card)
            if t is not None:
                out.append(t)
        for ch in pl.characters:
            if ch.can_attack():
                targets = sorted(t.entity_id for t in ch.attack_targets)
                if targets:
                    out.append({"type": "attack", "attacker": ch.entity_id, "targets": targets})
        t = self._hero_power_template(pl)
        if t is not None:
            out.append(t)
        out.append({"type": "end_turn"})
        out.append({"type": "concede"})
        return out

    # ------------------------------------------------------------------------------------------- validation

    def _find(self, templates, type_, key=None, value=None):
        for t in templates:
            if t["type"] == type_ and (key is None or t.get(key) == value):
                return t
        return None

    def _check_target(self, action, targets, what: str) -> int | None:
        target = action.get("target")
        if targets is None:
            if target is not None:
                raise _Reject("ILLEGAL_TARGET", f"{what} takes no target; omit 'target' (got {target!r})")
            return None
        if target is None:
            raise _Reject("TARGET_REQUIRED", f"{what} requires a target; one of {targets}")
        if not _is_int(target) or target not in targets:
            raise _Reject("ILLEGAL_TARGET", f"target {target!r} is not a valid target for {what}; one of {targets}")
        return target

    def _check_choose(self, action, options, what: str) -> dict[str, Any] | None:
        choose = action.get("choose")
        if options is None:
            if choose is not None:
                raise _Reject("ILLEGAL_CHOICE", f"{what} has no Choose One options; omit 'choose' (got {choose!r})")
            return None
        ids = [o["entity_id"] for o in options]
        if choose is None:
            raise _Reject("CHOOSE_REQUIRED", f"{what} is a Choose One card; set 'choose' to one of {ids}")
        for o in options:
            if _is_int(choose) and o["entity_id"] == choose:
                return o
        raise _Reject("ILLEGAL_CHOICE", f"choose {choose!r} is not one of the options {ids} of {what}")

    def _validate(self, i: int, action: Any) -> dict[str, Any]:
        """Return a resolved action (entity ids, all checked) or raise _Reject."""
        if not isinstance(action, dict):
            raise _Reject("BAD_JSON", "'action' must be a JSON object")
        atype = action.get("type")
        if not isinstance(atype, str) or atype not in ACTION_TYPES:
            raise _Reject("UNKNOWN_ACTION_TYPE", f"unknown action type {atype!r}; expected one of {list(ACTION_TYPES)}")
        _, phase = self.pending()
        if atype not in PHASE_ACTIONS[phase]:
            raise _Reject(
                "WRONG_PHASE", f"action '{atype}' is not allowed in phase '{phase}'; allowed: {list(PHASE_ACTIONS[phase])}"
            )
        templates = self.legal_actions(i)
        pl = self.player(i)
        if atype in ("end_turn", "concede"):
            return {"type": atype}
        if atype == "play_card":
            card_id = action.get("card")
            t = self._find(templates, "play_card", "card", card_id) if _is_int(card_id) else None
            if t is None:
                if _is_int(card_id) and any(c.entity_id == card_id for c in pl.hand):
                    raise _Reject("CARD_NOT_PLAYABLE", f"card {card_id} in your hand cannot be played now")
                raise _Reject("NOT_YOUR_ENTITY", f"card {card_id!r} is not a card in your hand")
            card = next(c for c in pl.hand if c.entity_id == card_id)
            what = f"card {card_id} ({self._name(card)})"
            opt = self._check_choose(action, t["choose"], what)
            targets = opt["targets"] if opt is not None else t["targets"]
            target = self._check_target(action, targets, what)
            position = action.get("position")
            if t["positions"] is None:
                if position is not None:
                    raise _Reject("ILLEGAL_POSITION", f"{what} is not a minion; omit 'position' (got {position!r})")
            elif position is not None and (not _is_int(position) or position not in t["positions"]):
                raise _Reject("ILLEGAL_POSITION", f"position {position!r} is not one of {t['positions']}")
            return {
                "type": "play_card",
                "card": card,
                "target": target,
                "position": position,
                "choose": opt["entity_id"] if opt else None,
            }
        if atype == "attack":
            attacker_id = action.get("attacker")
            t = self._find(templates, "attack", "attacker", attacker_id) if _is_int(attacker_id) else None
            if t is None:
                if _is_int(attacker_id) and any(c.entity_id == attacker_id for c in pl.characters):
                    raise _Reject("CANNOT_ATTACK", f"character {attacker_id} cannot attack now")
                raise _Reject("NOT_YOUR_ENTITY", f"attacker {attacker_id!r} is not one of your characters")
            attacker = next(c for c in pl.characters if c.entity_id == attacker_id)
            target = self._check_target(action, t["targets"], f"attacker {attacker_id} ({self._name(attacker)})")
            return {"type": "attack", "attacker": attacker, "target": target}
        if atype == "hero_power":
            t = self._find(templates, "hero_power")
            if t is None:
                raise _Reject("HERO_POWER_UNUSABLE", "your hero power cannot be used now")
            opt = self._check_choose(action, t.get("choose"), "the hero power")
            targets = opt["targets"] if opt is not None else t["targets"]
            target = self._check_target(action, targets, "the hero power")
            return {"type": "hero_power", "target": target, "choose": opt["entity_id"] if opt else None}
        if atype == "mulligan":
            t = self._find(templates, "mulligan")
            replace = action.get("replace", [])
            if replace is None:
                replace = []
            if not isinstance(replace, list) or not all(_is_int(x) for x in replace):
                raise _Reject("ILLEGAL_CHOICE", f"'replace' must be a list of entity ids (got {replace!r})")
            if len(set(replace)) != len(replace):
                raise _Reject("ILLEGAL_CHOICE", f"'replace' contains duplicates: {replace}")
            bad = [x for x in replace if x not in t["options"]]
            if bad:
                raise _Reject("ILLEGAL_CHOICE", f"cards {bad} are not in your mulligan options {t['options']}")
            if not (t["min"] <= len(replace) <= t["max"]):
                raise _Reject("ILLEGAL_CHOICE", f"replace between {t['min']} and {t['max']} cards")
            return {"type": "mulligan", "replace": list(replace)}
        if atype == "choose":
            t = self._find(templates, "choose")
            options = action.get("options")
            ids = [o["entity_id"] for o in t["options"]]
            if not isinstance(options, list) or not all(_is_int(x) for x in options):
                raise _Reject("ILLEGAL_CHOICE", f"'options' must be a list of entity ids from {ids} (got {options!r})")
            if len(set(options)) != len(options):
                raise _Reject("ILLEGAL_CHOICE", f"'options' contains duplicates: {options}")
            bad = [x for x in options if x not in ids]
            if bad:
                raise _Reject("ILLEGAL_CHOICE", f"{bad} are not among the options {ids}")
            if not (t["min"] <= len(options) <= t["max"]):
                raise _Reject("ILLEGAL_CHOICE", f"choose between {t['min']} and {t['max']} options")
            return {"type": "choose", "options": list(options)}
        raise _Reject("UNKNOWN_ACTION_TYPE", f"unknown action type {atype!r}")  # pragma: no cover

    def validate(self, i: int, action: Any) -> StepResult:
        """Check an action without applying it."""
        try:
            self._validate(i, action)
        except _Reject as r:
            return StepResult(False, r.code, r.message)
        return StepResult(True)

    # ------------------------------------------------------------------------------------------- apply

    def step(self, i: int, action: Any) -> StepResult:
        """Validate and apply an action of player i. Raises EngineCrash if the engine fails on a valid action."""
        if self.over:
            raise RuntimeError("game is over")
        pi, _ = self.pending()
        if pi != i:
            raise RuntimeError(f"player {i} is not the pending player")
        try:
            resolved = self._validate(i, action)
        except _Reject as r:
            return StepResult(False, r.code, r.message)
        self._apply(i, resolved)
        return StepResult(True)

    def _character(self, entity_id: int | None):
        if entity_id is None:
            return None
        for c in self.game.characters:
            if c.entity_id == entity_id:
                return c
        raise KeyError(entity_id)

    def _snapshot(self):
        snap = []
        for pl in self._p:
            snap.append(
                {
                    "board": [(m.entity_id, m) for m in pl.field],
                    "shields": {m.entity_id for m in pl.field if m.divine_shield},
                    "secrets": [(s.entity_id, s) for s in pl.secrets],
                    "weapon": pl.weapon,
                    "weapon_id": pl.weapon.entity_id if pl.weapon is not None else None,
                }
            )
        return snap

    def _involved_card_ids(self, i: int, resolved: dict[str, Any]) -> list[str]:
        ids: list[str] = []
        pl = self.player(i)
        try:
            if resolved["type"] == "play_card":
                ids.append(resolved["card"].id)
                if resolved.get("choose") is not None:
                    ids += [o.id for o in resolved["card"].choose_cards if o.entity_id == resolved["choose"]]
            elif resolved["type"] == "attack":
                ids.append(resolved["attacker"].id)
            elif resolved["type"] == "hero_power" and pl.hero.power is not None:
                ids.append(pl.hero.power.id)
            elif resolved["type"] == "choose" and pl.choice is not None:
                ids += [c.id for c in pl.choice.cards if c.entity_id in resolved["options"]]
                src = getattr(pl.choice, "source", None)
                if src is not None and hasattr(src, "id"):
                    ids.append(src.id)
            target = resolved.get("target")
            if target is not None:
                ids.append(self._character(target).id)
        except Exception:
            pass
        return ids

    def _apply(self, i: int, r: dict[str, Any]) -> None:
        from ._vendor.fireplace.exceptions import GameOver

        pl = self.player(i)
        before = self._snapshot()
        self._action_emitted = set()
        self._shield_emitted = set()
        self._armor = {p.hero.entity_id: int(p.hero.armor) for p in self._p}
        involved = self._involved_card_ids(i, r)
        self._mark_seen()
        try:
            t = r["type"]
            if t == "play_card":
                card = r["card"]
                target = self._character(r["target"])
                choose = None
                if r["choose"] is not None:
                    choose = next(o for o in card.choose_cards if o.entity_id == r["choose"])
                position = r["position"]
                ev = {
                    "event": "play_card",
                    "player": i,
                    "card_id": card.id,
                    "name": self._name(card),
                    "entity_id": card.entity_id,
                    "cost": int(card.cost),
                    "target": self._ref(target),
                    "position": (position if position is not None else len(pl.field))
                    if card.type == self._CardType.MINION
                    else None,
                    "choose": {"card_id": choose.id, "name": self._name(choose)} if choose is not None else None,
                }
                self._action_emitted.add(card.entity_id)
                self._seen.add(card.entity_id)
                if card.data.secret:
                    self._emit(ev, owner=i, public=None)  # the secret_played diff event is the public trace
                else:
                    self._emit(ev)
                card.play(target=target, index=position, choose=choose)
            elif t == "attack":
                attacker = r["attacker"]
                target = self._character(r["target"])
                self._emit(
                    {"event": "attack", "player": i, "attacker": self._ref(attacker), "target": self._ref(target)}
                )
                attacker.attack(target)
            elif t == "hero_power":
                hp = pl.hero.power
                target = self._character(r["target"])
                choose = None
                if r["choose"] is not None:
                    choose = next(o for o in hp.choose_cards if o.entity_id == r["choose"])
                self._emit(
                    {
                        "event": "hero_power",
                        "player": i,
                        "card_id": hp.id,
                        "name": self._name(hp),
                        "target": self._ref(target),
                    }
                )
                hp.use(target=target, choose=choose)
            elif t == "end_turn":
                self._emit({"event": "end_turn", "player": i})
                self.game.end_turn()
            elif t == "concede":
                self._conceded = i
                pl.concede()
            elif t == "mulligan":
                ch = pl.choice
                replaced = [c for c in ch.cards if c.entity_id in r["replace"]]
                # MulliganChoice.choose() takes the replacements from the top of the deck, one per replaced card
                # (replaced cards go to the bottom). Emit before choose(): the second mulligan starts turn 1.
                drawn = [c.id for c in reversed(list(pl.deck))][: len(replaced)]
                self._emit(
                    {
                        "event": "mulligan",
                        "player": i,
                        "replaced": len(replaced),
                        "replaced_card_ids": [c.id for c in replaced],
                        "drawn_card_ids": drawn,
                    },
                    owner=i,
                    public={"event": "mulligan", "player": i, "replaced": len(replaced)},
                )
                ch.choose(*replaced)
            elif t == "choose":
                ch = pl.choice
                picked = [c for c in ch.cards if c.entity_id in r["options"]]
                for c in picked:
                    self._emit(
                        {"event": "choose", "player": i, "card_id": c.id, "name": self._name(c)},
                        owner=i,
                        public={"event": "choose", "player": i},
                    )
                if len(picked) == 1:
                    ch.choose(picked[0])
                else:
                    ch.choose(*picked)
        except GameOver:
            pass
        except Exception as e:
            tb = traceback.format_exc()
            raise EngineCrash(f"{type(e).__name__}: {e}", involved, tb, _public_action(r)) from e
        try:
            self._diff(before)
        except Exception:
            pass
        self._mark_seen()
        if self.game.ended:
            self._finish_from_engine()
        elif self.max_turns is not None and self.turn > self.max_turns:
            self._end(None, "max_turns")

    def _diff(self, before) -> None:
        after = self._snapshot()
        for k, (b, a) in enumerate(zip(before, after), 1):
            b_ids = {eid for eid, _ in b["board"]}
            a_ids = {eid for eid, _ in a["board"]}
            for eid, m in b["board"]:
                if eid not in a_ids and eid not in self._action_emitted:
                    self._emit({"event": "leave_board", "player": k, "entity_id": eid, "card_id": m.id, "name": self._name(m)})
            for eid, m in a["board"]:
                if eid not in b_ids and eid not in self._action_emitted:
                    self._action_emitted.add(eid)
                    self._emit({"event": "summon", "player": k, "entity_id": eid, "card_id": m.id, "name": self._name(m)})
            # shields removed without LosesDivineShield (Silence, Blood Knight's UnsetTags)
            for eid, m in a["board"]:
                if eid in b["shields"] and eid not in a["shields"] and eid not in self._shield_emitted:
                    self._emit_shield_lost(m)
            b_sec = {eid for eid, _ in b["secrets"]}
            a_sec = {eid for eid, _ in a["secrets"]}
            for eid, s in a["secrets"]:
                if eid not in b_sec:
                    self._emit(
                        {"event": "secret_played", "player": k, "card_id": s.id, "name": self._name(s)},
                        owner=k,
                        public={"event": "secret_played", "player": k},
                    )
            for eid, s in b["secrets"]:
                if eid not in a_sec:
                    self._emit({"event": "secret_revealed", "player": k, "card_id": s.id, "name": self._name(s)})
            if b["weapon_id"] != a["weapon_id"]:
                if b["weapon"] is not None:
                    w = b["weapon"]
                    self._emit({"event": "weapon_destroyed", "player": k, "card_id": w.id, "name": self._name(w)})
                if a["weapon"] is not None:
                    w = a["weapon"]
                    self._emit(
                        {
                            "event": "weapon_equipped",
                            "player": k,
                            "card_id": w.id,
                            "name": self._name(w),
                            "attack": int(w.atk),
                            "durability": int(w.durability),
                        }
                    )

    # ------------------------------------------------------------------------------------------- hooks

    def _on_game_action(self, action, source, args) -> None:
        A = self._A
        CardType = self._CardType
        if isinstance(action, A.Death):
            card = args[0] if args else None
            if card is not None and card.type == CardType.MINION:
                self._action_emitted.add(card.entity_id)
                self._emit(
                    {
                        "event": "death",
                        "player": self.idx(card.controller),
                        "entity_id": card.entity_id,
                        "card_id": card.id,
                        "name": self._name(card),
                    }
                )
        elif isinstance(action, A.BeginTurn):
            player = args[0] if args else None
            if player is not None:
                self._emit({"event": "turn_start", "turn": self.turn, "player": self.idx(player)})

    def _on_targeted_action(self, action, source, target, args) -> None:
        A = self._A
        CardType = self._CardType
        if isinstance(action, (A.Damage, A.Heal)):
            amount = args[0] if args else 0
            if not amount or getattr(target, "type", None) not in (CardType.HERO, CardType.MINION):
                return
            ev = {
                "event": "damage" if isinstance(action, A.Damage) else "heal",
                "player": self.idx(target.controller),
                "entity_id": target.entity_id,
                "card_id": target.id,
                "name": self._name(target),
                "amount": int(amount),
                "health_after": int(target.health),
            }
            if source is not None and hasattr(source, "data") and getattr(source, "data", None) is not None:
                ev["source"] = self._ref(source)
            if isinstance(action, A.Damage) and target.type == CardType.HERO:
                # fireplace reports the whole hit and moves the absorbed part from health to armor
                after = int(target.armor)
                before = self._armor.get(target.entity_id, after)
                ev["armor_absorbed"] = max(0, min(int(amount), before - after))
                ev["armor_after"] = after
                self._armor[target.entity_id] = after
            self._emit(ev)
        elif isinstance(action, A.GainArmor):
            amount = args[0] if args else 0
            if amount and getattr(target, "type", None) == CardType.HERO:
                after = int(target.armor)
                self._armor[target.entity_id] = after
                ev = {
                    "event": "armor_gained",
                    "player": self.idx(target.controller),
                    "entity_id": target.entity_id,
                    "card_id": target.id,
                    "name": self._name(target),
                    "amount": int(amount),
                    "armor_after": after,
                }
                if source is not None and source is not target and getattr(source, "data", None) is not None:
                    ev["source"] = self._ref(source)
                self._emit(ev)
        elif isinstance(action, A.LosesDivineShield):
            # the shield absorbed a hit, which itself emits no damage event (0 damage)
            if getattr(target, "type", None) == CardType.MINION:
                self._emit_shield_lost(target)
        elif isinstance(action, A.Draw):
            card = args[0] if args else None
            if card is None:
                return
            k = self.idx(target)
            self._seen.add(card.entity_id)
            self._emit(
                {"event": "draw", "player": k, "card_id": card.id, "entity_id": card.entity_id},
                owner=k,
                public={"event": "draw", "player": k},
            )
        elif isinstance(action, A.Fatigue):
            self._emit({"event": "draw", "player": self.idx(target), "fatigue_damage": int(target.fatigue_counter)})
        elif isinstance(action, A.Summon):
            card = args[0] if args else None
            if card is not None and card.type == CardType.MINION and card.entity_id not in self._action_emitted:
                self._action_emitted.add(card.entity_id)
                self._emit(
                    {
                        "event": "summon",
                        "player": self.idx(card.controller),
                        "entity_id": card.entity_id,
                        "card_id": card.id,
                        "name": self._name(card),
                    }
                )

    def _emit_shield_lost(self, minion) -> None:
        self._shield_emitted.add(minion.entity_id)
        self._emit(
            {
                "event": "divine_shield_lost",
                "player": self.idx(minion.controller),
                "entity_id": minion.entity_id,
                "card_id": minion.id,
                "name": self._name(minion),
            }
        )

    # ------------------------------------------------------------------------------------------- end of game

    def _end(self, winner: int | None, reason: str) -> None:
        if self.over:
            return
        self.over = True
        self.winner = winner
        self.reason = reason
        self._emit({"event": "game_over", "winner": winner, "reason": reason})

    def _finish_from_engine(self) -> None:
        PlayState = self._PlayState
        s1, s2 = self._p[0].playstate, self._p[1].playstate
        if s1 == PlayState.WON and s2 != PlayState.WON:
            winner = 1
        elif s2 == PlayState.WON and s1 != PlayState.WON:
            winner = 2
        else:
            winner = None
        if winner is None:
            self._end(None, "draw")
        elif self._conceded is not None:
            self._end(winner, "concede")
        else:
            self._end(winner, "hero_death")

    def forfeit(self, loser: int, reason: str = "forfeit_illegal") -> None:
        self._end(3 - loser, reason)

    def void(self) -> None:
        self._end(None, "void_engine_error")

    def abort(self) -> None:
        self._end(None, "aborted")

    def result_for(self, i: int) -> dict[str, Any] | None:
        if not self.over:
            return None
        you_won = None if self.winner is None else (self.winner == i)
        return {"winner": self.winner, "you_won": you_won, "reason": self.reason}


def _strip_prefix(text: str, prefix: str) -> str:
    return text[len(prefix):] if text.startswith(prefix) else text


def _public_action(r: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for k, v in r.items():
        out[k] = getattr(v, "entity_id", v)
    return out
