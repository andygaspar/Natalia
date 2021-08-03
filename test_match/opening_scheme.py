import pandas as pd
import numpy as np
from datetime import timedelta




df_regulation = pd.read_csv("RowData/regulations.csv")
df_open = pd.read_csv("RowData/opening_scheme.csv")
df_acc = pd.read_csv("RowData/acc.csv")




df_regulation_staffing = df_regulation[df_regulation.Reason == 'ATC Staffing']
days = df_regulation_staffing.Date.unique()
day = days[10]

df_o_day = df_open[df_open.Date == day]
df_r_day = df_regulation_staffing[df_regulation_staffing.Date == day]

for acc in df_r_day.ID.unique():
    if acc not in list(df_o_day.ACC.unique()):
        print(acc)


df_delayed = pd.read_csv("RowData/delayed_flights.csv")
