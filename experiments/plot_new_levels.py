import pandas as pd
import matplotlib.pyplot as plt

from science import *

from collections import Counter

def level_var(hdr):
    blkid = bitcoin_hdr_to_id(hdr)
    target = header_to_target(hdr)
    return level(blkid, target=target)

levels_df = pd.DataFrame(bitcoin_core_headers()).applymap(level_var)[0]

def windowed_counts(df):
    WINDOW_SIZE = 2000
    counts = Counter(df[:WINDOW_SIZE])

    old_el = 0
    new_el = WINDOW_SIZE
    length = len(df)

    while new_el < length:
        counts[df[old_el]] -= 1
        counts[df[new_el]] += 1
        yield {k: counts[k] for k in counts if k < 6}
        old_el += 1
        new_el += 1

win = pd.DataFrame(windowed_counts(levels_df), dtype='int32').fillna(0)
win.columns = win.columns.to_series().apply(lambda mu: '%d-superblocks' % mu)
win.plot(logy=True).set(ylabel=r"\# of superblocks", xlabel="block height")
plt.show()
