import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from ACC import acc as a
from DataAggregation import saturation
from Solver.solver import Solver

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

tolerance = 40

df_delayed = pd.read_csv("RowData/delayed_flights.csv")
df_regulation = pd.read_csv("RowData/regulations.csv")
df_open = pd.read_csv("RowData/opening_aggregated.csv")
df_open = df_open[
    ~df_open.acc.isin(["EHMC", "EYKA", "EYPA", "EYSA", "EYVI", "LHKR", "UMKK", "UMMV", "EGCC"])]  # not considered
df_air_capacity = pd.read_csv("RowData/airspace_capacity.csv")
df_actual_capacity = pd.read_csv("RowData/actual_capacity.csv")
df_sector_capacity = pd.read_csv("RowData/sector_capacity.csv")
# df_saturation = saturation.get_saturation_df(tolerance)
df_saturation = pd.read_csv("RowData/saturation_aggregated.csv")
# df_acc = pd.read_csv("RowData/accslist.csv")
# df_acc = pd.read_csv("RowData/listSmall.csv")


df_regulation["acc"] = df_regulation.Airspace.apply(lambda a: a[:4])
df_regulation.to_csv("RowData/regulations.csv", index_label=False, index=False)


def get_acc_df(a, df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity, df_saturation, df_sec_cap):
    df_r_acc = df_regulation[df_regulation.acc == a]
    df_d_acc = df_delayed[df_delayed.Regulation.isin(df_r_acc.Regulation)]
    df_o_acc = df_open[df_open.acc == a]
    df_c_acc = df_air_capacity[df_air_capacity.acc == a]
    df_a_acc = df_actual_capacity[df_actual_capacity.acc == a]
    df_s_acc = df_saturation[df_saturation.acc == a]
    df_sc_acc = df_sec_cap[df_sec_cap.acc == a]

    return df_d_acc, df_r_acc, df_o_acc, df_c_acc, df_a_acc, df_s_acc, df_sc_acc


# day
days = df_open.date.unique()
days = days[:2]

comp_time = time.time()

acc_list = df_open.acc.unique()
accs = []
acc_index = 0
for acc in acc_list[:4]:
    df_d_acc, df_r_acc, df_o_acc, df_m_acc, df_a_acc, df_s_acc, df_sc_acc = get_acc_df(acc, df_delayed, df_regulation,
                                                                                       df_open,
                                                                                       df_air_capacity,
                                                                                       df_actual_capacity,
                                                                                       df_saturation,
                                                                                       df_sector_capacity)
    accs.append(a.Acc(acc_index, acc, days, df_o_acc, df_r_acc, df_d_acc, df_m_acc, df_a_acc, df_s_acc, df_sc_acc))
    acc_index += 1

    # print(accs[-1].delayedFlights)

# print("vars", sum([sum(acc.days[days.keys()[0]].inNeed) for acc in accs]))
# print("max delayed", max(acc.maxDelayed for acc in accs))
print("done", time.time() - comp_time)

solver = Solver(accs, days)
solver.run()

print(solver.matches)
print(len(solver.matches))

solver.set_constraints()



sol = solver.p.getSolution(solver.m)

print(sol)