import pandas as pd
import matplotlib.pyplot as plt

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
    #print('max_window_size=%d' % max_window_size)
    center_el = max_window_size // 2
    #print('center_el=%d' % center_el)

    assert center_el + max_window_size // 2 + 1 < length

    for i in range(min(length, max_window_size)):
        lvl = df[i]
        #print('actual level %d' % lvl)
        for l in range(lvl+1):
            if l <= MAX_LEVEL:
                left_el = center_el - window_size(l) // 2
                right_el = center_el + window_size(l) // 2
                #print('left_el=%d, i=%d, right_el=%d' % (left_el, i, right_el))
                if left_el <= i <= right_el:
                    #print('pass level %d' % l)
                    counts[l] += 1

    #print({k: counts[k]/window_size(k) for k in levels()})
    yield {k: counts[k]/window_size(k) for k in levels()}
    while center_el + max_window_size // 2 + 1 < length:
        for lvl in levels():
            old_el = center_el - window_size(lvl) // 2
            new_el = center_el + window_size(lvl) // 2 + 1
            if df[old_el] >= lvl:
                counts[lvl] -= 1
            if df[new_el] >= lvl:
                counts[lvl] += 1
        #print({k: counts[k]/window_size(k) for k in levels()})
        yield {k: counts[k]/window_size(k) for k in levels()}
        center_el += 1

#fake_levels_df = pd.DataFrame([0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 4])[0]
#print(fake_levels_df)
win = pd.DataFrame(windowed_counts(levels_df), dtype='int32').fillna(0)
win.columns = win.columns.to_series().apply(lambda mu: '%d-superblocks' % mu)
print(win)
win.plot(logy=True).set(ylabel="superblock density", xlabel="block height")
plt.show()
