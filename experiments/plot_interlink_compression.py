import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from science import *
from interlink import Interlink

def interlink_sizes(hdr_file):
    blkids = block_ids_from_file(hdr_file)
    genesis = next(blkids)
    interlink = Interlink(genesis)
    for blkid in blkids:
        lvl = level(blkid[::-1].hex())
        interlink = interlink.update(blkid, lvl)
        yield (len(interlink.as_array()), len(set(interlink.as_array())))

def columns_for_sizes(sizes):
    return pd.DataFrame(sizes, columns=['blocklist', 'blockset'])

def plot_commitment_comparison(hdr_file):
    df = columns_for_sizes(interlink_sizes(hdr_file)).rolling(1000).mean()
    df.plot()
    plt.show()

def plot_proof_comparison(hdr_file):
    df = columns_for_sizes(interlink_sizes(hdr_file))
    df['savings'] = 1-df['blockset']/df['blocklist']
    df['blockset_proof'] = np.log2(df['blockset'])
    df['blocklist_proof'] = np.log2(df['blocklist'])
    df['blockset_proof_savings'] = 1-df['blockset_proof']/df['blocklist_proof']

    #df[['blocklist_proof', 'blockset_proof']].rolling(2000).mean().plot() \
    #    .set(ylabel="# of block ids in interlink inclusion proof", xlabel="block height")
    (df['blockset_proof_savings'] * 100).rolling(2000).mean().plot() \
        .set(ylabel="interlink inclusion proof savings (%)", xlabel="block height")
    plt.show()

if __name__ == "__main__":
    plot_proof_comparison("BitcoinCash-Mainnet.bin")
