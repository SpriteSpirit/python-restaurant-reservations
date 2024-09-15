from datetime import datetime, date, time

from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def translate_time(value):
    """ Перевод времени в строчное представление """

    if isinstance(value, (datetime, time)):
        return value.strftime('%H:%M')  # Форматируем время
    else:
        return "-"


@register.filter
def translate_date(value):
    """ Перевод даты в строчное представление """
    if isinstance(value, (datetime, date)):
        return value.strftime('%d.%m.%Y')  # Правильное использование strftime
    else:
        return "-"


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter('translate')
def translate(value):
    return _(value)


@register.filter(name='in_range')
def in_range(query_list):
    return range(len(query_list))
