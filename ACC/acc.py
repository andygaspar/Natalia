import numpy as np

# class Sector:
#     def __init__(self, name, capacity, time_period):
#         self.name = name
#         self.capacity = capacity
#         self.open = np.array([False for _ in len(time_period)])

class Acc:
    def __init__(self, name, sectors: list[Sector]):
        self.name = name
        self.sectors = sectors
        self.airspaceCapacity = len(sectors)
        self.av