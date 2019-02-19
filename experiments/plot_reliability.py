import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./reliability.csv')
df = df[df.height >= 1272000]
df.loc[df.missingPtrs == -1, 'missingPtrs'] = r'$\infty$'
counts = df['missingPtrs'].value_counts(normalize=True, sort=False) * 100
counts.plot(kind='bar', rot=False) \
    .set(xlabel='missing pointers', ylabel='% of blocks')
plt.show()
