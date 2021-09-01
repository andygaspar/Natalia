import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

reg = pd.read_csv("RowData/regulations.csv")
reg = reg[(reg.Reason == "ATC Capacity") | (reg.Reason == "ATC Staffing")]
reg["duration"] = reg.end - reg.start

df_acc = pd.DataFrame(columns=["acc", "frequency", "delay_mean", "delay_std", "start_mean", "end_mean", "duration_mean",
                               "start_std", "end_std", "duration_std"])


plt.rcParams["figure.figsize"] = (20,20)

for acc in reg.ID.unique():
    df = reg[reg.ID == acc]
    frequency = df.shape[0]
    delay = df.Delay.mean()
    delay_std = df.Delay.std()

    start_mean = df.start.mean()
    end_mean = df.end.mean()
    dur_mean = df.duration.mean()

    start_std = df.start.std()
    end_std = df.end.std()
    dur_std = df.duration.std()

    df_acc = df_acc.append({"acc": acc, "frequency": frequency, "delay_mean": delay, "delay_std": delay_std,
                            "start_mean": start_mean, "end_mean": end_mean, "duration_mean": dur_mean,
                           "start_std": start_std, "end_std": end_std, "duration_std": dur_std}, ignore_index=True)

df_acc["start"] = np.round(df_acc.start_mean/60)
df_acc["end"] = np.round(df_acc.end_mean/60)

freq = df_acc.frequency.to_list()
delays = df_acc.delay_mean.to_list()
accs = df_acc.acc.to_list()


plt.scatter(freq, delays)

for i, txt in enumerate(accs):
    plt.annotate(accs[i], (freq[i], delays[i]))

plt.show()


#frequency of the sectors