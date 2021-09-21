import pandas as pd
import numpy as np

df_delayed = pd.read_csv("RowData/delayed_flights_refined_.csv")
df_delayed["start"] = df_delayed["Off BlockTime"].apply(lambda t: 60*int(t[:2]) + int(t[3:5]))
df_delayed["arrival"] = df_delayed["Arrival Time"].apply(lambda t: 60*int(t[:2]) + int(t[3:5]))
start = df_delayed["start"]
arrival = df_delayed["arrival"]
delay = df_delayed["Delay flight"]
regulation_time = [int((start[i] + arrival[i])/2 - delay[i])
                   if start[i] < arrival[i] else int((start[i] - 1440 + arrival[i])/2 - delay[i])
                   for i in range(start.shape[0])]

df_delayed["regulation_time"] = regulation_time
df_delayed["regulation_time"] = df_delayed["regulation_time"].apply(lambda t: t if t > 0 else 1440 + t)


df_delayed.to_csv("RowData/delayed_flights.csv", index_label=False, index=False)