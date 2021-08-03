df_mc = pd.read_csv("RowData/max_configuration.csv")

country = []
name = []
max_sectors = []
codes = []
for code in df_acc.code.unique():
    df = df_acc[df_acc.code == code]
    country.append(df.iloc[0].Country)
    name.append(df.iloc[0].Name.split()[0])
    codes.append(code)
    if code == "EYVC":
        max_sectors.append(5)
    else:
        max_sectors.append(sum(df.Sectors_nb))

name
name[-1] = "LONDON"
df_mc = pd.DataFrame({"country": country, "name": name, "max_sectors": max_sectors, "code": codes})
df_mc = df_mc[df_mc.code != "EYVI"]

df_mc.to_csv("RowData/max_config.csv", index_label=False, index=False)