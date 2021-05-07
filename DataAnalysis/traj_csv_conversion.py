import pandas as pd
from os import listdir
from os.path import isfile, join


import csv

# with open('trajectories/20170901_Initial_from_NEST.so6') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=' ')
#     line_count = 0
#     for row in csv_reader:
#         if line_count < 10:
#             print(row)
#             line_count += 1
#         else:
#             break


with open('trajectories/20170901_Initial_from_NEST.t5') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    line_count = 0
    for row in csv_reader:
        if line_count < 10:
            print(row)
            line_count += 1
        else:
            break