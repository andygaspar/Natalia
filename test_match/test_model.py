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

print(sum(acc.totalDelay for acc in accs))


d = solver.delaySolution

k = 0

# for j in range(len(d)):
#     for i in range(len(d[j])):
#         for g in range(len(d[j][i])):
#             for t in range(len(d[j][i][g])):
#                 if d[j][i][g][t] > 0.5:
#                     if not accs[j].days[g].inNeed[t]:
#                         print("an issue")
#                     if accs[i].days[g].regulated[t]:
#                         print("an issue")
#                     # print(d[j][i][g][t])
#                     # print(accs[j].days[g].delayedFlights[t], sum(accs[j].days[g].delayedFlights[t]))
#                     # print(accs[j].days[g].delays[t])
#                     # print(d[i][j][g][t])
#                     # print("\n")
#                     if d[i][j][g][t] > 0.5:
#                         print("issue")
#
np.sum(d[2])
tot = 0
for i in range(len(d[2])):
    for g in range(len(d[2][i])):
        for t in range(len(d[2][i][g])):
            if d[2][i][g][t] > 0.5:
                if not accs[2].days[g].inNeed[t]:
                    print("an issue")
                if accs[i].days[g].regulated[t]:
                    print("an issue")
                # print(d[2][i][g][t])
                # print(accs[2].days[g].delayedFlights[t], sum(accs[2].days[g].delayedFlights[t]))
                # print(accs[2].days[g].delays[t])
                tot += accs[2].days[g].delays[t]
                # print(d[i][2][g][t], accs[i].days[g].spareCapacity[t]*accs[i].sector_capacity)
                # print("\n")
                print(i)
                if d[i][2][g][t] > 0.5:
                    print("issue")


accs[2].days[0].delays

solver.combinationSolution

solver.get_match(accs[2], accs[0])
accs


np.sum([d[2, 0, day, t] for day in range(len(days)) for t in range(24)])