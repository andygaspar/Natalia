import pandas as pd
import numpy as np
from Funs.fix_date import fix_date

def fix_hour_start(df):
    return [time//60 * 60 for time in df.start]


def is_in_interval(start, end, df):
    cond1 = (df.start >= start) & (df.start < end)
    cond2 = (df.end > start) & (df.end <= end)
    cond3 = (df.start <= start) & (df.end >= end)
    return df[cond1 | cond2 | cond3]


open_df = pd.read_csv("RowData/opening_schemes.csv")

# new_start = fix_hour_start(open_df)
# open_df.start = new_start

days = open_df.date.unique()
intervals = [i for i in range(0, 1441, 60)]

mother_accs = open_df.mother_acc.unique()

# deal clusters ****************

# clusters = pd.DataFrame(columns=open_df.columns)
# for acc in mother_accs:
#     acc_df = open_df[open_df.mother_acc == acc]
#     if acc_df.acc.unique().shape[0] > 1:
#         clusters = pd.concat([clusters, acc_df], ignore_index=True)
#
# clus_mother_acc = clusters.mother_acc.unique()

aggregated_open_schemes = pd.DataFrame(columns=["acc", "date", "start", "n_sectors"])

print(mother_accs.shape[0])
for acc in mother_accs:

    df_acc = open_df[open_df.mother_acc == acc]
    for date in days:
        df_acc_day = df_acc[df_acc.date == date]
        for i in range(len(intervals)-1):
            n_sectors = 0
            df_clusters = is_in_interval(intervals[i], intervals[i+1], df_acc_day)
            clusts = df_clusters.acc.unique()
            for c in clusts:
                df_cluster = df_clusters[df_clusters.acc == c]
                n_sectors += max(df_cluster.n_sectors)
            aggregated_open_schemes = aggregated_open_schemes.append(
                {"acc": acc, "date": date, "start": intervals[i], "n_sectors": n_sectors}, ignore_index=True)

aggregated_open_schemes.date = aggregated_open_schemes.date.apply(fix_date)
aggregated_open_schemes.to_csv("RowData/opening_aggregated_egcc.csv", index_label=False, index=False)





