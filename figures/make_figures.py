"""Generate research figures from real project data. One figures/ dir per repo."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({
    'figure.dpi': 160, 'savefig.dpi': 160,
    'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 10,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.grid': True, 'grid.alpha': 0.3,
})
PALETTE = ['#1f6f9f', '#d96c2c', '#3a9e6e', '#8e5aa8', '#c0a02e', '#4aa3c7', '#e07b7b', '#6e7f80']

REPOS = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(7)


def savefig(fig, path):
    fig.tight_layout()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print('wrote', path)


def dbn_figs(d):
    ev = json.load(open(d / 'data/aggregated_evaluations.json'))['evaluations']
    labels = [f"{e['train_ship'].split()[0]}→{e['test_ship'].split()[0]}\n{e['grid_distance_limit_km']}km"
              for e in ev]
    brier = [e['models']['speed']['brier'] for e in ev]
    acc = [e['models']['speed']['accuracy'] for e in ev]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharex=True)
    x = np.arange(len(ev))
    axes[0].bar(x, brier, 0.6, color=PALETTE[3], edgecolor='k', lw=0.5)
    axes[0].set_ylabel('Brier score'); axes[0].set_title('Brier score by train/test setup')
    axes[1].bar(x, acc, 0.6, color=PALETTE[2], edgecolor='k', lw=0.5)
    axes[1].set_ylabel('Accuracy'); axes[1].set_title('Accuracy by train/test setup')
    for a in axes:
        a.set_xticks(x); a.set_xticklabels(labels, fontsize=8)
        a.set_ylim(0, max(max(brier), max(acc)) * 1.15)
    fig.suptitle('DBN cross-vessel generalization (speed state)')
    savefig(fig, d / 'figures/fig1_brier_accuracy.png')



if __name__ == '__main__':
    d = REPOS
    (d / 'figures').mkdir(exist_ok=True)
    dbn_figs(d)
    print('done')
