from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag
def current_year():
    return datetime.now().strftime('%Y')


@register.simple_tag
def mediapath(path_from_object):
    return path_from_object.url


@register.filter
def mediapath(path_from_object):
    return path_from_object.url


@register.simple_tag
def multiplication(chr_1, chr_2):
    return round(chr_1 * chr_2, 2)


@register.filter
def multiplication(chr_1, chr_2):
    return round(chr_1 * chr_2, 2)


@register.simple_tag
def shortweekday(day):
    week = {
        '0': 'ПН',
        '1': 'ВТ',
        '2': 'СР',
        '3': 'ЧТ',
        '4': 'ПТ',
        '5': 'СБ',
        '6': 'ВС',
    }
    return week.get(day)


@register.filter
def shortweekday(day):
    week = {
        '0': 'ПН',
        '1': 'ВТ',
        '2': 'СР',
        '3': 'ЧТ',
        '4': 'ПТ',
        '5': 'СБ',
        '6': 'ВС',
    }
    return week.get(day)
