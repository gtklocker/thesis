from hashlib import sha256
import math
import itertools

def doublesha256(x):
    return sha256(sha256(x).digest()).digest()

def hdr_to_id(hdr):
    return doublesha256(hdr)

def hdr_to_human_id(hdr):
    return hdr_to_id(hdr)[::-1].hex()

BITCOIN_TARGET =  0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff
LITECOIN_TARGET = 0x12a765e31ffd4059bada1e25190f6e98c99d9714d334efa41a195a7e7e04bfe2

def level(block_id, target=None):
    target = BITCOIN_TARGET if target is None else target
    if isinstance(block_id, str):
        block_id = int(block_id, 16)
    return -int(math.ceil(math.log(float(block_id) / target, 2)))

HEADER_SIZE = 80

def levels_for_file(file_name, target=None):
    with open(file_name, "rb") as f:
        for height in itertools.count():
            hdr = f.read(HEADER_SIZE)
            if len(hdr) != HEADER_SIZE:
                break
            yield level(hdr_to_human_id(hdr), target)

def bitcoin_cash_levels():
    yield from levels_for_file("BitcoinCash-Mainnet.bin")
def bitcoin_core_levels():
    yield from levels_for_file("BitcoinCore-Mainnet.bin")
def litecoin_levels():
    yield from levels_for_file("Litecoin-Mainnet.bin", LITECOIN_TARGET)

def column_for_levels(levels):
    return pd.DataFrame(levels).cummax()[0]

import pandas as pd
import matplotlib.pyplot as plt
df = pd.concat(
        [column_for_levels(lvls)
            for lvls in [bitcoin_core_levels(), bitcoin_cash_levels(), litecoin_levels()]]
        , axis=1, keys=["Bitcoin", "Bitcoin Cash", "Litecoin"])
df.plot().set(ylabel="interlink size", xlabel="block height")
plt.show()
