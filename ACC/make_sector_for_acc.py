import csv


def get_sectors_dict():
    sectors_acc = {}

    with open('RowData/sector_config.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] != "":
                acc = row[0]
            elif row[-1] != "":
                sectors_acc[row[-1]] = acc

    return sectors_acc


