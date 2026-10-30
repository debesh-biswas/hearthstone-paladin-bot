"""Public-state pilot for the three research decks; no engine, network or hidden state.

Uses the existing player's decide(state)/JSON relay interface. Unlike its Paladin-only
board simulator, this uses exact legal root actions, bounded face-combo search and
explicit card heuristics. It replans after every actual action. Heuristics are uncalibrated.
"""
import copy
import itertools
import json
import sys
from pathlib import Path
from hs_arena.cards import load

ROOT = Path(__file__).resolve().parent.parent
CATALOG = load()
# Race is not included in the public minion schema or the arena card catalog.
BEASTS = {'CS2_120','EX1_531','CS2_203','EX1_028','EX1_534','EX1_534t',
          'EX1_538t','NEW1_032','NEW1_033','NEW1_034','DS1_175','CS2_171','CS2_172',
          'CS2_237','DS1_178','EX1_543'}
OVERLOAD = {'EX1_238':1,'EX1_241':2,'EX1_259':2,'EX1_248':2,'EX1_567':2}
DIRECT = {'EX1_238':3,'EX1_241':5,'DS1_185':2,'EX1_539':3}
KEEP = {
 'SHAMAN':{'EX1_008','EX1_010','EX1_096','EX1_238'},
 'WARLOCK':{'CS2_065','NEW1_021','EX1_058','EX1_066'},
 'HUNTER':{'EX1_008','EX1_010','CS2_120','EX1_531','EX1_096'},
}


def expand(templates):
    """Concrete main-phase moves; target/position/Choose One combinations stay coupled."""
    out=[]
    for t in templates:
        kind=t['type']
        if kind=='end_turn': out.append({'type':kind})
        elif kind=='attack':
            out.extend(dict(type=kind,attacker=t['attacker'],target=x) for x in t['targets'])
        elif kind in ('play_card','hero_power'):
            for opt in t.get('choose') or [None]:
                base={'type':kind}
                if kind=='play_card': base['card']=t['card']
                if opt: base['choose']=opt['entity_id']
                targets=opt.get('targets') if opt else t.get('targets')
                positions=t.get('positions')
                for target,pos in itertools.product(targets if targets is not None else [None],
                                                     positions if positions is not None else [None]):
                    a=dict(base)
                    if target is not None: a['target']=target
                    if pos is not None: a['position']=pos
                    out.append(a)
    return out


def allowed(action, templates):
    if action.get('type')=='mulligan':
        return any(t['type']=='mulligan' and len(set(action['replace']))==len(action['replace'])
                   and set(action['replace'])<=set(t['options'])
                   and t.get('min',0)<=len(action['replace'])<=t.get('max',len(t['options'])) for t in templates)
    if action.get('type')=='choose':
        return any(t['type']=='choose' and len(set(action['options']))==len(action['options'])
                   and set(action['options'])<={o['entity_id'] for o in t['options']}
                   and t['min']<=len(action['options'])<=t['max'] for t in templates)
    return action in expand(templates)


def beast(m): return m.get('card_id') in BEASTS

def hp(hero): return hero['health']+hero.get('armor',0)

def value(m):
    v=m.get('attack',0)+0.65*m.get('health',0)
    v+=1.5*bool(m.get('taunt'))+2*bool(m.get('divine_shield'))
    v+=0.5*m.get('attack',0)*bool(m.get('windfury'))
    if not m.get('silenced'):
        v+= {'EX1_556':2,'EX1_534':4,'EX1_110':4,'EX1_383':6,
             'NEW1_019':3,'EX1_575':4,'EX1_608':3,'EX1_531':2}.get(m.get('card_id'),0)
    return v


def threat(s):
    # Conservative upper estimate: do not subtract Taunt health as if it always absorbs attacks.
    e=s['opponent']
    return sum(m.get('attack',0)*(2 if m.get('windfury') else 1)
               for m in e['board'] if not m.get('frozen'))+(e.get('weapon') or {}).get('attack',0)


