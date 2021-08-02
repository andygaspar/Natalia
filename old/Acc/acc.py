import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from old.configuration_data import set_configuration_df


class NSectors:
    def __init__(self, n: int, durations: np.array):
        self.n = n
        self.durations = durations
        self.occurrences = self.durations.shape[0]
        self.meanDuration = np.mean(self.durations)
        self.stdDuration = np.std(self.durations)

    def __repr__(self):
        return str(self.n)

    def __str__(self):
        return str(self.n)


class Acc:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy(deep=True)
        self.df.sort_values(by="n_sectors", inplace=True)
        self.name = self.df.iloc[0].acc
        self.country = self.name[:3]
        self.nSectors = {}
        n_sectors = self.df.n_sectors.unique()
        for n in n_sectors:
            durations = self.df[self.df.n_sectors == n].duration.to_numpy()
            self.nSectors[n] = NSectors(n, durations)
        self.numConfigurations = n_sectors.shape[0]

    def plot_config(self, save=False):
        plt.rcParams["figure.figsize"] = (20, 15)
        plt.rcParams['font.size'] = 22

        if self.numConfigurations > 2:
            plt.close()
            most_3_busy = list(self.nSectors.keys())[-3:]
            fig, ax = plt.subplots()

            ax.set_xticks(range(3))
            tick_position = ax.get_xticks()
            ax.set_xticklabels([str(i) for i in most_3_busy])
            ax.set_yticks(np.arange(0, max([self.nSectors[n_sec].meanDuration for n_sec in most_3_busy]) + 1))
            ax.set_xlabel("NUMBER OF SECTORS")
            ax.set_ylabel("DURATION IN HOURS")
            ax.bar([str(i) for i in most_3_busy], [self.nSectors[n_sec].meanDuration for n_sec in most_3_busy])
            for i in range(3):
                ax.annotate(self.nSectors[most_3_busy[i]].occurrences, xy=(0, 0), xytext=(tick_position[i], 1 / 3),
                            horizontalalignment='center', color="red")
            ax.annotate("OCCURRENCES", xy=(0, 0), xytext=(0.75, 0.8), xycoords='figure fraction', color="red")
            ax.set_title(self.name + " Configuration")

            if save:
                plt.savefig("Figures/Configurations/" + self.name + "_config.png")
            else:
                plt.show()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


def make_acc_dict():
    df_open = set_configuration_df()
    df_open.date.unique()

    acc_dict = {}

    for acc in df_open.acc.unique():
        df_acc = df_open[df_open.acc == acc]
        acc_dict[acc] = Acc(df_acc)

    return acc_dict
