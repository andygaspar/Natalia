import csv
import numpy as np
import pandas as pd


def edyy_lfmm():
    intervals_num = [i for i in range(0, 1440, 60)]

    df_actual = pd.DataFrame(columns=["acc"] + [str(start) for start in intervals_num])

    df_entry = {}
    # df_entry["acc"] = "EDYY"
    edyy_mat = np.zeros((24, 3))

    files = ['okEDYY.csv', 'okEDYY_1.csv', 'okEDYY_2.csv']

    for i in range(3):
        with open('Actual_capacity/exceptions/' + files[i]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                hour = row[0].split(":")[0]
                if hour in list(df_entry.keys()):
                    df_entry[str(intervals_num[int(hour)])].append(int(row[2]))
                else:
                    df_entry[str(intervals_num[int(hour)])] = [int(row[2])]

                hour = row[5].split(":")[0]
                if hour in list(df_entry.keys()):
                    df_entry[str(intervals_num[int(hour)])].append(int(row[7]))
                else:
                    df_entry[str(intervals_num[int(hour)])] = [int(row[7])]

        for key in df_entry.keys():
            df_entry[key] = np.round(np.mean(df_entry[key]))

        edyy_mat[:, i] = np.array([value for value in df_entry.values()])

        df_entry = {}

    entry_edyy = {}
    entry_edyy["acc"] = "EDYY"

    for i in range(24):
        entry_edyy[str(intervals_num[i])] = [sum(edyy_mat[i, :])]



    df_entry = {}
    # df_entry["acc"] = "EDYY"
    lfmm_mat = np.zeros((24, 2))

    files = ['okLFMM_1.csv', 'okLFMM_2.csv']

    for i in range(2):
        with open('Actual_capacity/exceptions/' + files[i]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            print(i)
            for row in csv_reader:
                if row[0] != "":
                    hour = row[0].split(":")[0]
                    if hour in list(df_entry.keys()):
                        df_entry[str(intervals_num[int(hour)])].append(int(row[2]))
                    else:
                        df_entry[str(intervals_num[int(hour)])] = [int(row[2])]

                if row[4] != "":
                    # print("jfkdsl", row[7])
                    hour = row[4].split(":")[0]
                    if hour in list(df_entry.keys()):
                        df_entry[str(intervals_num[int(hour)])].append(int(row[6]))
                    else:
                        df_entry[str(intervals_num[int(hour)])] = [int(row[6])]

                if row[8] != "":
                    hour = row[8].split(":")[0]
                    if hour in list(df_entry.keys()):
                        df_entry[str(intervals_num[int(hour)])].append(int(row[10]))
                    else:
                        df_entry[str(intervals_num[int(hour)])] = [int(row[10])]

        for key in df_entry.keys():
            df_entry[key] = np.round(np.mean(df_entry[key]))

        lfmm_mat[:, i] = np.array([value for value in df_entry.values()])

        df_entry = {}

    entry_lfmm = {}
    entry_lfmm["acc"] = "LFMM"

    for i in range(24):
        entry_lfmm[str(intervals_num[i])] = [sum(edyy_mat[i, :])]

    return entry_edyy, entry_lfmm
