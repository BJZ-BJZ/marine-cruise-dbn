"""Synthetic demonstration of conditional frequencies and unseen-row backoff."""
import json
from dbn import ConditionalDBN, brier

model = ConditionalDBN().fit([(0,0,0,0), (0,0,0,1), (1,1,0,2), (1,1,0,1), (2,1,1,2)])
p, fallback = model.predict(0,1,1)
assert fallback and p == [.5,.5,0]
assert brier(p,0) == .5
print(json.dumps(dict(status='PASS', input='Synthetic teaching data; not accident observations',
                     probability=p, unseen_condition_backoff=fallback, brier=brier(p,0))))
