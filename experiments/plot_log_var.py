from itertools import tee
from science import *

def log_var_for_file(file_name, hdr_to_id=bitcoin_hdr_to_id, target=None):
    interlink_size = 1
    gen, blkhdrs = tee(hdrs_from_file(file_name))
    genesis = next(gen)
    genesis_target = header_to_target(genesis)
    for hdr in blkhdrs:
        blkid = hdr_to_id(hdr)
        target = header_to_target(hdr)
        interlink_size = max(interlink_size, level(blkid[::-1].hex()) + 1)
        yield interlink_size + math.log2(float(target)/float(genesis_target))

def bitcoin_cash_log_var():
    yield from log_var_for_file("BitcoinCash-Mainnet.bin")
def bitcoin_core_log_var():
    yield from log_var_for_file("BitcoinCore-Mainnet.bin")

def column_for_levels(levels):
    return pd.DataFrame(levels)[0]#.cummax()[0]

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.concat(
            [column_for_levels(lvls)
                for lvls in [bitcoin_core_log_var(), bitcoin_cash_log_var()]]
            , axis=1, keys=["Bitcoin", "Bitcoin Cash"]).astype(float)
    print(df)
    df.plot(logx=True).set(ylabel="|interlink| + log2(vartarget / genesistarget)", xlabel="block height")
    plt.show()
