from typing import List

from ACC import set_accs
from ACC.acc import Acc


class Country:
    def __init__(self, name, accs: List[Acc], df_delayed, df_regulation, df_open,
                 df_air_capacity, df_actual_capacity, df_saturation,
                 df_sector_capacity, days):

        self.name = name
        self.accs = set_accs.make_acc_list(accs, df_delayed, df_regulation, df_open,
                                           df_air_capacity, df_actual_capacity, df_saturation,
                                           df_sector_capacity, days)
