"""Deterministic text rendering of states and events (no LLM involved). Shared with the replay renderer."""

from __future__ import annotations

from typing import Any, Callable

_catalog_cache: dict[str, Any] | None = None


def _catalog() -> dict[str, Any]:
    global _catalog_cache
    if _catalog_cache is None:
        try:
            from .. import cards

            _catalog_cache = cards.load()
        except Exception:
            _catalog_cache = {}
    return _catalog_cache


def _card_name(card_id: str | None) -> str:
    if not card_id:
        return "?"
    c = _catalog().get(card_id)
    return c["name"] if c else card_id


# keywords a minion can lose without being silenced: the printed text keeps them, so say when they are gone
_LOSABLE_KEYWORDS = (("DIVINE_SHIELD", "divine_shield", "Divine Shield"), ("STEALTH", "stealth", "Stealth"))


def _lost_keywords(m: dict[str, Any]) -> list[str]:
    mechanics = (_catalog().get(m.get("card_id") or "") or {}).get("mechanics") or []
    return [label for mech, flag, label in _LOSABLE_KEYWORDS if mech in mechanics and not m.get(flag)]


def _ref(r: dict[str, Any] | None) -> str:
    if not r:
        return "nothing"
    return f"{r.get('name', '?')} #{r.get('entity_id', '?')}"


def event_text(ev: dict[str, Any], who: Callable[[int | None], str]) -> str:
    """One line for an event. `who(player_index)` names a player ('You', 'Opponent', 'P1', ...)."""
    e = ev.get("event")
    p = who(ev.get("player"))
    if e == "deck_submitted":
        return f"{p} submitted and locked a deck."
    if e == "game_start":
        return f"Game start: {who(ev.get('first_player'))} goes first."
    if e == "turn_start":
        return f"--- Turn {ev.get('turn')}: {p} ---"
    if e == "draw":
        if ev.get("fatigue_damage"):
            return f"{p} has no cards left and takes {ev['fatigue_damage']} fatigue damage."
        if ev.get("card_id"):
            return f"{p} draws {_card_name(ev['card_id'])} #{ev.get('entity_id', '?')}."
        return f"{p} draws a card."
    if e == "mulligan":
        s = f"{p} mulligans {ev.get('replaced', 0)} card(s)"
        if "replaced_card_ids" in ev:
            out = ", ".join(_card_name(c) for c in ev["replaced_card_ids"]) or "-"
            new = ", ".join(_card_name(c) for c in ev.get("drawn_card_ids", [])) or "-"
            s += f" (out: {out}; in: {new})"
        return s + "."
    if e == "play_card":
        s = f"{p} plays {ev.get('name')} #{ev.get('entity_id')}"
        if ev.get("choose"):
            s += f" choosing {ev['choose'].get('name')}"
        if ev.get("target"):
            s += f" targeting {_ref(ev['target'])}"
        if ev.get("position") is not None:
            s += f" at position {ev['position']}"
        return s + "."
    if e == "choose":
        return f"{p} chooses {ev['name']}." if ev.get("name") else f"{p} makes a choice."
    if e == "hero_power":
        s = f"{p} uses {ev.get('name', 'the hero power')}"
        if ev.get("target"):
            s += f" on {_ref(ev['target'])}"
        return s + "."
    if e == "attack":
        return f"{p}: {_ref(ev.get('attacker'))} attacks {_ref(ev.get('target'))}."
    if e in ("damage", "heal"):
        verb = "takes" if e == "damage" else "is healed for"
        s = f"{ev.get('name')} #{ev.get('entity_id')} ({who(ev.get('player'))}) {verb} {ev.get('amount')}"
        if e == "damage":
            s += " damage"
        if ev.get("source"):
            s += f" from {_ref(ev['source'])}"
        if ev.get("armor_absorbed"):
            s += f" ({ev['armor_absorbed']} absorbed by armor)"
        s += f", health {ev.get('health_after')}"
        if ev.get("armor_after") or ev.get("armor_absorbed"):
            s += f", armor {ev.get('armor_after', 0)}"
        return s + "."
    if e == "armor_gained":
        s = f"{ev.get('name')} #{ev.get('entity_id')} ({p}) gains {ev.get('amount')} armor"
        if ev.get("source"):
            s += f" from {_ref(ev['source'])}"
        return s + f", armor {ev.get('armor_after')}."
    if e == "summon":
        return f"{p} summons {ev.get('name')} #{ev.get('entity_id')}."
    if e == "death":
        return f"{ev.get('name')} #{ev.get('entity_id')} ({p}) dies."
    if e == "divine_shield_lost":
        return f"{ev.get('name')} #{ev.get('entity_id')} ({p}) loses Divine Shield."
    if e == "leave_board":
        return f"{ev.get('name')} #{ev.get('entity_id')} leaves {p}'s board."
    if e == "secret_played":
        return f"{p} puts {ev['name']} into play as a secret." if ev.get("name") else f"{p} plays a secret."
    if e == "secret_revealed":
        return f"{p}'s secret {ev.get('name') or _card_name(ev.get('card_id'))} is revealed."
    if e == "weapon_equipped":
        return f"{p} equips {ev.get('name')} ({ev.get('attack')}/{ev.get('durability')})."
    if e == "weapon_destroyed":
        return f"{p}'s weapon {ev.get('name')} is destroyed."
    if e == "end_turn":
        return f"{p} ends the turn."
    if e == "illegal_action":
        return f"{p}: illegal action {ev.get('error')} (illegal count {ev.get('illegal_count')})."
    if e == "agent_failure":
        return f"{p}: {ev.get('error')}; game forfeited."
    if e == "agent_restart":
        return f"{p}'s agent was restarted (restart #{ev.get('restart_count')})."
    if e == "game_over":
        w = ev.get("winner")
        return f"Game over: {who(w) + ' wins' if w else 'no winner'} ({ev.get('reason')})."
    return f"{e}: {ev}"


