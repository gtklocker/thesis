import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./sizes.csv')
df['savings'] = 1-df['blockset']/df['blocklist']
df['blockSetInterlinkSize'] = np.log2(df['blockset'])
df['blockListInterlinkSize'] = np.log2(df['blocklist'])
df['interlinkProofSavings'] = 1-df['blockSetInterlinkSize']/df['blockListInterlinkSize']

y = df['interlinkProofSavings']
weights = np.ones_like(y) * 100 / len(y)
plt.hist(y * 100, weights=weights)

plt.xlabel('interlink proof size savings %')
plt.ylabel('blocks %')
plt.suptitle('block set over block list interlink proof savings')

plt.savefig('sizes.pdf')
plt.show()
