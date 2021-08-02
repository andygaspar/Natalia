import numpy as np

# class Sector:
#     def __init__(self, name, capacity, time_period):
#         self.name = name
#         self.capacity = capacity
#         self.open = np.array([False for _ in len(time_period)])

class Acc:
    def __init__(self, name, actual_capacity, delayed_flights, airspace_capacity, available_capacity):
        self.name = name
        self.actualCapacity = actual_capacity
        self.delayedFlights = delayed_flights
        self.airspaceCapacity = airspace_capacity
        self.availableCapacity = available_capacity

        self.spareCapacity = None

