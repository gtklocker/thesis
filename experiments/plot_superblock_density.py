import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker

from science import *

from collections import Counter

def level_var(hdr):
    blkid = bitcoin_hdr_to_id(hdr)
    target = header_to_target(hdr)
    return level(blkid, target=target)

MAX_LEVEL = 6
levels_df = pd.DataFrame(bitcoin_core_headers()).applymap(level_var)[0]

WINDOW_SIZE = 1000

def window_size(level):
    return WINDOW_SIZE * 2**level + 1

def levels():
    yield from range(MAX_LEVEL+1)

def windowed_counts(df):
    counts = [0 for lvl in range(MAX_LEVEL+1)]
    new_els = [window_size(lvl) for lvl in range(MAX_LEVEL+1)]
    length = len(df)

    max_window_size = window_size(MAX_LEVEL)
    center_el = max_window_size // 2

    assert center_el + max_window_size // 2 + 1 < length

    for i in range(min(length, max_window_size)):
        lvl = df[i]
        for l in range(lvl+1):
            if l <= MAX_LEVEL:
                left_el = center_el - window_size(l) // 2
                right_el = center_el + window_size(l) // 2
                if left_el <= i <= right_el:
                    counts[l] += 1

    yield {k: counts[k]/window_size(k) for k in levels()}
    while center_el + max_window_size // 2 + 1 < length:
        for lvl in levels():
            old_el = center_el - window_size(lvl) // 2
            new_el = center_el + window_size(lvl) // 2 + 1
            if df[old_el] >= lvl:
                counts[lvl] -= 1
            if df[new_el] >= lvl:
                counts[lvl] += 1
        yield {k: counts[k]/window_size(k) for k in levels()}
        center_el += 1

def binomial_expectation(n, p):
    return n*p

def binomial_std(n, p):
    return math.sqrt(n*p*(1-p))

def bounds_for_level(lvl):
    expectation = binomial_expectation(window_size(lvl), 2**(-lvl)) / window_size(lvl)
    std = binomial_std(window_size(lvl), 2**(-lvl)) / window_size(lvl)
    return (expectation - std, expectation + std)

def draw_expectations(ax):
    for lvl in levels():
        bottom, top = bounds_for_level(lvl)
        ax.axhspan(bottom, top, facecolor=ax.get_lines()[lvl].get_color(), alpha=0.35)

win = pd.DataFrame(windowed_counts(levels_df), dtype='int32').fillna(0)
win.columns = win.columns.to_series().apply(lambda mu: '%d-superblocks' % mu)
ax = win.plot(logy=True)
draw_expectations(ax)
ax.set(ylabel="superblock density", xlabel="block height")
ax.set_yscale('log', basey=2)
plt.show()
