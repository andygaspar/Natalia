import csv
import numpy as np
import pandas as pd
from Actual_capacity import irregular

intervals_num = [i for i in range(0, 1440, 60)]




import os

path = 'Actual_capacity'

files = os.listdir(path)
files = [file for file in files if file != "actual_conversion.py" and file != "irregular.py"]

df_actual = pd.DataFrame(columns=["acc"] + [str(start) for start in intervals_num])
index = 0
for f in files:
    if f != "okEDYY.csv" and f != "okLFMM.csv" and f != "exceptions" and f != "__pycache__":
        print(f)
        with open('Actual_capacity/'+f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            i = 0
            line = 0
            long = False
            read = False
            read_odd = False
            actual_capacities = []
            actual_capacities_odd = []
            df_entry = {}
            df_entry["acc"] = [f[2:-4]]

            if f == "okUBBA.csv":
                print(f)


            for row in csv_reader:
                if line > 60:
                    long = True
                line += 1
                if row[0] == "0:00" and row[1] == "0:59":
                    read = True
                if read:

                    for j in range(len(row)):
                        if row[j][-2:] == "59":
                            actual_capacities.append(int(row[j+1]))

                    # print(intervals_num[i], actual_capacities, int(np.round(np.mean(actual_capacities))))

                    df_entry[str(intervals_num[i])] = [np.round(np.mean(actual_capacities))]
                    actual_capacities = []
                    i += 1
                if row[0] == "23:00":
                    read = False

                if row[0] == "0:00" and row[1] == "0:29":
                    read_odd = True

                if read_odd:
                    if row[0][-3:] == ":00":
                        for j in range(len(row)):
                            if len(row[j]) > 1 and row[j][-1:] == "9" and row[j][-3] == ":":
                                actual_capacities.append(int(row[j + 1]))

                    elif row[0][-3:] == ":30":

                        for j in range(len(row)):

                            if len(row[j]) > 1 and row[j][-1:] == "9" and row[j][-3] == ":":
                                actual_capacities_odd.append(int(row[j + 1]))
                        actual_capacities = (np.array(actual_capacities) + np.array(actual_capacities_odd))/2
                        df_entry[str(intervals_num[i])] = [np.round(np.mean(actual_capacities))]
                        # print(intervals_num[i], actual_capacities, int(np.round(np.mean(actual_capacities))))
                        actual_capacities, actual_capacities_odd = [], []
                        i += 1

                        if row[0] == "23:30":
                            read_odd = False

                index += 1

            df_actual = df_actual.append(pd.DataFrame(df_entry), ignore_index=True)

edyy, lfmm = irregular.edyy_lfmm()

df_actual = df_actual.append(pd.DataFrame(edyy), ignore_index=True)
df_actual = df_actual.append(pd.DataFrame(lfmm), ignore_index=True)

for i in intervals_num:
    df_actual[str(i)] = df_actual[str(i)].astype(int)


print(df_actual)

df_actual.to_csv("RowData/actual_capacity.csv", index_label=False, index=False)
