import pandas as pd
import numpy as np

df_delayed = pd.read_csv("RowData/delayed_flights_refined_.csv")
df_delayed["start"] = df_delayed["Off BlockTime"].apply(lambda t: 60*int(t[:2]) + int(t[3:5]))
df_delayed["arrival"] = df_delayed["Arrival Time"].apply(lambda t: 60*int(t[:2]) + int(t[3:5]))
df_delayed["regulation_time"] = ((df_delayed.arrival + df_delayed.start)/2 - df_delayed["Delay flight"]).astype(int)


df_delayed.to_csv("RowData/delayed_flights.csv", index_label=False, index=False)