def attack_counts(s):
    """Only a visible current-turn boundary proves how many Windfury swings remain."""
    counts={}; known=False
    for e in s.get('_history_events',s.get('events',[])):
        if e.get('event')=='turn_start':
            known=e.get('turn')==s.get('turn') and e.get('player')==s.get('player')
            counts={}
        elif known and e.get('event')=='attack' and e.get('player')==s.get('player'):
            eid=e['attacker']['entity_id']; counts[eid]=counts.get(eid,0)+1
    return known,counts


def hero_bonus(y):
    return max(0,y['hero']['attack']-(y.get('weapon') or {}).get('attack',0))


def lethal(s, actions):
    """Conservative bounded search of face attacks, burn, buffs and enabling cards.

    No guessed draws, random outcomes, minion trades or secret resolution. A found line
    is a tactical estimate from visible information, not a complete engine proof.
    """
    if s['opponent']['hero'].get('immune') or s['opponent'].get('secrets_count',0): return None
    y=s['you']; oh=y['hero']['entity_id']; eh=s['opponent']['hero']['entity_id']
    known,counts=attack_counts(s)
    attackers={}
    for m in y['board']:
        cap=2 if m.get('windfury') else 1
        left=max(0,cap-counts.get(m['entity_id'],0)) if known else 1
        attackers[m['entity_id']]=[m['attack'],left if m.get('can_attack') and not m.get('frozen') else 0]
    weapon=y.get('weapon'); cap=2 if weapon and weapon['card_id']=='EX1_567' else 1
    left=max(0,cap-counts.get(oh,0)) if known else 1
    attackers[oh]=[y['hero']['attack'],min(left,(weapon or {}).get('durability',left)) if y['hero'].get('can_attack') and not y['hero'].get('frozen') else 0]
    root=dict(mana=y['mana'],damage=0,hand=list(y['hand']),atk=attackers,
              beasts=sum(beast(m) for m in y['board']),room=7-len(y['board']),
              spell=sum(m.get('spell_damage',0) for m in y['board']),
              taunts={m['entity_id'] for m in s['opponent']['board'] if m.get('taunt') and not m.get('stealth')},
              power=any(a['type']=='hero_power' for a in actions),hero_used=counts.get(oh,0),hero_buff=hero_bonus(y))
    target=hp(s['opponent']['hero']); seen=set(); nodes=0
    def visit(z,first,depth):
        nonlocal nodes
        nodes+=1
        if z['damage']>=target: return first
        if nodes>4000 or depth>18: return None
        key=(z['mana'],z['damage'],tuple(c['entity_id'] for c in z['hand']),
             tuple((i,*v) for i,v in sorted(z['atk'].items())),z['beasts'],z['room'],z['spell'],tuple(sorted(z['taunts'])),z['power'],z['hero_used'],z['hero_buff'])
        if key in seen: return None
        seen.add(key)
        moves=[]
        # Buffs/enablers precede attacks in traversal so one swing cannot consume a multiplier.
        for c in z['hand']:
            cid=c['card_id']; eid=c['entity_id']; cost=c['cost']
            if cost>z['mana']: continue
            base={'type':'play_card','card':eid}; effects=[]
            if cid in DIRECT:
                dmg=(5 if cid=='EX1_539' and z['beasts'] else DIRECT[cid])+z['spell']
                effects.append((dict(base,target=eh),('damage',dmg)))
            elif cid=='CS2_045':
                for i,(atk,n) in z['atk'].items():
                    if n: effects.append((dict(base,target=i),('buff',i)))
            elif cid in ('EX1_245','CS2_203') and z['taunts'] and (cid!='CS2_203' or z['room']):
                for i in sorted(z['taunts']):
                    a=dict(base,target=i)
                    if cid=='CS2_203': a['position']=len(y['board'])
                    effects.append((a,('silence',i)))
            elif cid=='EX1_567' and not y['hero'].get('frozen') and known:
                effects.append((base,('weapon',2)))
            elif cid=='NEW1_010' and z['room']:
                effects.append((dict(base,position=len(y['board'])),('charge',3)))
            elif cid=='EX1_012' and z['room']:
                effects.append((dict(base,position=len(y['board'])),('spell',1)))
            elif cid=='CS2_042' and z['room']:
                effects.append((dict(base,target=eh,position=len(y['board'])),('battlecry',3)))
            elif cid=='EX1_538' and z['room'] and s['opponent']['board']:
                effects.append((base,('hounds',min(z['room'],len(s['opponent']['board'])))))
            elif c['type']=='MINION' and beast(c) and cid not in ('CS2_203','EX1_534') and z['room']:
                effects.append((dict(base,position=len(y['board'])),('beast',1)))
            elif cid=='GAME_005': effects.append((base,('coin',1)))
            for a,eff in effects:
                q=copy.deepcopy(z); q['mana']-=cost; q['hand']=[x for x in q['hand'] if x['entity_id']!=eid]
                kind,arg=eff
                if kind in ('damage','battlecry'): q['damage']+=arg
                if kind=='buff':
                    q['atk'][arg][0]+=3
                    if arg==oh: q['hero_buff']+=3
                if kind=='silence': q['taunts'].remove(arg)
                if kind=='weapon': q['atk'][oh]=[2+q['hero_buff'],max(0,2-q['hero_used'])]
                if kind=='charge': q['atk'][eid]=[arg,2]
                if kind=='spell': q['spell']+=arg
                if kind=='coin': q['mana']=min(10,q['mana']+1)
                if c['type']=='MINION': q['room']-=1; q['beasts']+=beast(c)
                if kind=='hounds':
                    q['room']-=arg; q['beasts']+=arg
                    for j in range(arg): q['atk'][-eid*10-j]=[1,1]
                moves.append((a,q))
        if not z['taunts']:
            for i,(atk,n) in z['atk'].items():
                if n and atk>0:
                    q=copy.deepcopy(z); q['atk'][i][1]-=1; q['damage']+=atk
                    if i==oh: q['hero_used']+=1
                    moves.append((dict(type='attack',attacker=i,target=eh),q))
        if z['power'] and y['hero'].get('hero_class')=='HUNTER' and y['hero_power']['cost']<=z['mana']:
            q=copy.deepcopy(z); q['power']=False; q['mana']-=y['hero_power']['cost']; q['damage']+=2
            moves.append((dict(type='hero_power'),q))
        for a,q in moves:
            if first is None and a not in actions: continue
            found=visit(q,first or a,depth+1)
            if found: return found
        return None
    return visit(root,None,0)


