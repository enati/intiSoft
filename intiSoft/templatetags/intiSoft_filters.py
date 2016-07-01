# -*- coding: utf-8 -*-
from django import template
import datetime
from adm.models import OfertaTec

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='plus_five')
def plus_five(orig_date):
    try:
        date = (orig_date + datetime.timedelta(days=7)).strftime('%d/%m/%Y')
    except:
        date = orig_date
    return date


@register.filter(name='less_five')
def less_five(orig_date):
    try:
        date = (orig_date - datetime.timedelta(days=7)).strftime('%d/%m/%Y')
    except:
        date = orig_date
    return date


@register.filter(name='ot_by_lab')
def ot_by_lab(ot_list, lab):
    try:
        qs = ot_list.field.queryset.filter(area=lab)
    except:
        qs = ot_list
    return qs


@register.filter(name='range_3')
def range_3(actual_page):
    return range(actual_page - 3, actual_page + 4)


@register.filter(name='disable')
def disable(field):
    return field.as_widget(attrs={"disabled" : "disabled"})


@register.filter(name='getOTCode')
def getOTCode(ot_id):
    try:
        return OfertaTec.objects.get(pk=ot_id).codigo
    except:
        return []


@register.filter(name='revName')
def revName(name):
    try:
        return name[2:]
    except:
        return []
