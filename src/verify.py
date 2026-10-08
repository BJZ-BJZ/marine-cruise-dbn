"""Recompute all 24 archived scores and inspect conditional-table support."""

if not __debug__:
    raise RuntimeError('Verification requires assertions: do not use -O, -OO or PYTHONOPTIMIZE')
from pathlib import Path
import json
import math
from dbn import brier

path = Path(__file__).resolve().parents[1]/'data/aggregated_evaluations.json'
data = json.loads(path.read_text(encoding='utf-8'))
checks = []
for evaluation in data['evaluations']:
    for name, model in evaluation['models'].items():
        groups = model['scoring_groups']
        n = sum(g['count'] for g in groups)
        assert n == evaluation['n_test']
        for g in groups:
            assert len(g['p']) == 3 and all(0 <= x <= 1 for x in g['p'])
            assert math.isclose(sum(g['p']), 1., abs_tol=1e-12)
        score = sum(g['count']*brier(g['p'],g['observed']) for g in groups)/n
        accuracy = sum(g['count']*(max(range(3),key=lambda i:g['p'][i]) == g['observed']) for g in groups)/n
        assert math.isclose(score, model['brier'], abs_tol=1e-12)
        assert math.isclose(accuracy, model['accuracy'], abs_tol=1e-12)
        if name == 'speed_wind_wave' and evaluation['grid_distance_limit_km'] == 30:
            counts = [sum(row) for row in model['training_condition_counts'].values()]
            checks.append(dict(train=evaluation['train_ship'], n_train=evaluation['n_train'],
                               missing_conditions=12-len(counts), sparse_conditions=sum(1<=v<=5 for v in counts)))
assert checks[0]['missing_conditions'] == 1 and checks[0]['sparse_conditions'] == 6
assert checks[1]['sparse_conditions'] == 5
print(json.dumps(dict(status='PASS', score_checks=24, main_cpt_support=checks,
    scope='Archived score reconstruction from aggregate groups; no fresh AIS/environment acquisition or model fit.')))