def damage_value(m,dmg):
    if m.get('divine_shield'): return 1.5 if dmg>0 else 0
    if dmg>=m['health']: return value(m)+1.5
    return min(dmg,m['health'])*0.65


def silence_value(m):
    if m.get('silenced'): return -1
    base=CATALOG.get(m['card_id'],{})
    return (4*bool(m.get('taunt'))+2*bool(m.get('divine_shield'))+
            (6 if m['card_id']=='EX1_383' else 3*bool(m.get('deathrattle')))+
            max(0,m['attack']-base.get('attack',m['attack']))+
            .5*max(0,m.get('max_health',m['health'])-base.get('health',m['health']))+
            (4 if m['card_id'] in ('EX1_575','NEW1_019','EX1_608','EX1_531') else 0))


def score(s,a):
    y=s['you']; e=s['opponent']; hero=y['hero']; oh=hero['entity_id']; eh=e['hero']['entity_id']
    own={m['entity_id']:m for m in y['board']}; enemy={m['entity_id']:m for m in e['board']}
    health=hp(hero); incoming=threat(s); danger=incoming+3>=health
    face=1.8 if hp(e['hero'])<=12 else (1.15 if hero.get('hero_class')!='WARLOCK' else .65)
    kind=a['type']; target=a.get('target'); t=enemy.get(target) or own.get(target)
    if kind=='end_turn': return 0
    if kind=='attack':
        attacker=hero if a['attacker']==oh else own[a['attacker']]
        atk=attacker['attack']
        if target==eh: return atk*face
        if not t: return -1000
        dealt=damage_value(t,atk)
        if attacker.get('poisonous') and not t.get('divine_shield'): dealt=value(t)+1.5
        if a['attacker']==oh:
            if t['attack']>=health: return -10000
            return dealt-t['attack']*(1.5 if danger else .6)
        loss=0 if attacker.get('divine_shield') else min(t['attack'],attacker['health'])*.65
        if (t['attack']>=attacker['health'] or t.get('poisonous') and t['attack']>0) and not attacker.get('divine_shield'):
            loss=value(attacker)
            if attacker.get('deathrattle') and not attacker.get('silenced'): loss-=2
        return dealt-loss+(2 if danger and atk>=t['health'] and not t.get('divine_shield') else 0)
    if kind=='hero_power':
        pid=y['hero_power']['card_id']; hc=hero.get('hero_class')
        if pid=='EX1_tk33': return 12 if len(own)<6 else 5
        if hc=='WARLOCK':
            fatigue=(y.get('fatigue',0)+1) if y.get('deck_remaining',1)==0 else 0
            if len(y['hand'])>=9 or health<=incoming+5+fatigue: return -1000
            playable=any(c['cost']<=y['mana'] and c['type']=='MINION' for c in y['hand'])
            return (2 if playable else 5)-.2*len(y['hand'])
        if hc=='HUNTER': return 2*face+(2 if y['mana']>=6 else 0)
        return 2.5 if len(own)<5 else .5
    if kind!='play_card': return -1000
    c=next(c for c in y['hand'] if c['entity_id']==a['card']); cid=c['card_id']; cost=c['cost']
    spell=sum(m.get('spell_damage',0) for m in own.values())
    penalty=.35*cost
    locked=y.get('overload_next_turn',0)+OVERLOAD.get(cid,0)
    next_mana=max(0,min(10,y.get('max_mana',y['mana'])+1)-locked)
    penalty+=.5*OVERLOAD.get(cid,0)
    if OVERLOAD.get(cid) and any(next_mana<x['cost']<=min(10,y.get('max_mana',y['mana'])+1) for x in y['hand'] if x!=c): penalty+=1.5
    if cid=='GAME_005':
        return 8 if any(x['cost']==y['mana']+1 and x['type']=='MINION' for x in y['hand']) else -5
    if cid in DIRECT:
        dmg=(5 if cid=='EX1_539' and any(beast(m) for m in own.values()) else DIRECT[cid])+spell
        if target==eh: return dmg*face*.65-penalty
        return damage_value(t,dmg)-penalty if target in enemy else -1000
    if cid=='EX1_245': return silence_value(t)+damage_value(t,1+spell)-penalty if target in enemy else -20
    if cid=='EX1_246': return value(t)+silence_value(t)*.4-3-penalty if target in enemy else -1000
    if cid=='CS2_045':
        if target==oh:
            w=y.get('weapon'); known,counts=attack_counts(s)
            n=(max(0,2-counts.get(oh,0)) if known else 1) if w and w['card_id']=='EX1_567' else 1
            return 3*n*face-penalty if hero.get('can_attack') and not hero.get('frozen') else -20
        return 3*(2 if t.get('windfury') else 1)*face-penalty if target in own and t.get('can_attack') else -20
    if cid in ('CS2_062','EX1_259','EX1_303','EX1_312'):
        if cid=='EX1_303' and target not in own: return -1000
        dmg=1000 if cid=='EX1_312' else (t['attack'] if cid=='EX1_303' else (3 if cid=='CS2_062' else 2))+spell
        if cid=='CS2_062' and health<=dmg: return -10000
        gain=sum(damage_value(m,dmg) for m in enemy.values())
        loss=sum(damage_value(m,dmg) for m in own.values()) if cid in ('CS2_062','EX1_312') else 0
        if cid=='EX1_303':
            loss=value(t)
            # First use a ready donor's safe attack; reassess the actual resulting board.
            if any(x['type']=='attack' and x['attacker']==target and eh in x['targets'] for x in s['legal_actions']): loss+=t['attack']*face+6
        if cid=='CS2_062': loss+=dmg*(1.5 if danger else .7)
        return gain-loss-penalty+(4 if danger and gain>loss else 0)
    if cid=='EX1_302':
        if target not in enemy: return -30
        kills=not t.get('divine_shield') and t['health']<=1+spell
        return damage_value(t,1+spell)+(3 if kills and len(y['hand'])<10 else 0)-penalty
    if cid=='EX1_309':
        return value(t)+min(3,hero['max_health']-hero['health'])*(1 if danger else .6)-penalty if target in enemy else -1000
    if cid=='EX1_317':
        if len(y['hand'])>8: return -20
        counts=y.get('deck_remaining_counts',{})
        return (7 if counts.get('EX1_323',0) and y['max_mana']>=7 else 2)-penalty-(6 if danger else 0)
    if cid=='DS1_184': return 3 if y['mana']>=4 or not any(x['type']=='MINION' and x['cost']<=y['mana'] for x in y['hand']) else .1
    if cid=='EX1_248': return 9-penalty+(3 if danger else 0)
    if cid=='NEW1_031': return 8-penalty
    if cid=='EX1_538':
        n=min(7-len(own),len(enemy)); hyena=any(m['card_id']=='EX1_531' and not m.get('silenced') for m in own.values())
        return n*(2.5+bool(hyena))-penalty if n else -20
    if cid in ('EX1_610','EX1_611'):
        return (len(enemy)*1.8 if cid=='EX1_610' else max((value(m)*.45 for m in enemy.values()),default=1))-penalty
    if c['type']=='WEAPON':
        old=y.get('weapon'); loss=old['attack']*old['durability']*.6 if old else 0
        return min(c.get('durability',2),4)*c.get('attack',0)+2-loss-penalty
    if c['type']=='MINION':
        v=c.get('attack',0)+.65*c.get('health',0)-penalty
        mech=set(CATALOG.get(cid,{}).get('mechanics',[]))
        v+=1.5*('DIVINE_SHIELD' in mech)+.8*('STEALTH' in mech)
        if len(own)>=4: v-=2*(len(own)-3)
        if any(m['card_id']=='NEW1_021' and not m.get('silenced') for m in own.values()) and cid!='EX1_323': v-=12
        if cid=='EX1_323':
            if incoming+5>=15: return -1000
            return 12+max(0,15-hero['health'])-max(0,hero['health']-15)*.5
        if cid=='NEW1_021':
            if incoming>=c.get('health',7): return -2
            return 4+sum(value(m) for m in enemy.values())*.6-sum(value(m) for m in own.values())*.8
        if cid=='CS2_117':
            if target==oh: v+=min(3,hero['max_health']-hero['health'])*(2 if danger else 1)
            elif target in own: v+=min(3,t.get('max_health',t['health'])-t['health'])*.8
            else: v-=10
        if cid=='CS2_203': v+=silence_value(t) if target in enemy else -10
        if cid=='CS2_042': v+=damage_value(t,3) if target in enemy else (3*face if target==eh else -20)
        if cid=='DS1_070': v+=6+(3 if danger else 0) if target in own and beast(t) else -5
        if cid in ('EX1_058','EX1_093'):
            pos=a.get('position',len(own)); adj=y['board'][max(0,pos-1):pos+1]
            v+=sum((2 if not m.get('taunt') else 0)+(2 if cid=='EX1_093' else 0) for m in adj)
        if cid=='EX1_043': v+=.65*min(9,len(y['hand'])-1)
        if cid=='EX1_066': v+=(e.get('weapon') or {}).get('attack',0)*(e.get('weapon') or {}).get('durability',0)*.8
        if cid in ('EX1_534','EX1_110'): v+=4
        if cid=='EX1_556': v+=2
        if cid=='EX1_575': v+=3 if not danger else -3
        if cid=='EX1_258': v+=sum(x['card_id'] in OVERLOAD and x['cost']<=y['mana']-cost for x in y['hand'])*1.5
        if cid=='EX1_531' and any(x['card_id']=='EX1_538' and x['cost']<=y['mana']-cost for x in y['hand']): v+=min(len(enemy),7-len(own)-1)*1.5
        if cid=='NEW1_010': v+=5
        if cid in ('CS2_065','CS2_179'): v+=2 if danger else 1
        return v
    return -2  # Unknown spells are not cast speculatively.


