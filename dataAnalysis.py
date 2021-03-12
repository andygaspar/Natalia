import pandas as pd
from os import listdir
from os.path import isfile, join

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





