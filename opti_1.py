import xpress as xp
from itertools import combinations
import time
import pandas as pd
import numpy as np

xp.controls.outputlog = 0

df_sh = pd.read_csv('data/sector_hours.csv')
df_geo = pd.read_csv('data/df_geo.csv')
df_mat = pd.read_csv('data/per_mat.csv')
df_geo_one = pd.read_csv('data/df_geo_one.csv')
df_sh_name = pd.read_csv('data/flight_sector_EU.csv')
df_nations = pd.read_csv('data/icao_nations.csv')

df_open = df_sh[df_sh["capacity"] > 0].copy()
df_open["icao_short"] = df_open["icao"].apply(lambda icao: icao[:4])
df_open["free"] = df_open.capacity - df_open.capacity_utilization
df_open["period"] = df_open.minute_start // 60
nations_dict = dict(zip(df_nations.prefix, df_nations.country))
df_open["area"] = df_open.icao_short.apply(lambda icao: nations_dict[icao[:2]])

df_test = df_open[(df_open.period >= 11) & (df_open.period <= 14)].copy()

acc_list = []
capacity = []
load = []
start_minute = []
for acc in df_test.area.unique():
    df_acc = df_test[df_test.area == acc]
    for start in df_acc.period.unique():
        start_minute.append(start)
        ddf = df_acc[df_acc.period == start]
        acc_list.append(acc)
        capacity.append(sum(ddf["capacity"]))
        load.append(sum(ddf["capacity_utilization"]))

acc_df = pd.DataFrame(columns=["area", "capacity", "load", "period"])
acc_df.area = acc_list
acc_df.capacity = capacity
acc_df.load = load
acc_df["period"] = start_minute
acc_df["free"] = acc_df.capacity - acc_df.load
acc_df["new_capacity"] = np.round(acc_df.capacity * 0.675).astype(int)

filtered = ['Germany (civil)', 'Iceland',
            'United Kingdom (and Crown dependencies)', 'Norway',
            'Spain (mainland section and Balearic Islands)',
            'France (Metropolitan France; including Saint-Pierre and Miquelon)',
            'Switzerland', 'Italy', 'Spain (Canary Islands)',
            'Belgium', 'Poland', 'Slovenia',
            'Czech Republic', 'Hungary', 'Bulgaria', 'Malta', 'Austria', 'Cypruslia', 'Estonia', 'Moldova']
            # 'Finland', 'Serbia and Montenegro', 'Croatia', 'Netherlands', 'Sweden',
            # 'Portugal (including the Azores and Madeira)', 'Slovakia', 'Ireland',
            # 'Denmark and the Faroe Islands', 'Bosnia and Herzegovina', 'Romania', 'Luxembourg', 'Latvia', 'Lithuania']
acc_df = acc_df[acc_df.area.isin(filtered)]

print(acc_df)


class Area:
    def __init__(self, name, index, df):
        self.name = name
        self.index = index
        self.capacity = dict(zip(df.period, df.new_capacity))
        self.load = dict(zip(df.period, df.load))
        self.matches = []


areas = {}
areas_list = []
periods = dict(zip([0, 1, 2], [11,12, 13]))
index = 0
for area in acc_df.area.unique():
    new_area = Area(area, index, acc_df[acc_df.area == area])
    areas_list.append(new_area)
    areas[area] = new_area
    index += 1

matches = np.array(list(combinations(areas_list, 2)))

p = xp.problem()

e = np.array([[xp.var(vartype=xp.integer) for _ in periods] for _ in areas_list])
y = np.array([[[xp.var(vartype=xp.integer) for _ in periods] for _ in areas_list] for _ in areas_list])
m = np.array([xp.var(vartype=xp.binary) for _ in matches])
p.addVariable(e, y, m)

for a in range(len(areas_list)):
    for t in periods.keys():
        p.addConstraint(areas_list[a].load[periods[t]] - areas_list[a].capacity[periods[t]] - xp.Sum(
            y[a, j, t] for j in range(len(areas_list))) + xp.Sum(y[j, a, t] for j in range(len(areas_list))) <= e[a, t])
        available = 1 if (areas_list[a].load[periods[t]] - areas_list[a].capacity[periods[t]]) < 0 else 0
        # print(areas_list[a].name, available, areas_list[a].load[periods[t]], areas_list[a].capacity[periods[t]])
        p.addConstraint(xp.Sum(y[j, a, t] for j in range(len(areas_list))) <= 10000 * available)
        p.addConstraint(xp.Sum(y[a, j, t] for j in range(len(areas_list))) <= 10000 * (1-available))
        p.addConstraint(e[a, t] >= 0)

    idxs = [i for i in range(len(matches)) if
            matches[i][0].name == areas_list[a].name or matches[i][1].name == areas_list[a].name]

    p.addConstraint(xp.Sum(m[i] for i in idxs) <= 1)

for i in range(len(matches)):
    a = matches[i][0].index
    b = matches[i][1].index

    p.addConstraint(xp.Sum(y[a, b, t] + y[b, a, t] for t in periods.keys()) <= 10000 * m[i])

p.setObjective(xp.Sum(xp.Sum(e[a, t] for t in periods.keys()) for a in range(len(areas_list)))
               + 0.001*xp.Sum(xp.Sum(xp.Sum(y[a, b, t] for t in periods.keys()) for a in range(len(areas_list)))
                        for b in range(len(areas_list))), sense=xp.minimize)

t = time.time()
p.solve()
print("time ", time.time() - t)

sol = p.getSolution(y)

initial = sum(
    [a.load[t] - a.capacity[t] if a.load[t] - a.capacity[t] > 0 else 0 for a in areas_list for t in periods.values()])
print("initial: ", initial, "   final: ", int(p.getObjVal()))

solm = p.getSolution(m)
print(solm)
for i in range(len(solm)):
    if solm[i] > 0.9:
        print(matches[i][0].name, matches[i][1].name)
        for j in range(2):
            print(sol[matches[i][0].index, matches[i][1].index, j], sol[matches[i][1].index, matches[i][0].index, j])
            print(matches[i][0].load[periods[j]] - matches[i][0].capacity[periods[j]],
                  matches[i][1].load[periods[j]] - matches[i][1].capacity[periods[j]])
        print()
