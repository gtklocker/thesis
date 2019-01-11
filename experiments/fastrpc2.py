from os import path
import math
import configparser
from itertools import chain, zip_longest, filterfalse
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from xdg.BaseDirectory import save_cache_path, save_config_path

APP_NAME = 'bch-interlinker'
config_path = save_config_path(APP_NAME)
config_file_path = path.join(config_path, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

chunk = lambda n, iterable: (filterfalse(lambda x: x == (), chunk) for chunk in (zip_longest(*[iter(iterable)]*n, fillvalue=())))

rpc = AuthServiceProxy("http://%s:%s@%s:%s" %
            (config['daemon']['user'], config['daemon']['password'],
                config['daemon']['host'], config['daemon']['port']))

def nice_batch(reqs):
    chunks = chunk(100000, reqs)
    return chain.from_iterable(rpc.batch_(r) for r in chunks)

def command_for_height_range(cmd, range_):
    return nice_batch([cmd, h] for h in range_)

def block_hashes_with_height(range_):
    return command_for_height_range('getblockhash', range_)

def blocks_with_height(range_):
    return nice_batch(['getblock', h] for h in block_hashes_with_height(range_))

VELVET_FORK_GENESIS = '00000000000001934669a81ecfaa64735597751ac5ca78c4d8f345f11c2237cf'
MAX_TARGET = 0xffff0000000000000000000000000000000000000000000000000000

def level(block_id, target=None):
    target = MAX_TARGET if target is None else target
    if isinstance(block_id, str):
        block_id = int(block_id, 16)
    return -int(math.ceil(math.log(float(block_id) / target, 2)))

tip_height = rpc.getblockcount()

with open('fullblock.csv', 'w') as f:
    for i, block in enumerate(blocks_with_height(range(1, tip_height+1))):
        f.write(','.join(map(str, (i + 1, block['hash'], block['size'])))+'\n')
        if i % 100000 == 0:
            print(i)
