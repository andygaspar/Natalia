import time
import numpy as np
import pandas as pd
from model import Model, Area

#np.random.seed()
df_nations = pd.read_csv('data/icao_nations.csv')
df = pd.read_csv("data/first_test_4countries.csv")



nations_dict = dict(zip(df_nations.prefix, df_nations.country))
df["area"] = df.name.apply(lambda icao: nations_dict[icao[:2]])


areas = {}
areas_list = []
periods = dict(zip(range(24), range(24)))
index = 0
for area in df.area.unique():
    new_area = Area(area, index, df[df.area == area])
    areas_list.append(new_area)
    areas[area] = new_area
    index += 1

m = Model(areas_list, periods)
t = time.time()
m.run()
print(time.time()-t)