# ----------------------------------------------------------------------------------------------- state


def _flags(m: dict[str, Any]) -> str:
    names = [
        ("taunt", "taunt"),
        ("divine_shield", "divine shield"),
        ("stealth", "stealth"),
        ("windfury", "windfury"),
        ("charge", "charge"),
        ("poisonous", "poisonous"),
        ("frozen", "frozen"),
        ("silenced", "silenced"),
        ("deathrattle", "deathrattle"),
    ]
    out = [label for key, label in names if m.get(key)]
    if m.get("spell_damage"):
        out.append(f"spell damage +{m['spell_damage']}")
    if m.get("can_attack"):
        out.append("can attack")
    return (" [" + ", ".join(out) + "]") if out else ""


def _hero_line(label: str, side: dict[str, Any]) -> str:
    h = side["hero"]
    s = f"{label}: {h['name']} ({h.get('hero_class', '?')}) #{h['entity_id']} health {h['health']}"
    if h.get("armor"):
        s += f" armor {h['armor']}"
    if h.get("attack"):
        s += f" attack {h['attack']}"
    flags = [k for k in ("frozen", "immune") if h.get(k)]
    if h.get("can_attack"):
        flags.append("can attack")
    if flags:
        s += " [" + ", ".join(flags) + "]"
    return s


