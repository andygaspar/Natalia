from Acc import acc
import pandas as pd

acc_dict = acc.make_acc_dict()

lovv = acc_dict["LOVVCTA"]
lovv.plot_config()

df_sat = pd.read_csv("RowData/ACCs_ActualCapacities/Saturations.csv", sep=";")

