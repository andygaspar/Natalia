import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from ACC import acc as a
from ACC import set_accs
from DataAggregation import saturation
from Solver.solver_1 import Solver1
from tests import test_cases

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df_delayed = pd.read_csv("RowData/delayed_flights.csv")
df_regulation = pd.read_csv("RowData/regulations.csv")
df_open = pd.read_csv("RowData/opening_aggregated.csv")
df_open = df_open[
    ~df_open.acc.isin(["EHMC", "EYKA", "EYPA", "EYSA", "EYVI", "LHKR", "UMKK", "UMMV", "EGCC"])]  # not considered
df_air_capacity = pd.read_csv("RowData/airspace_capacity.csv")
df_actual_capacity = pd.read_csv("RowData/actual_capacity.csv")
df_sector_capacity = pd.read_csv("RowData/sector_capacity.csv")

# df_saturation = pd.read_csv("RowData/saturation_aggregated.csv")

# day
days = df_open.date.unique()
days = [days[23]]

comp_time = time.time()

tolerances = [40]
cap_corrections = [1]

# test_cases.cases["VIRTUAL_CENTER"] = df_open.acc.unique()
france = {"FRANCE": test_cases.cases["FRANCE"]}

for key in france:
    df = None
    df_interactions = None
    for tolerance in tolerances:
        for cap_correction in cap_corrections:
            print(key, tolerance)
            df_saturation = saturation.get_saturation_df(tolerance, test_cases.cases[key])

            accs = set_accs.make_acc_list(test_cases.cases[key], df_delayed, df_regulation, df_open, df_air_capacity,
                                          df_actual_capacity, df_saturation, df_sector_capacity, days, cap_correction)

            # print("vars", sum([sum(acc.days[days.keys()[0]].inNeed) for acc in accs]))
            # print("max delayed", max(acc.maxDelayed for acc in accs))
            print("setting environment", time.time() - comp_time)

            solving_time = time.time()
            solver = Solver1(accs, days)
            solver.run()

            print("solving time", time.time() - solving_time)

            df = solver.make_df(key, tolerance, cap_correction, df)
            print("\n\n")
            countries_dict = dict((zip(test_cases.countries_case[key], [test_cases.country_acc[country] for country
                                                                        in test_cases.countries_case[key]])))
            df_interactions = solver.make_interaction_df(countries_dict, tolerance, cap_correction, df_interactions)


    # df.to_csv("Results/Virtual/" + key + ".csv", index_label=False, index=False)
    # df_interactions.to_csv("Results/Virtual/interactions" + key + ".csv", index_label=False, index=False)
import matplotlib.pyplot as plt

for d in range(solver.delaySolution.shape[2]):
    print(d, sum([solver.delaySolution[acc_a.index,acc_b.index,d,t] for acc_a in solver.accs for acc_b in solver.accs for t in range(solver.intervalsNum)]))

solver.delaySolution
for acc in solver.accs:
    # plt.bar(range(24), acc.days[0].delays, tick_label=range(1, 25))
    # plt.savefig("Figures/"+acc.name+"delay.png")
    # plt.clf()
    # plt.bar(range(24), acc.days[0].spareCapacity)
    # plt.savefig("Figures/"+acc.name+"spare.png")
    # plt.clf()

    pippo = []
    for t in range(solver.intervalsNum):
        for acc_b in solver.accs:
            if solver.delaySolution[acc_b.index, acc.index, 0, t] > 0:
                pippo.append((t, acc.name, acc_b.name))
    print(pippo)

for acc in solver.accs:
    print(acc.name)
    print(acc.days[0].spareCapacity)

pippo = []
for acc in solver.accs:
    for t in range(solver.intervalsNum):
        for acc_b in solver.accs:
            if solver.delaySolution[acc.index, acc_b.index, 0, t] > 0:
                pippo.append((t, acc.name, acc_b.name))

pippo


for t in range(solver.intervalsNum):
    print(solver.delaySolution[:, :, 0, t], "\n")


"""
LFRR 72 1830.0 LFBB 1 39 1426.0
LFMM 64 1458.0 LFBB 1 39 1236.0
LFRR 72 1830.0 LFFF 6 27 1830.0
LFMM 64 1458.0 LFFF 6 27 1458.0
LFMM 64 1458.0 LFEE 2 28 1413.0
LFRR 72 1830.0 LFEE 2 28 1698.0
"""

import matplotlib.pyplot as plt

plt.bar(range(6), [1426, 1236, 1830, 1458, 1413, 1698], tick_label=["BR", "BM", 'FR', 'FM', 'EM', 'ER'])
plt.savefig("Figures/spare.png")


plt.bar(range(2), [ 1830, 1458], tick_label=["r", "m"])
plt.savefig("Figures/delay.png")

3288-3156


1698+1458