import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./levels.csv')
df = df[df['height'] >= 1257603]
x = df['height']
y = df['level'].cummax()

plt.plot(x, y)
plt.xlabel('block height')
plt.ylabel('interlink size')
plt.savefig('bitcoin-cash-testnet-levels-after-velvet-genesis.pdf')
plt.show()
