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


comp_time = time.time()

tolerances = [0, 20, 40]
cap_corrections = [1, 0.95, 0.9]

# test_cases.cases["VIRTUAL_CENTER"] = df_open.acc.unique()

for key in list(test_cases.cases.keys())[-1:]:
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


    df.to_csv("Results/Virtual/" + key + ".csv", index_label=False, index=False)
    df_interactions.to_csv("Results/Virtual/interactions" + key + ".csv", index_label=False, index=False)
