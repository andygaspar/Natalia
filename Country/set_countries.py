from ACC import set_accs
from Country.country import Country

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
}


def make_country_list(country_list, df_delayed, df_regulation, df_open, df_air_capacity, df_actual_capacity,
                      df_saturation, df_sector_capacity, days):
    countries = []
    for country in country_list:
        countries.append(Country(country_acc[country], df_delayed, df_regulation, df_open,
                                 df_air_capacity, df_actual_capacity, df_saturation,
                                 df_sector_capacity, days))
