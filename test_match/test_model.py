import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from ACC import acc as a


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


df_delayed = pd.read_csv("RowData/delayed_flights.csv")
df_regulation = pd.read_csv("RowData/regulations.csv")
df_open = pd.read_csv("RowData/opening_schemes.csv")
df_mc = pd.read_csv("RowData/max_config.csv")
df_acc = pd.read_csv("RowData/acc_list.csv")


def get_day_df(d, df_delayed, df_regulation, df_open):
    df_d_d = df_delayed[df_delayed.Date == d]
    df_r_d = df_regulation[df_regulation.Date == d]
    df_o_d = df_open[df_open.Date == d]

    return df_d_d, df_r_d, df_o_d

def get_acc_df(a, df_delayed, df_regulation, df_open, df_mc):
    df_r_acc = df_regulation[df_regulation.acc == a]
    df_d_acc = df_delayed[df_delayed.MPR.isin(df_r_acc.Regulation)]
    df_o_acc = df_open[df_open.acc == a]
    df_m_acc = df_mc[df_mc.acc == a]

    return df_d_acc, df_r_acc, df_o_acc, df_m_acc


# day
days = df_open.Date.unique()
day = days[0]

interval_size = 10
intervals = [interval_size*i for i in range(1440//interval_size + 1)]

comp_time = time.time()

accs = []
for acc in df_acc.acc.unique():

    df_d_day, df_r_day, df_o_day = get_day_df(day, df_delayed, df_regulation, df_open)
    df_d_acc, df_r_acc, df_o_acc, df_m_acc = get_acc_df(acc, df_d_day, df_r_day, df_o_day, df_mc)
    accs.append(a.Acc(acc, interval_size, intervals, df_o_acc, df_r_acc, df_d_acc, df_m_acc))

# regulation = "LCS2W20"

# df_staff = df_regulation[df_regulation.Regulation == regulation]
# df_del = df_delayed[df_delayed.MPR == regulation]

# delays = df_del["Total Delay"].sort_values(ascending=False).to_numpy()
# start = df_staff.iloc[0].start
# end = df_staff.iloc[0].end
# delayed_time = np.array([start + (end-start)*i/delays.shape[0] for i in range(delays.shape[0])])
# delays_per_interval = [sum(delays[np.where((intervals[i] <= delayed_time) & (delayed_time < intervals[i+1]))]) for i in range(delays.shape[0])]

print("vars", sum([sum(acc.inNeed) for acc in accs]))
print("max delayed", max(acc.maxDelayed for acc in accs))
print("done", time.time() - comp_time)



# # regulation
# regs = df_r_day.Regulation.unique()
# reg = regs[1]
#
# df_reg = df_r_day[df_r_day.Regulation == reg]
# df_d_day_r = df_d_day[df_d_day.MPR == reg]
#
# # *****
# dod = sorted(df_o_day.ACC.unique())
# df_r_day.ID.unique()
# i = 2
# print(df_r_day.ID.unique()[i])
# print(df_r_day.ID.unique()[i] in df_o_day.ACC.unique(), "\n", df_o_day.ACC.unique())
from re import search
g= df_open.ACC.unique()
k = 0
for acc in df_open.ACC.unique():
    if search("CTA", acc):
        k +=1


