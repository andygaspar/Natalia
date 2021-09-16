import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from ACC import acc as a
from ACC import set_accs
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


# day
days = df_open.date.unique()


comp_time = time.time()

acc_list = df_open.acc.unique()

#  list of accs of interest
fra_ger_list = [a for a in acc_list if a[:2] == "ED"]

accs = set_accs.make_acc_list(fra_ger_list, df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity,
                              df_saturation, df_sector_capacity, days)

# print("vars", sum([sum(acc.days[days.keys()[0]].inNeed) for acc in accs]))
# print("max delayed", max(acc.maxDelayed for acc in accs))
print("setting environment", time.time() - comp_time, "\n")

solving_time = time.time()
solver = Solver(accs, days)
solver.run()

print("solving time", time.time() - solving_time, "\n")

solver.report()
