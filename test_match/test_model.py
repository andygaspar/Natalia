import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
from ACC import acc as a
from ACC import set_accs
from DataAggregation import saturation
from Solver.solver import Solver
from test_match import test_cases

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
# df_saturation = saturation.get_saturation_df(tolerance)
# df_saturation = pd.read_csv("RowData/saturation_aggregated.csv")
# df_acc = pd.read_csv("RowData/accslist.csv")
# df_acc = pd.read_csv("RowData/listSmall.csv")


# df_regulation["acc"] = df_regulation.Airspace.apply(lambda a: a[:4])
# df_regulation.to_csv("RowData/regulations.csv", index_label=False, index=False)


# day
days = df_open.date.unique()


comp_time = time.time()

tolerances = [0, 20, 40]

for key in test_cases.cases.keys():
    for tolerance in tolerances:
        df_saturation = saturation.get_saturation_df(tolerance)
        #  list of accs of interest


        accs = set_accs.make_acc_list(test_cases.cases[key], df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity,
                                      df_saturation, df_sector_capacity, days)

        # print("vars", sum([sum(acc.days[days.keys()[0]].inNeed) for acc in accs]))
        # print("max delayed", max(acc.maxDelayed for acc in accs))
        print("setting environment", time.time() - comp_time, "\n")

        solving_time = time.time()
        solver = Solver(accs, days)
        solver.run()

        print("solving time", time.time() - solving_time, "\n")

        solver.make_df(key, tolerance)



