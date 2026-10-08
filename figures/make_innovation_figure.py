"""Innovation figure for this project: regenerated from the project's own data files.
Run: python make_innovation_figure.py  (needs matplotlib, numpy, pandas)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, pandas as pd, json
from pathlib import Path
plt.rcParams.update({'font.size': 10})
R = Path(__file__).parent.parent

d = json.load(open(R / 'data/aggregated_evaluations.json'))
evs = d['evaluations']
models = ['speed', 'speed_wind', 'speed_wave', 'speed_wind_wave']
labels = ['speed only', 'speed+wind', 'speed+wave', 'speed+wind+wave']
settings = [f"{e['train_ship'].split()[0]}->{e['test_ship'].split()[0]}\n{e['grid_distance_limit_km']}km" for e in evs]
B = np.array([[e['models'][m]['brier'] for m in models] for e in evs])
x = np.arange(len(settings)); w = 0.18
colors = ['#2e86c1', '#e67e22', '#1a7f4b', '#b03a2e']
fig, ax = plt.subplots(figsize=(11, 5.2))
for j, (lab, c) in enumerate(zip(labels, colors)):
    ax.bar(x + (j - 1.5) * w, B[:, j], w, label=lab, color=c)
ax.set_xticks(x); ax.set_xticklabels(settings, fontsize=8)
ax.set_ylabel('Brier score (lower = better)')
ax.set_title('Conditional DBN: wind/wave conditioning does not beat the speed-only baseline\n'
             'The innovation: conditional dynamic Bayesian network + data-identifiability diagnosis',
             fontsize=11)
ax.legend(fontsize=9)
fig.tight_layout(); fig.savefig(Path(__file__).parent / 'fig3_brier_models.png', dpi=150)
plt.close(fig); print('saved fig3_brier_models.png')