def _side_lines(side: dict[str, Any], own: bool) -> list[str]:
    lines = []
    hp = side.get("hero_power")
    if hp:
        usable = " usable" if hp.get("usable") else ""
        lines.append(f"  hero power: {hp['name']} #{hp['entity_id']} ({hp['cost']} mana){usable} - {hp.get('text', '')}")
    w = side.get("weapon")
    if w:
        lines.append(f"  weapon: {w['name']} #{w['entity_id']} {w['attack']}/{w['durability']}")
    # the opponent never has spendable mana while you decide: show their crystals only
    mana = f"  mana {side['mana']}/{side['max_mana']}" if own else f"  mana crystals {side['max_mana']}"
    if side.get("overloaded"):
        mana += f" (overloaded {side['overloaded']})"
    if side.get("overload_next_turn"):
        mana += f" (overload next turn {side['overload_next_turn']})"
    if own:
        mana += f" | deck {side['deck_remaining']} | fatigue {side['fatigue']}"
    else:
        mana += (
            f" | hand {side['hand_size']} | deck {side['deck_remaining']} | secrets {side['secrets_count']}"
            f" | fatigue {side['fatigue']}"
        )
    lines.append(mana)
    board = side.get("board") or []
    lines.append("  board:" + ("" if board else " (empty)"))
    for k, m in enumerate(board):
        text = f" - {m['text']}" if m.get("text") else ""
        if m.get("silenced") and m.get("text"):
            text = f" - silenced; original text (no longer active): {m['text']}"
        elif m.get("text") and _lost_keywords(m):
            text += f" ({', '.join(_lost_keywords(m))} already lost)"
        lines.append(f"    [{k}] #{m['entity_id']} {m['name']} {m['attack']}/{m['health']}{_flags(m)}{text}")
    if own:
        hand = side.get("hand") or []
        lines.append("  hand:" + ("" if hand else " (empty)"))
        for c in hand:
            stats = ""
            if c["type"] == "MINION":
                stats = f" {c.get('attack')}/{c.get('health')}"
            elif c["type"] == "WEAPON":
                stats = f" {c.get('attack')}/{c.get('durability')}"
            playable = " [playable]" if c.get("playable") else ""
            text = f" - {c['text']}" if c.get("text") else ""
            lines.append(f"    #{c['entity_id']} {c['name']} ({c['cost']} mana {c['type'].lower()}{stats}){playable}{text}")
        secrets = side.get("secrets") or []
        if secrets:
            lines.append("  secrets: " + ", ".join(f"#{s['entity_id']} {s['name']}" for s in secrets))
    if side.get("graveyard"):
        lines.append("  graveyard: " + ", ".join(c["name"] if isinstance(c, dict) else _card_name(c) for c in side["graveyard"]))
    return lines


def _labels(state: dict[str, Any]) -> dict[int, str]:
    labels: dict[int, str] = {}
    you, opp = state["you"], state["opponent"]
    labels[you["hero"]["entity_id"]] = "your hero"
    labels[opp["hero"]["entity_id"]] = "enemy hero"
    for m in you.get("board") or []:
        labels[m["entity_id"]] = f"your {m['name']} {m['attack']}/{m['health']}"
    for m in opp.get("board") or []:
        labels[m["entity_id"]] = f"enemy {m['name']} {m['attack']}/{m['health']}"
    return labels


def _targets(ids, labels) -> str:
    return "{" + ", ".join(f"#{x} {labels.get(x, '?')}" for x in ids) + "}"


def legal_action_lines(state: dict[str, Any]) -> list[str]:
    if state["phase"] == "deck_submission":
        return ["1. submit_deck hero_class=<class> cards=[30 card ids]", "2. concede"]
    if state["you"] is None:
        return []
    labels = _labels(state)
    hand = {c["entity_id"]: c for c in state["you"].get("hand") or []}
    own_board = {m["entity_id"]: m for m in state["you"].get("board") or []}
    lines = []
    for n, t in enumerate(state.get("legal_actions") or [], 1):
        tt = t["type"]
        if tt == "play_card":
            c = hand.get(t["card"], {})
            s = f"play_card card={t['card']} ({c.get('name', '?')}, {c.get('cost', '?')} mana)"
            if t.get("positions") is not None:
                s += f" position in {t['positions']} (default rightmost)"
            if t.get("targets") is not None:
                s += f" target in {_targets(t['targets'], labels)}"
            elif not t.get("choose"):
                s += " (no target)"
            lines.append(f"{n}. {s}")
            for o in t.get("choose") or []:
                os_ = f"     choose={o['entity_id']} ({o['name']}: {o.get('text', '')})"
                if o.get("targets") is not None:
                    os_ += f" target in {_targets(o['targets'], labels)}"
                lines.append(os_)
        elif tt == "attack":
            a = t["attacker"]
            name = labels.get(a) or (own_board.get(a, {}).get("name", "?"))
            lines.append(f"{n}. attack attacker={a} ({name}) target in {_targets(t['targets'], labels)}")
        elif tt == "hero_power":
            hp = state["you"].get("hero_power") or {}
            s = f"hero_power ({hp.get('name', '?')}, {hp.get('cost', '?')} mana)"
            if t.get("targets") is not None:
                s += f" target in {_targets(t['targets'], labels)}"
            elif not t.get("choose"):
                s += " (no target)"
            lines.append(f"{n}. {s}")
            for o in t.get("choose") or []:
                os_ = f"     choose={o['entity_id']} ({o['name']}: {o.get('text', '')})"
                if o.get("targets") is not None:
                    os_ += f" target in {_targets(o['targets'], labels)}"
                lines.append(os_)
        elif tt == "mulligan":
            opts = ", ".join(f"#{x} {hand.get(x, {}).get('name', '?')}" for x in t["options"])
            lines.append(f"{n}. mulligan replace = any subset of {{{opts}}} ({t['min']}..{t['max']} cards)")
        elif tt == "choose":
            lines.append(f"{n}. choose options = pick {t['min']}..{t['max']} of:")
            for o in t["options"]:
                stats = f" {o['attack']}/{o['health']}" if "attack" in o and "health" in o else ""
                cost = f"{o['cost']} mana " if "cost" in o else ""
                lines.append(f"     #{o['entity_id']} {o['name']} ({cost}{o.get('type', '').lower()}{stats}) - {o.get('text', '')}")
        else:
            lines.append(f"{n}. {tt}")
    return lines


