import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from datetime import timedelta


def hours_conversion(time):
    time = time[-8:]
    delta = timedelta(hours=int(time[:2]), minutes=int(time[3:5]), seconds=int(time[6:8]))
    total_seconds = delta.total_seconds()
    hours = int(total_seconds// 60 + 1)/60
    return hours

plt.rcParams["figure.figsize"] = (20,15)
plt.rcParams['font.size']=  22

def set_configuration_df():
    df_open = pd.read_csv("RowData/ACCs_ActualCapacities/OpeningSchemes_1907_1908.csv", sep=",", low_memory=False)

    #cleaning None in ACC
    ACC_new = df_open["ACC"].apply(lambda acc: acc if type(acc) == str else "None")
    df_open.ACC = ACC_new
    df_open = df_open[df_open["ACC"]!= "None"]

    #cleaning None in duration (in datatime format)
    duration_new = df_open["Duration"].apply(lambda time: time if type(time) == str else "None")
    df_open.Duration = duration_new
    df_open = df_open[df_open["Duration"] != "None"]

    #making hours
    min_duration = df_open["Duration"].apply(lambda time: hours_conversion(time))
    df_open["min_duration"] = min_duration


    #row renaming and nan removal
    df_open.columns = ['acc', 'configuration', 'date', 'duration_datetime', 'end', 'start','n_sectors', 'duration']
    df_open = df_open[~df_open.n_sectors.isna()]

    #transformation of n_sec in int
    df_open.n_sectors = df_open.n_sectors.astype(int)

    return df_open


df_open = set_configuration_df()


class NSectors:
    def __init__(self, n: int, durations: np.array(int)):
        self.n = n
        self.durations = durations
        self.occurences = self.durations.shape[0]
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
        if self.numConfigurations > 2:
            plt.close()
            most_3_busy = list(self.nSectors.keys())[-3:]
            fig, ax = plt.subplots()

            ax.set_xticks(range(3))
            tick_position = ax.get_xticks()
            ax.set_xticklabels([str(i) for i in most_3_busy])
            ax.set_yticks(np.arange(0, max([self.nSectors[n_sec].meanDuration for n_sec in most_3_busy])+1))
            ax.set_xlabel("NUMBER OF SECTORS")
            ax.set_ylabel("DURATION IN HOURS")
            ax.bar([str(i) for i in most_3_busy], [self.nSectors[n_sec].meanDuration for n_sec in most_3_busy])
            for i in range(3):
                ax.annotate(self.nSectors[most_3_busy[i]].occurences, xy=(0, 0), xytext=(tick_position[i], 1/3),
                            horizontalalignment='center', color="red")
            ax.annotate("OCCURENCES", xy=(0, 0), xytext=(0.75, 0.8), xycoords='figure fraction', color="red")
            ax.set_title(self.name+" Configuration")

            if save:
                plt.savefig("Figures/Configurations/"+self.name+"_config.png")
            else:
                plt.show()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


df_open.date.unique()

accs = {}

for acc in df_open.acc.unique():
    df_acc = df_open[df_open.acc == acc]
    accs[acc] = Acc(df_acc)

for acc in accs:
    accs[acc].plot_config(save=True)






# lovv = accs["LOVVCTA"]
# lovv.plot_config()


# max(df_open.n_sectors)
#
#


# lovv = df_open[df_open.acc=="LOVVCTA"]
# lovv.sort_values(by=["n_sectors", "duration"], ascending=[False, False])
#
# accs = df_open.acc.unique()
# mean_d_1, mean_d_2, mean_d_3 = [], [], []
# max_sectors_1, max_sectors_2, max_sectors_3 = [], [], []
#
# for acc in accs:
#     df_acc = df_open[df_open.acc == acc]
#     max_sec = df_acc.n_sectors.unique()
#     max_sec = np.sort(max_sec)
#     print(acc, max_sec)
#     # top_3_max_sec = df_acc.n_sectors.unique()
#
#
# df_open[df_open.acc == "UMKKCTA"]


