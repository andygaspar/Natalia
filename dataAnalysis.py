import d2 as d2
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from os import walk


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df_trajectories = pd.read_csv("data/trajectories.csv")
df_flights = pd.read_csv("data/one_day_flights.csv")
df_sectors = pd.read_csv("data/sectorhours.csv")
#
# print(df_trajectories)
print(df_flights)
# print(df_sectors)


class Flight:

    def __init__(self, row, trajectories):
        self.origin = row["O_D_A"][:4]
        self.destination = row["O_D_A"][5:9]
        self.aircraft = row["O_D_A"][10:]
        self.departure = row["dep_time_minutes"]
        self.departureTime = row["dep_time"]
        original_trajectory = row["original_trajectory"]
        self.original_trajectory = trajectories[trajectories["centroid"] == original_trajectory]

    def __repr__(self):
        return self.origin + " " + self.destination + " " + self.aircraft + "   departure: " + self.departureTime


flights = [Flight(df_flights.iloc[i], df_trajectories) for i in range(20)]

for flight in flights:
    print(flight.departureTime, flight.original_trajectory.iloc[:1])

from shapely.geometry import LineString
from shapely import wkb
for tb in d2.itertuples():
    t = wkb.loads(tb.trajectory, hex=True)
    numerics = np.array(t)
    if checkOD(numerics, origin, destination):
        t = LineString(numerics * np.array([1.0, 1.0, 0.0007]))
        dataset.append(t)
    else:
        d2.drop(tb.Index, inplace=True)