def state_to_text(state: dict[str, Any]) -> str:
    """Compact deterministic rendering of a state.json (wall-clock time does not enter the text)."""
    me = state["player"]

    def who(i):
        if i is None:
            return "nobody"
        return f"P{i} (you)" if i == me else f"P{i} (opponent)"

    lines = [
        f"Game {state['game_id']} | seq {state['seq']} | turn {state['turn']} | you are player {me} | phase {state['phase']}",
    ]
    if state["phase"] == "game_over":  # timeout_s / deadline are the exit grace here, not a decision deadline
        lines.append("The game is over; no action is expected.")
    else:
        lines.append(f"Answer within {state['timeout_s']:g} s (deadline_epoch_s {state['deadline_epoch_s']}).")
    lr = state.get("last_action_result")
    if lr and not lr.get("accepted", False):
        lines.append(
            f"YOUR LAST ACTION WAS REJECTED: {lr.get('error')} - {lr.get('message')} "
            f"(illegal actions {lr.get('illegal_count')}/{lr.get('illegal_limit')}; reaching the limit forfeits the game)"
        )
    if state.get("result"):
        r = state["result"]
        outcome = {True: "you won", False: "you lost"}.get(r.get("you_won"), "no winner")
        lines.append(f"RESULT: winner {r.get('winner')} ({outcome}), reason {r.get('reason')}")
    if state.get("choice"):
        ch = state["choice"]
        src = f" from {ch['source']['name']}" if ch.get("source") else ""
        lines.append(f"Pending choice: {ch.get('kind')}{src}")
    lines.append("")
    if state["phase"] == "deck_submission":
        rules = state["deck_rules"]
        lines += ["DECK SUBMISSION: choose your hero class and submit a legal 30-card deck now.",
                  "Both seats build independently; the opponent's class and deck are hidden until play begins.",
                  f"Classes: {', '.join(rules['hero_classes'])}. Pool: {rules['pool_version']}.",
                  f"Exactly {rules['deck_size']} cards; same class or NEUTRAL; max {rules['max_copies']} copies, "
                  f"max {rules['max_legendary_copies']} per Legendary; no blacklisted cards.",
                  "Read game/card_pool.json for the allowed cards (including cost, stats and text).",
                  'Use act(seq, {"type":"submit_deck","hero_class":"MAGE","cards":[...30 card ids...]}).',
                  "You may build dynamically or randomly following your skill; deck.json is just an optional recipe.",
                  "Once accepted, your class and deck are fixed for this game; you cannot resubmit during play."]
    elif state["you"] is not None:
        lines.append(_hero_line("OPPONENT", state["opponent"]))
        lines += _side_lines(state["opponent"], own=False)
        lines.append(_hero_line("YOU", state["you"]))
        lines += _side_lines(state["you"], own=True)
    else:
        lines.append("The game ended before both decks were accepted; no board was created.")
    events = state.get("events") or []
    lines.append("")
    lines.append("EVENTS since your previous state:" + ("" if events else " (none)"))
    for ev in events:
        lines.append("  " + event_text(ev, who))
    legal = legal_action_lines(state)
    lines.append("")
    lines.append("LEGAL ACTIONS:" + ("" if legal else " (none)"))
    lines += ["  " + x for x in legal]
    return "\n".join(lines)
