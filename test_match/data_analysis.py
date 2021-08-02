import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df_delayed = pd.read_csv("test_match/delayed_flights.csv")
df_regulation = pd.read_csv("test_match/regulations.csv")
df_regulation.columns

df_regulation_staffing = df_regulation[df_regulation.Reason == 'ATC Staffing']

most_busy = df_regulation_staffing.value_counts("Airspace")
accs = list(most_busy.index)
days = df_regulation_staffing.Date.unique()
df_dict = {}
df_dict["ACC"] = accs
for day in days:
    df_dict[day] = np.zeros(len(accs)).astype(int)



for day in days:
    df_reg_staff_day = df_regulation_staffing[df_regulation_staffing.Date == day]
    i = 0
    for acc in accs:
        num = df_reg_staff_day[df_reg_staff_day.Airspace == acc].shape[0]
        df_dict[day][i] = num
        i +=1

df = pd.DataFrame(df_dict)


plt.rcParams["figure.figsize"] = (40,20)

for acc in accs[:10]:
    to_plot = [df[(df.ACC == acc)][day].iloc[0] for day in days]
    plt.plot(days, to_plot, label=acc)



plt.legend()
plt.xticks(range(len(days)), days, rotation='vertical')
plt.show()



accs[:10]



































days = df_delayed.Date.unique()
day  = days[0]

df_d_day = df_delayed[df_delayed.Date == day]
df_reg_day = df_regulation[df_regulation.Reason == 'ATC Staffing']



pb = 0
ok = 0

reg_pb = []

for day in days:
    df_d_day = df_delayed[df_delayed.Date == day]
    df_reg_day = df_regulation[df_regulation.Date == day]
    df_reg_staff_day = df_reg_day[df_reg_day.Reason == 'ATC Staffing']

    for reg in df_reg_staff_day.Regulation:
        if df_d_day[df_d_day.MPR == reg].shape[0] > 40:
            pb += 1
            reg_pb.append(reg)
        else:
            ok += 1


reg = reg_pb[0]
df_delayed[df_delayed.MPR == reg].shape
sum(df_delayed[df_delayed.MPR == reg]["Total Delay"])

df_regulation[df_regulation.Regulation== reg]

df_regulation.shape
df_regulation.Regulation.unique().shape

m = max([df_delayed[df_delayed.MPR== r].shape[0] for r in reg_pb])

for r in reg:
    print()
