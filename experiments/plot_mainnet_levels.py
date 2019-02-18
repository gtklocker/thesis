from science import *

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