def mulligan(s):
    t=next(t for t in s['legal_actions'] if t['type']=='mulligan')
    cards={c['entity_id']:c for c in s['you']['hand']}; hc=s['you']['hero']['hero_class']
    early=any(c['card_id'] in KEEP.get(hc,set()) for c in cards.values())
    kept=set(); replace=[]
    for eid in t['options']:
        c=cards[eid]; cid=c['card_id']
        keep=cid in KEEP.get(hc,set()) or (early and cid in {'EX1_556','CS2_117','EX1_258','NEW1_031','EX1_536'})
        if cid in kept and c['cost']>=2: keep=False
        if keep: kept.add(cid)
        else: replace.append(eid)
    return {'type':'mulligan','replace':replace}


def choose(s):
    t=next(t for t in s['legal_actions'] if t['type']=='choose')
    def rank(c):
        cid=c['card_id']; cost=c.get('cost',0); y=s['you']; health=hp(s['opponent']['hero'])
        r=c.get('attack',0)+.6*c.get('health',0)
        if cid in DIRECT: r=DIRECT[cid]+(6 if health<=8 else 0)
        if cid=='EX1_539' and any(beast(m) for m in y['board']): r+=2
        if cid=='CS2_203' and any(m.get('taunt') for m in s['opponent']['board']): r+=6
        if cid=='EX1_534': r+=4
        if cost>y.get('mana',0): r-=3
        if cost>y.get('max_mana',0)+1: r-=4
        return r
    ranked=sorted(t['options'],key=rank,reverse=True)
    return {'type':'choose','options':[c['entity_id'] for c in ranked[:t['min']]]}


