import pandas as pd
import matplotlib.pyplot as plt

from science import *

from collections import Counter

def level_var(hdr):
    blkid = bitcoin_hdr_to_id(hdr)
    target = header_to_target(hdr)
    return level(blkid, target=target)

MAX_LEVEL = 7
levels_df = pd.DataFrame(bitcoin_core_headers()).applymap(level_var)[0]

def window_size(level):
    return 1000 * 2**level

def windowed_counts(df):
    old_el = 0
    counts = [0 for lvl in range(MAX_LEVEL+1)]
    for i in range(window_size(MAX_LEVEL)):
        if window_size(df[i]) < i:
            counts[df[i]] += 1

    new_els = [window_size(lvl) for lvl in range(MAX_LEVEL+1)]
    active_levels = set(lvl for lvl in range(MAX_LEVEL+1))
    length = len(df)

    while active_levels:
        prunable_levels = set()
        for lvl in active_levels:
            if new_els[lvl] >= length:
                prunable_levels.add(lvl)
                continue

            if df[old_el] == lvl:
                counts[lvl] -= 1
            if df[new_els[lvl]] == lvl:
                counts[lvl] += 1
            new_els[lvl] += 1
        active_levels -= prunable_levels
        yield {k: counts[k] for k in range(MAX_LEVEL+1)}
        old_el += 1

win = pd.DataFrame(windowed_counts(levels_df), dtype='int32').fillna(0)
win.columns = win.columns.to_series().apply(lambda mu: '%d-superblocks' % mu)
win.plot(logy=True).set(ylabel=r"\# of superblocks", xlabel="block height")
plt.show()
