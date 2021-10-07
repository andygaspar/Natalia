import pandas as pd
import numpy as np
import os

country_acc = {
    "GERMANY": ["EDWW", "EDUU", "EDMM", 'EDGG'],
    'CZECH': ['LKAA'],
    'AUSTRIA': ['LOVV'],
    'SWITS': ['LSAG', 'LSAZ'],
    'MAASTR': ['EDYY'],
    'AMSETER': ['EHAA'],
    'FRANCE': ['LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE'],
    'ITALY': ['LIBB', 'LIMM', 'LIPP', 'LIRR'],
    'SPAIN': ['LECB', 'LECM', 'LECP', 'LECS'],
    'BELGIUM': ["EBBU"],
    'SLOVAKIA': ["LZBB"],
    'HUNGARY': ["LHCC"],
    'SLOVENIA': ["LJLA"],
    'CROATIA': ['LDZO'],
    'BOSNIA': ['LQSB'],
    'POLAND': ['EPWW'],
    'LITHUANIA': ['EYVC'],
    'UK': ['EGPX', 'EGTT'],
    'IRELAND': ['EIDW', 'EISN'],
    'BULGARIA': ['LBSR'],
    'ROMANIA': ['LRBB'],
    'DENMARK': ['EKDK'],
    'SWEDEN': ['ESMM', 'ESOS'],
    'ESTONIA': ['EETT'],
    'FINLAND': ['EFIN'],
    'LATVIA': ['EVRR'],
    'NORWAY': ['ENBD', 'ENOSE', 'ENOSW'],
    'PORTUGAL': ['LPPC'],
    'CYPRUS': ['LCCC'],
    'GREECE': ['LGGG', 'LGMD'],
    'MALTA': ['LMMM']
}





pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def one_to_one(save=False):
    total = pd.read_csv("Results/total.csv")

    columns = ["country", "initial delay", "final delay", "reduction", "saturation tolerance", "case"]

    df_one_to_one = pd.DataFrame(columns=columns)

    for case in total.case.unique():
        df_case = total[total.case == case]
        for saturation in df_case["saturation tolerance"].unique():
            df_case_sat = df_case[df_case["saturation tolerance"] == saturation]
            found_acc = ["total"]
            df_total = df_case_sat[df_case_sat.acc == "total"]
            initial = df_total["initial delay"].iloc[0]
            final = df_total["final delay"].iloc[0]
            reduction = df_total["reduction"].iloc[0]
            to_append = ["total"] + [initial] + [final] + [reduction] + [saturation] + [case]
            df_one_to_one = df_one_to_one.append(dict(zip(columns, to_append)), ignore_index=True)
            for country in country_acc.keys():
                for acc in df_case_sat.acc:
                    if acc in country_acc[country] and acc not in found_acc:
                        found_acc += country_acc[country]
                        df_country = df_case_sat[df_case_sat.acc.isin(country_acc[country])]
                        initial = sum(df_country["initial delay"])
                        final = sum(df_country["final delay"])
                        reduction = sum(df_country["reduction"])
                        to_append = [country] + [initial] + [final] + [reduction] + [saturation] + [case]
                        df_one_to_one = df_one_to_one.append(dict(zip(columns, to_append)), ignore_index=True)

    if save:
        df_one_to_one.to_csv("Results/one_to_one_by_country.csv", index_label=False, index=False)
    else:
        print(df_one_to_one)


def virtual(save=False):
    path = 'Results/Virtual'

    files = os.listdir(path)
    columns = ["country", "initial delay", "final delay", "reduction", "saturation tolerance", "capacity correction",
               "fab"]

    df_virtual = pd.DataFrame(columns=columns)

    for file in files:
        df_case = pd.read_csv(path + "/" + file)
        case = df_case.case.iloc[0]
        print(file)

        for saturation in df_case["saturation tolerance"].unique():
            df_case_sat = df_case[df_case["saturation tolerance"] == saturation]
            for cap_correction in df_case_sat["capacity correction"].unique():
                df_case_sat_cap = df_case_sat[df_case_sat["capacity correction"] == cap_correction]
                found_acc = ["total"]
                df_total = df_case_sat_cap[df_case_sat_cap.acc == "total"]
                initial = df_total["initial delay"].iloc[0]
                final = df_total["final delay"].iloc[0]
                reduction = df_total["reduction"].iloc[0]
                to_append = ["total"] + [initial] + [final] + [reduction] + [saturation] + [cap_correction] + [case]
                df_virtual = df_virtual.append(dict(zip(columns, to_append)), ignore_index=True)
                for country in country_acc.keys():
                    for acc in df_case_sat_cap.acc:
                        if acc in country_acc[country] and acc not in found_acc:
                            found_acc += country_acc[country]
                            df_country = df_case_sat_cap[df_case_sat_cap.acc.isin(country_acc[country])]
                            initial = sum(df_country["initial delay"])
                            final = sum(df_country["final delay"])
                            reduction = sum(df_country["reduction"])
                            to_append = [country] + [initial] + [final] + [reduction] + [saturation] + [cap_correction]\
                                        + [case]
                            df_virtual = df_virtual.append(dict(zip(columns, to_append)), ignore_index=True)

    if save:
        df_virtual.to_csv("Results/virtual_aggregated.csv", index_label=False, index=False)
    else:
        print(df_virtual)


def fabs(save=False):
    path = 'Results/Fabs'

    files = os.listdir(path)
    columns = ["country", "initial delay", "final delay", "reduction", "saturation tolerance", "capacity correction",
               "fab"]

    df_virtual = pd.DataFrame(columns=columns)

    for file in files:
        df_case = pd.read_csv(path + "/" + file)
        case = df_case.case.iloc[0]

        for saturation in df_case["saturation tolerance"].unique():
            df_case_sat = df_case[df_case["saturation tolerance"] == saturation]
            for cap_correction in df_case["capacity correction"].unique():
                df_case_sat_cap = df_case_sat[df_case_sat["capacity correction"] == cap_correction]
                found_acc = ["total"]
                df_total = df_case_sat_cap[df_case_sat_cap.acc == "total"]
                initial = df_total["initial delay"].iloc[0]
                final = df_total["final delay"].iloc[0]
                reduction = df_total["reduction"].iloc[0]
                to_append = ["total"] + [initial] + [final] + [reduction] + [saturation] + [cap_correction] + [case]
                df_virtual = df_virtual.append(dict(zip(columns, to_append)), ignore_index=True)
                for country in country_acc.keys():
                    for acc in df_case_sat_cap.acc:
                        if acc in country_acc[country] and acc not in found_acc:
                            found_acc += country_acc[country]
                            df_country = df_case_sat_cap[df_case_sat_cap.acc.isin(country_acc[country])]
                            initial = sum(df_country["initial delay"])
                            final = sum(df_country["final delay"])
                            reduction = sum(df_country["reduction"])
                            to_append = [country] + [initial] + [final] + [reduction] + [saturation] \
                                        + [cap_correction] + [case]
                            df_virtual = df_virtual.append(dict(zip(columns, to_append)), ignore_index=True)

    if save:
        df_virtual.to_csv("Results/fabs_aggregated.csv", index_label=False, index=False)
    else:
        print(df_virtual)

# one_to_one()
# virtual(True)
fabs(True)
