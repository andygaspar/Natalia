
cases = {
    "GERMANY": ["EDWW", "EDUU", "EDMM", 'EDGG'],
    'GERMANY_CZECH': ["EDWW", "EDUU", "EDMM", 'EDGG', 'LKAA'],
    'GERMANY_AUSTRIA': ["EDWW", "EDUU", "EDMM", 'EDGG', 'LOVV'],
    'GERMANY_SWITS': ["EDWW", "EDUU", "EDMM", 'EDGG', 'LSAG', 'LSAZ'],
    'GERMANY_MAASTR': ["EDWW", "EDUU", "EDMM", 'EDGG', 'EDYY'],
    'GERMANY_AMSETER': ["EDWW", "EDUU", "EDMM", 'EDGG', 'EHAA'],
    'GERMANY_FRANCE': ["EDWW", "EDUU", "EDMM", 'EDGG', 'LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE'],
    'FRANCE': ['LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE'],
    'FRANCE_SWITS': ['LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE', 'LSAG', 'LSAZ'],
    'FRANCE_ITALY': ['LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE', 'LIBB', 'LIMM', 'LIPP', 'LIRR'],
    'FRANCE_SPAIN': ['LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE', 'LECB', 'LECM', 'LECP', 'LECS'],
    'FRANCE_MAASTR': ['LFBB', 'LFRR', 'LFMM', 'LFFF', 'LFEE', 'EDYY'],
    'VIRTUAL_CENTRE': ["EDWW", "EDUU", "EDMM", 'EDGG', 'LKAA', 'LOVV', 'LSAG', 'LSAZ', 'EDYY', 'EHAA', 'LFBB', 'LFRR',
                       'LFMM', 'LFFF', 'LFEE', 'LIBB', 'LIMM', 'LIPP', 'LIRR', 'LECB', 'LECM', 'LECP', 'LECS', "EBBU",
                       "LZBB", "LHCC", "LJLA", 'LDZO', 'LQSB', 'EPWW', 'EYVC', 'EGPX', 'EGTT', 'EIDW', 'EISN', 'LBSR',
                       'LRBB', 'EKDK', 'ESMM', 'ESOS', 'EETT', 'EFIN', 'EVRR', 'ENBD', 'ENOSE', 'ENOSW', 'LPPC', 'LCCC',
                       'LGGG', 'LGMD', 'LMMM']
}

fabs = {
    'FABEC': ['EDGG', 'EDUU', 'EDMM', 'EDWW', 'LFBB', 'LFRR', 'LFMM',
               'LFFF', 'LFEE', 'EBBU', 'EDYY', 'EHAA', 'LSAZ', 'LSAG'],
    'FABCE': ['LKAA', 'LZBB', 'LOVV', 'LHCC', 'LJLA', 'LDZO', 'LQSB'], # LZBA instead of LZBB
    'BALTIC FAB': ['EPWW', 'EYVC'],
    'UK-IRELAND FAB': ['EGPX', 'EGTT', 'EIDW', 'EISN'], #removed EGCC
    'DANUBE FAB': ['LBSR', 'LRBB'],
    'DANISH-SWEDISH': ['EKDK', 'ESMM', 'ESOS'],
    'NORTH EU FAB': ['EETT', 'EFIN', 'EVRR', 'ENBD', 'ENOSE', 'ENOSW'],  #changed ENOS to ENOSE ENOSW
    'SOUTH-WEST FAB': ['LPPC', 'LECB', 'LECM', 'LECP', 'LECS'],  #changed LPCC into LPPC
    'BLUE MED FAB': ['LCCC', 'LGGG', 'LGMD', 'LIBB', 'LIMM', 'LIPP', 'LIRR', 'LMMM']
}

countries_case = {
    'FABEC': ["GERMANY", "FRANCE", "BELGIUM", 'MAASTR', 'AMSETER', 'SWITS'],
    "GERMANY": ["GERMANY"],
    'GERMANY_CZECH': ['GERMANY', 'CZECH'],
    'GERMANY_AUSTRIA': ['GERMANY', 'AUSTRIA'],
    'GERMANY_SWITS': ['GERMANY', 'SWITS'],
    'GERMANY_MAASTR': ['GERMANY', 'MAASTR'],
    'GERMANY_AMSETER': ['GERMANY', 'AMSETER'],
    'GERMANY_FRANCE': ['GERMANY', 'FRANCE'],
    'FRANCE': ['FRANCE'],
    'FRANCE_SWITS': ['FRANCE', 'SWITS'],
    'FRANCE_ITALY': ['FRANCE', 'ITALY'],
    'FRANCE_SPAIN': ['FRANCE', 'SPAIN'],
    'FRANCE_MAASTR': ['FRANCE', 'MAASTR'],
    'VIRTUAL_CENTRE': ["GERMANY", "FRANCE", "BELGIUM", 'AMSETER', 'SWITS', 'CZECH', 'AUSTRIA', 'ITALY', 'MAASTR',
                       "SPAIN", 'SLOVAKIA', 'SLOVENIA', 'CROATIA', 'BOSNIA', 'POLAND', 'LITHUANIA', 'UK', 'IRELAND',
                       'BULGARIA', 'ROMANIA','DENMARK','SWEDEN', 'ESTONIA', 'FINLAND', 'LATVIA', 'NORWAY', 'PORTUGAL',
                       'CYPRUS', 'GREECE', 'MALTA']
}


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