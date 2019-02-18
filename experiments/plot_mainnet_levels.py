from hashlib import sha256, scrypt
import math
import itertools

def doublesha256(x):
    return sha256(sha256(x).digest()).digest()

def bitcoin_hdr_to_id(hdr):
    return doublesha256(hdr)

def litecoin_hdr_to_id(hdr):
    return scrypt(password=hdr, salt=hdr, n=1024, r=1, p=1, dklen=32)

BITCOIN_TARGET =  0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff
LITECOIN_TARGET = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

def block_ids_from_file(file_name, hdr_to_id=bitcoin_hdr_to_id):
    with open(file_name, "rb") as f:
        for height in itertools.count():
            hdr = f.read(HEADER_SIZE)
            if len(hdr) != HEADER_SIZE:
                break
            yield hdr_to_id(hdr)

def level(block_id, target=None):
    target = BITCOIN_TARGET if target is None else target
    if isinstance(block_id, str):
        block_id = int(block_id, 16)
    return -int(math.ceil(math.log(float(block_id) / target, 2)))

HEADER_SIZE = 80

def levels_for_file(file_name, hdr_to_id=bitcoin_hdr_to_id, target=None):
    for blkid in block_ids_from_file(file_name, hdr_to_id):
        yield level(blkid[::-1].hex(), target)

def bitcoin_cash_levels():
    yield from levels_for_file("BitcoinCash-Mainnet.bin")
def bitcoin_core_levels():
    yield from levels_for_file("BitcoinCore-Mainnet.bin")
def litecoin_levels():
    yield from levels_for_file("Litecoin-Mainnet.bin", litecoin_hdr_to_id, LITECOIN_TARGET)

def column_for_levels(levels):
    return pd.DataFrame(levels).cummax()[0]

if __name__ == "__main__":
    import pandas as pd
    import matplotlib.pyplot as plt
    df = pd.concat(
            [column_for_levels(lvls)
                for lvls in [bitcoin_core_levels(), bitcoin_cash_levels()]]#, litecoin_levels()]]
            , axis=1, keys=["Bitcoin", "Bitcoin Cash"])#, "Litecoin"])
    df.plot(logy=True).set(ylabel="interlink size", xlabel="block height")
    plt.show()
