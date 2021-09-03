import pandas as pd
import numpy as np

df_sat = pd.read_csv("RowData/saturations.csv")
df_sat.fillna(value=np.nan, inplace=True)

accs = []

threshold = 40

for acc in df_sat.ID:
    if acc == "ENOSECTA":
        accs.append("ENOSE")
    elif acc == "ENOSWCTA":
        accs.append("ENOSW")
    else:
        accs.append(acc[:4])

df_sat["acc"] = accs
aggregated_saturations = pd.DataFrame(columns=["acc", "date", "start", "n_sectors"])

acc_list = df_sat.acc.unique()
days = df_sat.Date.unique()

intervals = list(df_sat.columns)[7:-1]
intervals_num = [i for i in range(0, 1441, 60)]

print(acc_list.shape[0])
j = 0
for acc in acc_list:
    print(acc, j)
    df_acc = df_sat[df_sat.acc == acc]
    for date in days:
        df_acc_day = df_acc[df_acc.Date == date]
        num = 0
        for i in intervals:
            n_sectors = 0
            df_acc_interval = df_acc_day[i]
            num_available = df_acc_interval[df_acc_interval < threshold].shape[0]
            aggregated_saturations = aggregated_saturations.append(
                {"acc": acc, "date": date, "start": intervals_num[num], "n_sectors": num_available}, ignore_index=True)
            num += 1
    j+=1

aggregated_saturations.to_csv("RowData/saturation_aggregated.csv", index_label=False, index=False)
