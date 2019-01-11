import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./prob.csv')
group = df.groupby(df.missing)
prob = (group.size() / group.size().sum()) * 100

fig, ax = plt.subplots(1, 1)
p = ax.plot(prob.keys(), prob)
xtl = ax.get_xticks().tolist()
xtl = [int(x) for x in xtl]
xtl[1] = r'$\infty$'
ax.set_xticklabels(xtl)
plt.xlabel('missing pointers')
plt.ylabel('% of blocks')
plt.savefig('testnet-deployment-reliability.pdf')
plt.show()
