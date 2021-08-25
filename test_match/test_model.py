import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from ACC import acc as a
from Solver.solver import Solver
from Solver.vars import Ivars

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


df_delayed = pd.read_csv("RowData/delayed_flights.csv")
df_regulation = pd.read_csv("RowData/regulations.csv")
df_open = pd.read_csv("RowData/opening_schemes.csv")
df_mc = pd.read_csv("RowData/max_config.csv")
df_acc = pd.read_csv("RowData/accslist.csv")
# df_acc = pd.read_csv("RowData/listSmall.csv")


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

interval_size = 30
intervals = [interval_size*i for i in range(1440//interval_size + 1)]

comp_time = time.time()

accs = []
acc_index = 0
for acc in df_acc.acc.unique():
    print(acc)
    df_d_day, df_r_day, df_o_day = get_day_df(day, df_delayed, df_regulation, df_open)
    df_d_acc, df_r_acc, df_o_acc, df_m_acc = get_acc_df(acc, df_d_day, df_r_day, df_o_day, df_mc)
    accs.append(a.Acc(acc_index, acc, interval_size, intervals, df_o_acc, df_r_acc, df_d_acc, df_m_acc))
    acc_index += 1
    # print(accs[-1].delayedFlights)


print("vars", sum([sum(acc.inNeed) for acc in accs]))
print("max delayed", max(acc.maxDelayed for acc in accs))
print("done", time.time() - comp_time)

# solver = Solver(accs, intervals)
#
# print(solver.matches)
# print(len(solver.matches))
#
# solver.set_constraints()

vars = {}
for t in range(len(intervals)-1):
    vars[t] = Ivars(t)
    for acc in accs:
        if acc.inNeed[t]:
            print(acc, acc.delayedFlights[t])
            vars[t].add_in_need(acc)
    for acc in accs:
        if acc.spareCapacity[t]:
            vars[t].add_available(acc)
            print(acc, acc.spareCapacity[t])


print("end")





