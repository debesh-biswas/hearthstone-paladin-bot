"""Offline protocol and tactical regression tests; never launches a match."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('pilot', ROOT/'decks/burst-shaman/scripts/move.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

def unit(eid, cid='CS2_182', attack=4, health=5, **kw):
    return dict(entity_id=eid, card_id=cid, attack=attack, health=health,
                max_health=health, can_attack=False, **kw)

def state(hero='SHAMAN', mana=10):
    def side(eid, hc):
        return dict(hero=unit(eid, 'HERO', 0, 30, hero_class=hc, armor=0),
                    board=[], hand=[], weapon=None, mana=mana, max_mana=10,
                    hero_power=dict(card_id='HERO_02bp', cost=2, usable=False),
                    hand_size=4, secrets_count=0, secrets=[], deck_remaining=15,
                    deck_remaining_counts={}, fatigue=0)
    return dict(seq=1, phase='main', turn=9, player=1, you=side(1,hero),
                opponent=side(2,'PALADIN'), events=[dict(event='turn_start',turn=9,player=1)],
                legal_actions=[dict(type='end_turn')])

def card(s, eid, cid, targets=None, positions=None):
    c=dict(p.CATALOG[cid],card_id=cid,entity_id=eid)
    s['you']['hand'].append(c)
    if c['cost']<=s['you']['mana']:
        s['legal_actions'].insert(0,dict(type='play_card',card=eid,targets=targets,positions=positions,choose=None))
    return c

class PilotTests(unittest.TestCase):
    def test_target_and_position_cartesian(self):
        t=dict(type='play_card',card=5,targets=[1,2],positions=[0,1],choose=None)
        acts=p.expand([t])
        self.assertEqual(len(acts),4)
        self.assertTrue(all(p.allowed(a,[t]) for a in acts))
        self.assertFalse(p.allowed(dict(type='play_card',card=5),[t]))
        self.assertFalse(p.allowed(dict(type='play_card',card=5,target=1,position=9),[t]))
    def test_rockbiter_before_doomhammer_attacks(self):
        s=state(); s['opponent']['hero']['health']=10
        s['you']['weapon']=dict(card_id='EX1_567',attack=2,durability=8)
        s['you']['hero'].update(attack=2,can_attack=True)
        s['legal_actions'].append(dict(type='attack',attacker=1,targets=[2]))
        card(s,10,'CS2_045',[1])
        self.assertEqual(p.decide(s),dict(type='play_card',card=10,target=1))
    def test_no_false_windfury_after_first_swing(self):
        s=state(); s['opponent']['hero']['health']=10
        s['you']['weapon']=dict(card_id='EX1_567',attack=2,durability=7)
        s['you']['hero'].update(attack=2,can_attack=True)
        s['events'].append(dict(event='attack',player=1,attacker=dict(entity_id=1)))
        s['legal_actions'].append(dict(type='attack',attacker=1,targets=[2]))
        card(s,10,'CS2_045',[1])
        self.assertIsNone(p.lethal(s,p.expand(s['legal_actions'])))
    def test_jaraxxus_not_played_into_visible_death(self):
        s=state('WARLOCK'); s['opponent']['board']=[unit(3,attack=16)]
        card(s,10,'EX1_323',positions=[0])
        self.assertNotEqual(p.decide(s).get('card'),10)
    def test_farseer_heals_own_hero(self):
        s=state('WARLOCK'); s['you']['hero']['health']=8
        card(s,10,'CS2_117',[1,2],positions=[0])
        self.assertEqual(p.decide(s).get('target'),1)
    def test_inferno_not_life_tap(self):
        s=state('WARLOCK'); s['you']['hero_power']['card_id']='EX1_tk33'
        s['you']['hero_power']['usable']=True; s['you']['hero']['health']=3
        s['legal_actions'].append(dict(type='hero_power',targets=None))
        self.assertEqual(p.decide(s)['type'],'hero_power')
    def test_kill_command_requires_beast(self):
        s=state('HUNTER',3); s['opponent']['hero']['health']=5
        card(s,10,'EX1_539',[2])
        self.assertIsNone(p.lethal(s,p.expand(s['legal_actions'])))
        s['you']['board']=[unit(4,'CS2_120',2,3)]
        self.assertEqual(p.lethal(s,p.expand(s['legal_actions']))['card'],10)
    def test_hellfire_does_not_suicide(self):
        s=state('WARLOCK'); s['you']['hero']['health']=3
        s['opponent']['board']=[unit(i,attack=3,health=3) for i in range(3,7)]
        card(s,10,'CS2_062')
        self.assertEqual(p.decide(s)['type'],'end_turn')
    def test_choice_bounds(self):
        s=state('HUNTER'); s['phase']='choice'
        s['legal_actions']=[dict(type='choose',min=1,max=1,options=[dict(p.CATALOG['EX1_539'],card_id='EX1_539',entity_id=10),dict(p.CATALOG['DS1_175'],card_id='DS1_175',entity_id=11)])]
        self.assertTrue(p.allowed(p.decide(s),s['legal_actions']))
    def test_weapon_replacement_does_not_refresh_attacks(self):
        s=state(); s['opponent']['hero']['health']=5
        s['you']['weapon']=dict(card_id='EX1_567',attack=2,durability=8)
        s['you']['hero'].update(attack=2,can_attack=True)
        s['legal_actions'].append(dict(type='attack',attacker=1,targets=[2]))
        card(s,10,'EX1_567')
        self.assertIsNone(p.lethal(s,p.expand(s['legal_actions'])))
    def test_unknown_history_uses_one_existing_windfury_swing(self):
        s=state(); s['events']=[]; s['opponent']['hero']['health']=4
        s['you']['weapon']=dict(card_id='EX1_567',attack=2,durability=7)
        s['you']['hero'].update(attack=2,can_attack=True)
        s['legal_actions'].append(dict(type='attack',attacker=1,targets=[2]))
        self.assertIsNone(p.lethal(s,p.expand(s['legal_actions'])))
    def test_owl_opens_taunt_for_lethal(self):
        s=state('HUNTER'); s['opponent']['hero']['health']=4
        s['you']['board']=[unit(4,attack=4)]
        s['you']['board'][0]['can_attack']=True
        s['opponent']['board']=[unit(3,'EX1_383',6,6,taunt=True,divine_shield=True)]
        s['legal_actions'].append(dict(type='attack',attacker=4,targets=[3]))
        card(s,10,'CS2_203',[3,4],positions=[0,1])
        self.assertEqual(p.lethal(s,p.expand(s['legal_actions'])),dict(type='play_card',card=10,target=3,position=1))
    def test_shadowflame_uses_donor_face_attack_first(self):
        s=state('WARLOCK'); s['you']['board']=[unit(4,attack=8,health=8)]
        s['you']['board'][0]['can_attack']=True
        s['opponent']['board']=[unit(i,attack=6,health=6) for i in (3,5,6)]
        s['legal_actions'].append(dict(type='attack',attacker=4,targets=[2,3,5,6]))
        card(s,10,'EX1_303',[4])
        self.assertEqual(p.decide(s),dict(type='attack',attacker=4,target=2))
    def test_tracking_selection_requires_card_ids_in_bounds(self):
        t=dict(type='play_card',card=5,targets=None,positions=None,choose=[dict(entity_id=9,targets=[1]),dict(entity_id=10,targets=None)])
        self.assertFalse(p.allowed(dict(type='play_card',card=5,choose=10,target=1),[t]))
        self.assertTrue(p.allowed(dict(type='play_card',card=5,choose=9,target=1),[t]))
    def test_no_lethal_claim_through_secret_or_immune(self):
        s=state('HUNTER'); s['opponent']['hero']['health']=2
        card(s,10,'DS1_185',[2]); s['opponent']['secrets_count']=1
        self.assertIsNone(p.lethal(s,p.expand(s['legal_actions'])))
        s['opponent']['secrets_count']=0; s['opponent']['hero']['immune']=True
        self.assertIsNone(p.lethal(s,p.expand(s['legal_actions'])))
    def test_life_tap_avoids_fatigue_death(self):
        s=state('WARLOCK'); s['you']['hero']['health']=6
        s['you']['deck_remaining']=0; s['you']['fatigue']=4
        s['legal_actions'].append(dict(type='hero_power',targets=None))
        self.assertEqual(p.decide(s)['type'],'end_turn')
    def test_argus_position_protects_two_minions(self):
        s=state('WARLOCK'); s['you']['board']=[unit(3),unit(4)]
        card(s,10,'EX1_093',positions=[0,1,2])
        self.assertEqual(p.decide(s).get('position'),1)
    def test_mulligan_returns_slow_combo(self):
        s=state(); s['phase']='mulligan'
        card(s,10,'EX1_567'); card(s,11,'CS2_045',[1]); card(s,12,'EX1_008',positions=[0])
        s['legal_actions']=[dict(type='mulligan',options=[10,11,12],min=0,max=3)]
        self.assertEqual(p.decide(s)['replace'],[10,11])
    def test_each_deck_card_has_finite_scores(self):
        import math
        for name in ('burst-shaman','infernal-warlock','pressure-hunter'):
            d=json.loads((ROOT/'decks'/name/'deck.json').read_text())
            for cid in set(d['cards']):
                s=state(d['hero_class']); s['you']['board']=[unit(3,'CS2_120',2,3)]
                s['opponent']['board']=[unit(4,'EX1_383',6,6,taunt=True,divine_shield=True)]
                targeted=cid in {'EX1_238','EX1_241','EX1_245','EX1_246','CS2_045','CS2_117','CS2_042','CS2_203','EX1_302','EX1_303','EX1_309','DS1_070','EX1_539','DS1_185'}
                card(s,10,cid,[1,2,3,4] if targeted else None,[0,1] if p.CATALOG[cid]['type']=='MINION' else None)
                for a in p.expand(s['legal_actions']):
                    self.assertTrue(math.isfinite(p.score(s,a)),(name,cid,a))
    def test_cli_is_self_contained_and_blocks_external_state_path(self):
        import os
        import shutil
        import subprocess
        import sys
        import tempfile
        for name in ('burst-shaman','infernal-warlock','pressure-hunter'):
            with tempfile.TemporaryDirectory() as tmp:
                dest=Path(tmp)/name;shutil.copytree(ROOT/'decks'/name,dest)
                (dest/'game').mkdir()
                (dest/'game/state.json').write_text(json.dumps(dict(seq=7,phase='deck_submission')))
                env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
                result=subprocess.run([sys.executable,str(dest/'scripts/move.py')],cwd=tmp,env=env,capture_output=True,text=True,check=True)
                out=json.loads(result.stdout)
                self.assertEqual(out['seq'],7);self.assertEqual(len(out['action']['cards']),30)
                outside=Path(tmp)/'outside.json';outside.write_text('{}')
                result=subprocess.run([sys.executable,str(dest/'scripts/move.py'),str(outside)],cwd=tmp,env=env,capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('inside this skill workspace',result.stderr)
    def test_submission_each_canonical_deck(self):
        for name in ('burst-shaman','infernal-warlock','pressure-hunter'):
            old=p.ROOT
            try:
                p.ROOT=ROOT/'decks'/name
                a=p.decide(dict(phase='deck_submission',legal_actions=[dict(type='submit_deck')]))
                self.assertEqual(len(a['cards']),30)
                self.assertEqual(a['cards'],json.loads((p.ROOT/'deck.json').read_text())['cards'])
            finally: p.ROOT=old

if __name__=='__main__': unittest.main()
