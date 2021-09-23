def fix_date(date):
    date_list = list(date)
    if date_list[1] == "/" and date_list[3] == "/":
        date_list.insert(2, "0")
    elif date_list[2] == "/" and date_list[4] == "/":
        date_list.insert(3, "0")

    if date_list[1] == "/":
        date_list.insert(0, "0")

    return ''.join(date_list)


