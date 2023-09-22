def get_week_days(days: list) -> str:
    days_dict = {
        0: 'ПН',
        1: 'ВТ',
        2: 'СР',
        3: 'ЧТ',
        4: 'ПТ',
        5: 'СБ',
        6: 'ВС'
    }
    tmp_list = [days_dict.get(day) for day in days]
    return ', '.join(tmp_list)
