from hashlib import sha256, scrypt
from concurrent.futures import ThreadPoolExecutor
import math
import itertools
import struct

def doublesha256(x):
    return sha256(sha256(x).digest()).digest()

def bitcoin_hdr_to_id(hdr):
    return doublesha256(hdr)

def litecoin_hdr_to_id(hdr):
    return scrypt(password=hdr, salt=hdr, n=1024, r=1, p=1, dklen=32)

BITCOIN_TARGET =  0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff
LITECOIN_TARGET = 0x00000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

def hdrs_from_file(file_name):
    with open(file_name, "rb") as f:
        for height in itertools.count():
            hdr = f.read(HEADER_SIZE)
            if len(hdr) != HEADER_SIZE:
                break
            yield hdr

def chunk(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip(*args)

POOL_SIZE = 24

def block_ids_from_file(file_name, hdr_to_id=bitcoin_hdr_to_id):
    with ThreadPoolExecutor(POOL_SIZE) as p:
        i = 0
        for hdr_chunk in chunk(hdrs_from_file(file_name), POOL_SIZE):
            i += 1
            if i % 10000 == 0:
                print(i)
            yield from p.map(hdr_to_id, hdr_chunk)

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

def bits_to_target(bits):
    # bits to target
    bitsN = (bits >> 24) & 0xff
    # print('bitsN: %s' % bitsN)
    assert bitsN >= 0x03 and bitsN <= 0x1d, "First part of bits should be in [0x03, 0x1d]"
    bitsBase = bits & 0xffffff
    # print('bitsBase: %s' % hex(bitsBase))
    assert bitsBase >= 0x8000 and bitsBase <= 0x7fffff, "Second part of bits should be in [0x8000, 0x7fffff]"
    target = bitsBase << (8 * (bitsN-3))
    return target

def header_to_bits(hdr):
    return struct.unpack("<L", hdr[72:76])[0]

def header_to_target(hdr):
    return bits_to_target(header_to_bits(hdr))
