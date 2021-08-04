import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df_delayed = pd.read_csv("test_match/delayed_flights_15_min.csv")
df_regulation = pd.read_csv("test_match/regulations.csv")
df_open = pd.read_csv("RowData/ACCs_ActualCapacities/opening_schemes.csv")
s



# day
df_regulation_staffing = df_regulation[df_regulation.Reason == 'ATC Staffing']
days = df_regulation_staffing.Date.unique()
day = days[0]

df_d_day = df_delayed[df_delayed.Date == day]
df_r_day = df_regulation_staffing[df_regulation_staffing.Date == day]
df_o_day = df_open[df_open.Date == day]


# regulation
regs = df_r_day.Regulation.unique()
reg = regs[1]

df_reg = df_r_day[df_r_day.Regulation == reg]
df_d_day_r = df_d_day[df_d_day.MPR == reg]

# *****
dod = sorted(df_o_day.ACC.unique())
df_r_day.ID.unique()
i = 2
print(df_r_day.ID.unique()[i])
print(df_r_day.ID.unique()[i] in df_o_day.ACC.unique(), "\n", df_o_day.ACC.unique())


