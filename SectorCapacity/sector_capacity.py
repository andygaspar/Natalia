import pandas as pd
import numpy as np

df_sector = pd.read_csv("RowData/Sector/sector_capacity_all.csv")

accs = []

for acc in df_sector.SectorID:
    if acc[:5] == "ENOSE":
        accs.append("ENOSE")
    elif acc[:5] == "ENOSW":
        accs.append("ENOSW")
    else:
        accs.append(acc[:4])

df_sector["acc"] = accs
np.sort(df_sector.acc.unique())

df_acc_capacity = pd.DataFrame(columns=["acc", "sector_capacity"])

for acc in df_sector.acc.unique():
    df = df_sector[df_sector.acc == acc]
    mean_capacity = np.round(df.Capacity.mean())
    df_acc_capacity = df_acc_capacity.append({"acc": acc, "sector_capacity": mean_capacity}, ignore_index=True)

df_acc_capacity.sector_capacity = df_acc_capacity.sector_capacity.astype(int)
df_acc_capacity.to_csv("RowData/sector_capacity.csv", index_label=False, index=False)
