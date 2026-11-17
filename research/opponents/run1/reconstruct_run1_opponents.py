"""Reconstruct visible opponent cards from the returned run archive; no games."""
import collections
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'run-1-results.zip'
DEST = Path(__file__).resolve().parent
CATALOG = {c['id']: c for c in json.loads((ROOT/'pkg/hs-arena-0.2.2/data/cards.json').read_text())['cards']}
CONFIG = {
    'bot2': ('opps_deck1-bot2-face-hunter', 'HUNTER', 'Bot 2 — Face Hunter'),
    'astra': ('opps_deck2-astra-zoo-warlock', 'WARLOCK', 'Astra — Zoo Warlock'),
}

def reconstruct():
    with zipfile.ZipFile(SOURCE) as z:
        payload = json.loads(z.read('games.json'))
        results_text = z.read('results.md').decode()
    assert payload['submission_number'] == 1
    output = {'source': SOURCE.name, 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'method': 'Distinct played entity IDs per game, plus publicly revealed secrets; per-card maximum across games. No hidden deck/order access.',
              'opponents': {}}
    for opponent, (folder, hero, title) in CONFIG.items():
        games = []
        lower = collections.Counter()
        for game in payload['games']:
            if game['opponent'] != opponent:
                continue
            plays = {}; secrets = []; classes = set(); evidence = collections.defaultdict(list)
            for obs in game['observations']:
                state = obs['state']
                if state.get('opponent'):
                    classes.add(state['opponent']['hero']['hero_class'])
                for event in state['events']:
                    if event.get('player') != 3-game['student_seat']:
                        continue
                    cid = event.get('card_id')
                    if cid not in CATALOG:
                        continue  # Coin and generated tokens are not starting-deck cards.
                    record = {'seq':state['seq'], 'turn_at_observation':state['turn'], 'event':event['event']}
                    if event['event'] == 'play_card' and event['entity_id'] not in plays:
                        plays[event['entity_id']] = cid
                        record['entity_id'] = event['entity_id']
                        evidence[cid].append(record)
                    elif event['event'] == 'secret_revealed':
                        secrets.append(cid); evidence[cid].append(record)
            assert classes == {hero}, (opponent, classes)
            counts = collections.Counter(plays.values())
            # Opposing secret play events hide the card. Reveals identify those slots.
            for cid, count in collections.Counter(secrets).items():
                counts[cid] = max(counts[cid], count)
            assert all(n <= (1 if CATALOG[c]['rarity']=='LEGENDARY' else 2) for c,n in counts.items())
            lower |= counts
            final = game['observations'][-1]['state']
            # Independent snapshot cross-check: these lists show no return/copy/resurrection cards.
            grave_board = collections.Counter(c['card_id'] for c in final['opponent']['graveyard']+final['opponent']['board'] if c['card_id'] in CATALOG)
            assert grave_board == counts, (game['game_id'],grave_board,counts)
            games.append({'game':opponent+'_'+game['game_id'].rsplit('_',1)[-1],
                          'game_id':game['game_id'],'student_outcome':game['outcome'],
                          'final_turn':final['turn'],'revealed_starting_cards':sum(counts.values()),
                          'opponent_deck_remaining':final['opponent']['deck_remaining'],
                          'opponent_hand_remaining':final['opponent']['hand_size'],
                          'counts':dict(counts),'evidence':dict(evidence),
                          'student_illegal_actions':game['illegal_actions'], 'student_timeouts':game['timeouts'],
                          'student_forfeit':game['student_forfeit'], 'finish_reason':game['finish_reason']})
        assert len(games)==4
        expected = 21 if opponent=='bot2' else 29
        assert sum(lower.values())==expected, lower
        proposed = collections.Counter({c:2 for c in lower}) if opponent=='bot2' else lower.copy()
        if opponent=='astra': proposed['EX1_029'] += 1
        assert sum(proposed.values())==30
        order = sorted(proposed, key=lambda c:(CATALOG[c]['cost'],CATALOG[c]['name']))
        deck = {'name':folder,'hero_class':hero,'cards':[c for c in order for _ in range(proposed[c])]}
        records = [{'card_id':c,'name':CATALOG[c]['name'],'cost':CATALOG[c]['cost'],
                    'observed_minimum':lower[c],'reconstructed_copies':proposed[c],
                    'inferred_copies':proposed[c]-lower[c],
                    'per_game_counts':[g['counts'].get(c,0) for g in games]} for c in order]
        info = {'hero_class':hero,'title':title,'folder':folder,'observed_slots':sum(lower.values()),
                'inferred_slots':30-sum(lower.values()),'exact_deck_known':False,
                'constant_deck_assumption':'All four games are compatible with this reconstruction; identical hidden lists cannot be proven.',
                'cards':records,'games':games}
        output['opponents'][opponent]=info
        dest=DEST/folder; dest.mkdir(exist_ok=True)
        (dest/'deck.json').write_text(json.dumps(deck,indent=2)+'\n')
        (dest/'evidence.json').write_text(json.dumps(info,indent=2)+'\n')
        lines=[f'# {title}', '', '**Status: legal 30-card hypothesis, not an exact recovered deck.**', '',
               f'Reconstructed from run 1 returned observations in `{SOURCE.name}`. Four games, all {hero}.',
               f'Public evidence confirms at least **{sum(lower.values())} slots** under a constant-list assumption; **{30-sum(lower.values())} slots are inferred**.', '',
               'Use `deck.json` for local opponent testing. `evidence.json` records per-game counts and observation seq/entity evidence. This folder is a deck recipe, not a model skill.', '',
               '| Card | Mana | G1 | G2 | G3 | G4 | Observed minimum | Reconstructed | Inferred |',
               '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for r in records:
            lines.append('| '+ ' | '.join(map(str,[r['name'],r['cost'],*r['per_game_counts'],r['observed_minimum'],r['reconstructed_copies'],r['inferred_copies']]))+' |')
        lines += ['', 'Counts are distinct played cards, not repeated board sightings. Revealed Explosive Traps are included. The Coin, Hounds, Animal Companions, Damaged Golems and Imp tokens are excluded. Final graveyard/board counts independently match the identified starting cards in every game.', '',
                  'A maximum of one observed copy does **not** prove the card is a singleton. Maxima are taken across games, never summed across games. The unseen deck and opponent hand are absent from the archive.', '']
        if opponent=='bot2':
            lines += ['## Reconstruction choice', '',
                      'Fifteen distinct card names were observed. Two copies of each make a simple legal Face Hunter list consistent with all four games, without inventing an unseen card name. Only six names have their second copy directly confirmed. Nine second copies remain guesses: Abusive Sergeant, Argent Squire, Worgen Infiltrator, Bluegill Warrior, Explosive Trap, Eaglehorn Bow, Kill Command, Unleash the Hounds and Wolfrider.', '',
                      'Other completions could replace any inferred second copy with an unseen legal card. Four short games do not distinguish them. Do not treat this list as an exact clone.', '',
                      '## Playing pattern and matchup', '',
                      'Low-cost attackers establish pressure; Charge minions, Bow, burn and Steady Shot finish. Timber Wolf supports Hounds/Beasts, Juggler rewards summons, and Owl bypasses Taunts. No Highmane or other expensive finisher was revealed. That does not prove absence.', '',
                      'The opponent ended all four games with an empty hand and 16–18 cards still in its deck. This supports a limited-refill pressure plan. Our Control Paladin won all four; healing, Taunts and clears can exhaust the early attack. The pilot also used some Kill Commands/Arcane Shots on minions, so the result measures that pilot plus its list.', '']
        else:
            lines += ['## Reconstruction choice', '',
                      'Sixteen distinct card names were observed: thirteen confirmed pairs and one observed copy each of Leper Gnome, Mortal Coil and Imp Master. This fixes 29 slots if the list stayed constant. The thirtieth card is unknown.', '',
                      'The playable hypothesis uses a second Leper Gnome to support the aggressive curve and deathrattle reach. A second Mortal Coil, a second Imp Master, or an entirely unseen legal card also fits. No replay evidence establishes that Leper Gnome is more likely than those alternatives.', '',
                      'In game 1, 28 original cards were revealed, with no cards in hand and two left in the deck. Game 2 confirms the second Loot Hoarder, leaving exactly one unresolved slot across the combined evidence. Soulfire discards and unobserved cards are not assigned invented identities.', '',
                      '## Playing pattern and matchup', '',
                      'This is low-curve Zoo, not our Infernal Warlock or the earlier local Steady Paladin experiment. Flame Imp and cheap bodies contest the board; Abusive Sergeant, Dire Wolf, Cleric and Dark Iron Dwarf turn small minions into trades or damage. Argus protects a wide board, Harvest Golem/Imp Master supply bodies, and Life Tap/Loot Hoarder sustain pressure. Soulfire adds reach.', '',
                      'Our Control Paladin split 2–2. The fourth game ended on turn 11 after Dark Iron Dwarf buffed Flame Imp and Soulfire targeted our hero. Unlike Bot 2, this list can refill rather than simply exhausting its opening hand. The near-complete evidence leaves no space for a large hidden late-game package under a constant-list assumption.', '']
        (dest/'reconstruction.md').write_text('\n'.join(lines))
    DEST.mkdir(exist_ok=True)
    (DEST/'evidence.json').write_text(json.dumps(output,indent=2)+'\n')
    (DEST/'official-results.md').write_text(results_text)
    print(json.dumps({k:{'observed':v['observed_slots'],'inferred':v['inferred_slots'],'folder':v['folder']} for k,v in output['opponents'].items()},indent=2))

if __name__=='__main__': reconstruct()
