import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
from datetime import timedelta


def hours_conversion(time):
    time = time[-8:]
    delta = timedelta(hours=int(time[:2]), minutes=int(time[3:5]), seconds=int(time[6:8]))
    total_seconds = delta.total_seconds()
    hours = int(total_seconds // 60 + 1) / 60
    return hours


def set_configuration_df():
    df_open = pd.read_csv("RowData/ACCs_ActualCapacities/OpeningSchemes.csv", sep=",", low_memory=False)

    #cleaning None in ACC
    ACC_new = df_open["ACC"].apply(lambda acc: acc if type(acc) == str else "None")
    df_open.ACC = ACC_new
    df_open = df_open[df_open["ACC"]!= "None"]

    #cleaning None in duration (in datatime format)
    duration_new = df_open["Duration"].apply(lambda time: time if type(time) == str else "None")
    df_open.Duration = duration_new
    df_open = df_open[df_open["Duration"] != "None"]

    #making hours
    min_duration = df_open["Duration"].apply(lambda time: hours_conversion(time))
    df_open["min_duration"] = min_duration


    #row renaming and nan removal
    df_open.columns = ['acc', 'configuration', 'date', 'duration_datetime', 'end', 'start','n_sectors', 'duration']
    df_open = df_open[~df_open.n_sectors.isna()]

    #transformation of n_sec in int
    df_open.n_sectors = df_open.n_sectors.astype(int)

    return df_open




