import pandas as pd
import numpy as np
from datetime import timedelta


def hours_conversion(time):
    delta = timedelta(hours=int(time[:2]), minutes=int(time[3:5]))
    total_seconds = delta.total_seconds()
    return total_seconds//60


df_regulation = pd.read_csv("RowData/regulations.csv")
df_open = pd.read_csv("RowData/FromRnest/o.csv", sep="\t")
df_open["Nb Sectors"] = df_open["Nb Sectors"].fillna(0)
df_open["Nb Sectors"] = df_open["Nb Sectors"].astype(int)
df_open.Start = df_open.Start.apply(lambda t: "0" + t if len(t) == 7 else t)
df_open["start"] = df_open.Start.apply(hours_conversion)


df_open[df_open.Start.isna()]


len(df_open.iloc[0].Start)
# day
df_regulation_staffing = df_regulation[df_regulation.Reason == 'ATC Staffing']
days = df_regulation_staffing.Date.unique()
day = days[10]

df_o_day = df_open[df_open.Date == day]


o1 = pd.read_csv("RowData/FromRnest/OpeningScheme_1907.csv")
o2 = pd.read_csv("RowData/FromRnest/OpeningScheme_1908.csv")


nb_sec = pd.read_csv("RowData/FromRnest/Conf_Nb_Sectors.csv")

op = pd.concat([o1, o2], ignore_index=True)

op["n_sectors"] = []
err_sec = []
err = 0
for i in range(op.shape[0]):
    mm = nb_sec[(nb_sec.ACC == op.iloc[i].ACC) & (nb_sec.Configuration == op.iloc[i].Configuration)].Nb_Sectors.values
    if len(mm) == 0:
        err += 1
        err_sec.append(op.iloc[i].ACC)


accs = op.ACC.unique()
n_accs = nb_sec.ACC.unique()

not_ok = []
for acc in accs:
    if acc not in list(n_accs):
        not_ok.append(acc)

not_ok

open_ok = op[~op.ACC.isin(not_ok)].copy()
open_ok.Configuration = open_ok.Configuration.apply(lambda conf: conf.replace(",", "."))

err_sec = []
err = 0
for i in range(open_ok.shape[0]):
    if i%100==0:
        print(i)
    mm = nb_sec[(nb_sec.ACC == open_ok.iloc[i].ACC) & (nb_sec.Configuration == open_ok.iloc[i].Configuration)].Nb_Sectors.values
    if len(mm) == 0:
        err += 1
        err_sec.append([open_ok.iloc[i].ACC, open_ok.iloc[i].Configuration])


a = "fhjkdlsòa"

a = a.replace(",", "9")

open_ok_ok = open_ok

for exception in err_sec:
    open_ok_ok = open_ok_ok[~((open_ok_ok.ACC == exception[0]) & (open_ok_ok.Configuration == exception[1]))]



err_sec = []
err = 0
for i in range(open_ok_ok.shape[0]):
    if i%100==0:
        print(i)
    mm = nb_sec[(nb_sec.ACC == open_ok_ok.iloc[i].ACC) & (nb_sec.Configuration == open_ok_ok.iloc[i].Configuration)].Nb_Sectors.values
    if len(mm) == 0:
        print("nooooo")

vals = []

for i in range(open_ok_ok.shape[0]):
    if i%100==0:
        print(i)
    mm = nb_sec[(nb_sec.ACC == open_ok_ok.iloc[i].ACC) & (nb_sec.Configuration == open_ok_ok.iloc[i].Configuration)].Nb_Sectors.values[0]
    vals.append(mm)

v = [i[0] for i in vals]

open_ok_ok["n_sectors"] = v

open_ok_ok["start"] = open_ok_ok.Start.apply(hours_conversion)
open_ok_ok.start = open_ok_ok.start.astype(int)

open_ok_ok["end"] = open_ok_ok.End.apply(hours_conversion)
open_ok_ok.end = open_ok_ok.end.astype(int)

open_ok_ok.to_csv("RowData/opening_scheme.csv", index_label=False, index=False)