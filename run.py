from old.Acc import acc
import pandas as pd
from old.configuration_data import set_configuration_df

acc_dict = acc.make_acc_dict()


df_open = set_configuration_df()

df_sat = pd.read_csv("old/ACCs_ActualCapacities/Saturations.csv", sep=";")


df_occ = pd.read_csv("old/ACCs_ActualCapacities/Occupancies.csv", sep=";")

