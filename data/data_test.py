import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from datetime import timedelta
plt.rcParams["figure.figsize"] = (20,15)


df_saturation = pd.read_csv("data/ACCs_ActualCapacities/Saturation_1908.csv", sep= ";")
df_saturation.columns

df_saturation
def minutes_conversion(time):
    delta = timedelta(hours=int(time[:2]), minutes=int(time[3:5]), seconds=int(time[6:8]))
    total_seconds = delta.total_seconds()
    minutes = int(total_seconds  // 60 + 1)/60
    return minutes


ACC_new = df_saturation["ID"].apply(lambda acc: acc if type(acc)==str else "None")
df_saturation = df_saturation[df_saturation["ID"]!= "None"]
min_duration = df_saturation["Duration"].apply(lambda time: minutes_conversion(time))
df_saturation["min_duration"]= min_duration

lovv = df[df.ACC=="LOVVCTA"]
plt.plot(range(to_plot.shape[0]), lovv["Nb Sectors"])
plt.plot(range(to_plot.shape[0]), lovv.min_duration)