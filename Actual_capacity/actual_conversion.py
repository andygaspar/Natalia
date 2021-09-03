import csv
import numpy as np
import pandas as pd

intervals_num = [i for i in range(0, 1441, 60)]




import os

path = 'Actual_capacity'

files = os.listdir(path)
files = [file for file in files if file != "actual_conversion.py"]

for f in files:
    with open('Actual_capacity/'+f) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0

        print(f[2:-4])
        if f[2:-4] == "LFMM":
            print("fjdksla")
        read = False
        actual_capacities = []
        actual_capacities_odd = []

        for row in csv_reader:
            if row[0] == "0:00" and row[1] == "0:59":
                read = True
                if read:

                    for j in range(len(row)):
                        if row[j][-2:] == "59":
                            actual_capacities.append(int(row[j+1]))

                    print(intervals_num[i], actual_capacities, int(np.round(np.mean(actual_capacities))))
                    actual_capacities = []
                    i += 1
                if row[0] == "23:00":
                    read = False

            elif row[0] == "0:00" and row[1] == "0:29":
                read = True
                if read:
                    for j in range(len(row)):
                        if row[j][-1:] == "9":
                            actual_capacities.append(int(row[j + 1]))

            elif row[0] == "0:30" and row[1] == "0:59":
                read = True
                compute_average = False
                if read:
                    for j in range(len(row)):
                        if row[j][-1:] == "9":
                            actual_capacities_odd.append(int(row[j + 1]))
                    actual_capacities = (np.array(actual_capacities) + np.array(actual_capacities_odd))/2

                    print(intervals_num[i], actual_capacities, int(np.round(np.mean(actual_capacities))))
                    actual_capacities, actual_capacities_odd = [], []
                    i += 1
                if row[0] == "23:00":
                    read = False

        # print("ok \n\n")

