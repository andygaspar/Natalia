import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

reg = pd.read_csv("RowData/regulations.csv")
reg = reg[(reg.Reason == "ATC Capacity") | (reg.Reason == "ATC Staffing")]
reg["start"] = reg.Period.apply(lambda p: int(p[:2])*60 + int(p[3:5]))
reg["end"] = reg.Period.apply(lambda p: int(p[6:8])*60 + int(p[9:11]))
reg["duration"] = reg.end - reg.start

reg.to_csv("RowData/regulations.csv", index_label=False, index=False)

df_acc = pd.DataFrame(columns=["acc", "frequency", "delay_mean", "delay_std", "start_mean", "end_mean", "duration_mean",
                               "start_std", "end_std", "duration_std"])


# reg.to_csv("DataRow/")
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

df_acc_plot = df_acc[(df_acc.frequency >= 100) | (df_acc.delay_mean >= 300)]


freq = df_acc_plot.frequency.to_list()
delays = df_acc_plot.delay_mean.to_list()
accs = df_acc_plot.acc.to_list()

plt.rcParams["figure.figsize"] = (30, 30)
plt.rcParams.update({'font.size': 22})

plt.scatter(freq, delays, s=100)
plt.xlabel("frequency")
plt.ylabel("delay")
for i, txt in enumerate(accs):
    plt.annotate(accs[i], (freq[i], delays[i] + 5), ha="center")

plt.show()

# df_acc.to_csv("Analysis/regulation_analysis.csv", index_label=False, index=False)

#frequency of the sectors