def decide(s):
    phase=s['phase']
    if phase=='game_over': return None
    if phase=='deck_submission':
        d=json.loads((ROOT/'deck.json').read_text())
        return dict(type='submit_deck',hero_class=d['hero_class'],cards=d['cards'])
    try:
        if phase=='mulligan': action=mulligan(s)
        elif phase=='choice': action=choose(s)
        else:
            actions=expand(s['legal_actions'])
            action=lethal(s,actions)
            if action is None:
                action=max(actions,key=lambda a:score(s,a))
                hand={c['entity_id']:c for c in s['you']['hand']}
                if action['type']=='play_card' and hand[action['card']]['card_id']=='EX1_303' and not s['opponent'].get('secrets_count'):
                    attack=dict(type='attack',attacker=action['target'],target=s['opponent']['hero']['entity_id'])
                    if attack in actions: action=attack
        if allowed(action,s['legal_actions']): return action
    except Exception as exc:
        print('pilot fallback: '+repr(exc),file=sys.stderr)
    # A legal, finite fallback never concedes or fabricates a target.
    if phase=='mulligan':
        t=next(t for t in s['legal_actions'] if t['type']=='mulligan')
        return dict(type='mulligan',replace=t['options'][:t.get('min',0)])
    if phase=='choice':
        t=next(t for t in s['legal_actions'] if t['type']=='choose')
        return dict(type='choose',options=[o['entity_id'] for o in t['options'][:t['min']]])
    return next(a for a in expand(s['legal_actions']) if a['type']=='end_turn')


def main():
    path=(ROOT/(sys.argv[1] if len(sys.argv)>1 else 'game/state.json')).resolve()
    if not path.is_relative_to(ROOT): raise ValueError('State must be inside this skill workspace')
    s=json.loads(path.read_text())
    history=ROOT/'game/history.jsonl'
    if history.exists():
        try: s['_history_events']=[json.loads(line) for line in history.read_text().splitlines() if line.strip()]
        except (ValueError,OSError): pass
    if s['phase']=='game_over': print(json.dumps(dict(seq=s['seq'],game_over=True,result=s.get('result'))))
    else: print(json.dumps(dict(seq=s['seq'],action=decide(s))))

if __name__=='__main__': main()
