"""Empirical one-hour conditional state model with speed-only backoff.

Implements the same counting and no-pseudocount policy as the archived v23 model.
"""
from collections import defaultdict

class ConditionalDBN:
    def fit(self, rows):
        self.speed = defaultdict(lambda: [0, 0, 0])
        self.joint = defaultdict(lambda: [0, 0, 0])
        for speed, wind, wave, next_state in rows:
            if any(v not in (0, 1, 2) for v in (speed, next_state)) or wind not in (0, 1) or wave not in (0, 1):
                raise ValueError('Expected three speed states and binary environmental states')
            self.speed[speed][next_state] += 1
            self.joint[speed, wind, wave][next_state] += 1
        return self

    def predict(self, speed, wind, wave):
        if speed not in (0, 1, 2) or wind not in (0, 1) or wave not in (0, 1):
            raise ValueError('Expected three speed states and binary environmental states')
        if not hasattr(self, 'joint'):
            raise ValueError('Fit the model before prediction')
        key = speed, wind, wave
        fallback = key not in self.joint
        counts = self.speed.get(speed) if fallback else self.joint[key]
        if counts is None:
            raise ValueError('No training support for this speed state')
        return [n/sum(counts) for n in counts], fallback

def brier(probabilities, observed):
    return sum((p-float(k == observed))**2 for k, p in enumerate(probabilities))
