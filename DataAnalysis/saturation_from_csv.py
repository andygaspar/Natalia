import math

import pandas as pd
import numpy as np
import math
import csv
from os import walk


path = "data/test"
_, _, filenames = next(walk(path))
print(filenames)

final_df = pd.DataFrame(columns=["name", "capacity", "demand", "period"])

for file in filenames:
    df = pd.read_csv(path + "/" + file)
    df.columns = ["name"] + list(df.columns[1:])



    name = [df.name[0]] * len(df.columns[2:])

    capacity =[]
    demand = []
    periods = list(range(len(df.columns[2:])))
    for column in df.columns[2:]:
        cap = 0
        dem = 0

        period = 0
        for item in df[column]:

            if type(item) == str:

                end = item.index(" (")
                c = int(item[:end])
                cap += c

                start = item.index("(") + 1
                end = item.index(" %", start)
                d = np.floor(c*int(item[start:end])/100).astype(int)
                dem += d

        capacity.append(cap)
        demand.append(dem)

    new_df = pd.DataFrame({"name": name, "capacity": capacity, "demand": demand, "period": periods})

    final_df = pd.concat([final_df, new_df])

# final_df.to_csv("data/first_test_4countries.csv")

# print(final_df[final_df.capacity < final_df.demand])
