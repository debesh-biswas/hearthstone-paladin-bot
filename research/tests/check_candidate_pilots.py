"""Static package checks and saved-state decisions only; no game runner or model calls."""
import contextlib
import hashlib
import importlib.util
import io
import json
import time
from pathlib import Path
from hs_arena.deck import validate_deck_data
from hs_arena.skill.loader import load_skill

ROOT=Path(__file__).resolve().parents[2]
NAMES=('burst-shaman','infernal-warlock','pressure-hunter')
results={'method':'Static loaders and recorded public states; no match runner', 'packages':{}, 'states':0,'illegal':0,'fallbacks':0,'max_seconds':0,'failures':[]}
modules=[]
for name in NAMES:
    d=ROOT/'decks'/name
    spec=importlib.util.spec_from_file_location(name,d/'scripts/move.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);modules.append(m)
    for base in (d,ROOT/'research/haiku-skills'/name):
        skill=load_skill(base)
        errors=validate_deck_data(json.loads((base/'deck.json').read_text()))
        assert not errors,errors
        assert skill.name==name
        for path in base.rglob('*.py'): compile(path.read_text(),str(path),'exec')
    assert (d/'deck.json').read_bytes()==(ROOT/'research/haiku-skills'/name/'deck.json').read_bytes()
    results['packages'][name]={'skill_static':'pass','deck_static':'pass','same_model_deck':True,
                             'pilot_sha256':hashlib.sha256((d/'scripts/move.py').read_bytes()).hexdigest()}
assert len({v['pilot_sha256'] for v in results['packages'].values()})==1
paths=sorted((ROOT/'games/astra').glob('*/g_*/p*/decisions/*.state.json'))
# Every selected saved state is evaluated once by each packaged pilot. No game is advanced.
for path in paths[::max(1,len(paths)//200)][:200]:
    state=json.loads(path.read_text())
    if state['phase'] in ('deck_submission','game_over'): continue
    for m in modules:
        err=io.StringIO();start=time.perf_counter()
        with contextlib.redirect_stderr(err): action=m.decide(state)
        elapsed=time.perf_counter()-start
        results['states']+=1;results['max_seconds']=max(results['max_seconds'],elapsed)
        if err.getvalue(): results['fallbacks']+=1;results['failures'].append({'path':str(path.relative_to(ROOT)),'error':err.getvalue()})
        if not m.allowed(action,state['legal_actions']):
            results['illegal']+=1;results['failures'].append({'path':str(path.relative_to(ROOT)),'action':action})
(ROOT/'research/candidate-pilot-offline-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
assert results['illegal']==results['fallbacks']==0
