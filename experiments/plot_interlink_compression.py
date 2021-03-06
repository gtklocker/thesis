import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from science import *
from interlink import Interlink

def interlink_sizes(blkids, target=BITCOIN_TARGET):
    genesis = next(blkids)
    interlink = Interlink(genesis)
    for blkid in blkids:
        lvl = level(blkid, target)
        interlink = interlink.update(blkid, lvl)
        yield (len(interlink.as_array()), len(set(interlink.as_array())))

def df_for_interlink_sizes(*args, **kwargs):
    df = pd.DataFrame(interlink_sizes(*args, **kwargs), columns=['blocklist', 'blockset'])
    df['savings'] = 1-df['blockset']/df['blocklist']
    df['blockset_proof'] = np.log2(df['blockset'])
    df['blocklist_proof'] = np.log2(df['blocklist'])
    df['blockset_proof_savings'] = 1-df['blockset_proof']/df['blocklist_proof']
    return df

def plot_commitment_comparison(df):
    df = df[["blocklist", "blockset"]].rolling(1000).mean()
    df \
        .rename(columns={"blocklist": "Block List", "blockset": "Block Set"}) \
        .plot() \
        .set(ylabel=r"\# of block ids in interlink vector", xlabel="block height")

def plot_proof_savings(df):
    (df['blockset_proof_savings'] * 100).rolling(2000).mean().plot() \
        .set(ylabel=r"interlink inclusion proof savings (\%)", xlabel="block height")

def plot_proof_cmp(df):
    df[['blocklist_proof', 'blockset_proof']] \
        .rename(columns={"blocklist_proof": "Block List", "blockset_proof": "Block Set"}) \
        .rolling(2000).mean().plot() \
        .set(ylabel=r"\# of block ids in interlink inclusion proof", xlabel="block height")

if __name__ == "__main__":
    bitcoin_cash_df = df_for_interlink_sizes(bitcoin_cash_blkids())
    #bitcoin_core_df = df_for_interlink_sizes(bitcoin_core_blkids())
    #litecoin_df = df_for_interlink_sizes(litecoin_blkids(), target=LITECOIN_TARGET)
    #plot_commitment_comparison(litecoin_df)
    #plt.show()
    plot_proof_savings(bitcoin_cash_df)
    plt.show()
    #plot_proof_cmp(bitcoin_core_df)
    #plt.show()
