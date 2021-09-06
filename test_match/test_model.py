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
df_open = df_open[~df_open.acc.isin(["EHMC", "EYKA", "EYPA", "EYSA", "EYVI", "LHKR", "UMKK", "UMMV"])] #not considered
df_air_capacity = pd.read_csv("RowData/airspace_capacity.csv")
df_actual_capacity = pd.read_csv("RowData/actual_capacity.csv")
# df_saturation = saturation.get_saturation_df(tolerance)
df_saturation = pd.read_csv("RowData/saturation_aggregated.csv")
# df_acc = pd.read_csv("RowData/accslist.csv")
# df_acc = pd.read_csv("RowData/listSmall.csv")


df_regulation["acc"] = df_regulation.Airspace.apply(lambda a: a[:4])
df_regulation.to_csv("RowData/regulations.csv", index_label=False, index=False)

def get_day_df(d, df_delayed, df_regulation, df_open, df_saturation):
    df_d_d = df_delayed[df_delayed.Date == d]
    df_r_d = df_regulation[df_regulation.Date == d]
    df_o_d = df_open[df_open.date == d]
    df_s_d = df_saturation[df_saturation.date == d]

    return df_d_d, df_r_d, df_o_d, df_s_d


def get_acc_df(a, df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity, df_sat_day):
    df_r_acc = df_regulation[df_regulation.acc == a]
    df_d_acc = df_delayed[df_delayed.MPR.isin(df_r_acc.Regulation)]
    df_o_acc = df_open[df_open.acc == a]
    df_c_acc = df_air_capacity[df_air_capacity.acc == a]
    df_a_acc = df_actual_capacity[df_actual_capacity.acc == a]
    df_s_acc = df_sat_day[df_sat_day.acc == a]

    return df_d_acc, df_r_acc, df_o_acc, df_c_acc, df_a_acc, df_s_acc


# day
days = df_open.date.unique()
day = days[0]

interval_size = 60
intervals = [interval_size*i for i in range(1440//interval_size + 1)]

comp_time = time.time()

acc_list = df_open.acc.unique()
accs = []
acc_index = 0
for acc in acc_list:
    df_d_day, df_r_day, df_o_day, df_s_day = get_day_df(day, df_delayed, df_regulation, df_open, df_saturation)
    df_d_acc, df_r_acc, df_o_acc, df_m_acc, df_a_acc, df_s_acc = get_acc_df(acc, df_d_day, df_r_day, df_o_day,
                                                                  df_air_capacity, df_actual_capacity, df_s_day)
    accs.append(a.Acc(acc_index, acc, interval_size, intervals, df_o_acc, df_r_acc,
                      df_d_acc, df_m_acc, df_a_acc, df_s_acc))
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





