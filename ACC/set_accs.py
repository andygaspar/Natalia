from ACC import acc as a


def get_acc_df(acc, df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity, df_saturation, df_sec_cap):
    df_r_acc = df_regulation[df_regulation.acc == acc]
    df_d_acc = df_delayed[df_delayed.Regulation.isin(df_r_acc.Regulation)]
    df_o_acc = df_open[df_open.acc == acc]
    df_c_acc = df_air_capacity[df_air_capacity.acc == acc]
    df_a_acc = df_actual_capacity[df_actual_capacity.acc == acc]
    df_s_acc = df_saturation[df_saturation.acc == acc]
    df_sc_acc = df_sec_cap[df_sec_cap.acc == acc]

    return df_d_acc, df_r_acc, df_o_acc, df_c_acc, df_a_acc, df_s_acc, df_sc_acc


def make_acc_list(acc_list, df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity, df_saturation,
                  df_sector_capacity, days):
    acc_index = 0
    accs = []
    for acc in acc_list:
        df_d_acc, df_r_acc, df_o_acc, df_m_acc, df_a_acc, df_s_acc, df_sc_acc = get_acc_df(acc, df_delayed,
                                                                                           df_regulation,
                                                                                           df_open,
                                                                                           df_air_capacity,
                                                                                           df_actual_capacity,
                                                                                           df_saturation,
                                                                                           df_sector_capacity)
        accs.append(a.Acc(acc_index, acc, days, df_o_acc, df_r_acc, df_d_acc, df_m_acc, df_a_acc, df_s_acc, df_sc_acc))
        acc_index += 1

    return accs

