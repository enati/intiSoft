# -*- coding: utf-8 -*-
from django import template
import datetime
from adm.models import OfertaTec, OfertaTec_Descripcion, CentroDeCostos, AreaTematica

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
    return field.as_widget(attrs={"disabled": "disabled"})


@register.filter(name='getOTCode')
def getOTCode(ot_id):
    try:
        return OfertaTec.objects.get(pk=ot_id).codigo
    except:
        return []

@register.filter(name='getOTCentroDetalle')
def getOTCentroDetalle(ot_id):
    try:
        return OfertaTec_Descripcion.objects.get(pk=ot_id).detalle
    except:
        return ''

@register.filter(name='revName')
def revName(name):
    try:
        return name[2:]
    except:
        return []


@register.filter(name='boolToText')
def boolToText(val):
    if val:
        return "Si"
    return "No"


@register.simple_tag
def get_verbose_name(model, field_name):
    """
    Returns verbose_name for a field.
    """
    return model._meta.get_field(field_name).verbose_name


@register.filter(name='getCentroDeCostos')
def getCentroDeCostos(cc_id):
    try:
        return CentroDeCostos.objects.get(pk=cc_id).nombre
    except:
        return ''


@register.filter(name='getAreaTematica')
def getAreaTematica(area_id):
    try:
        return AreaTematica.objects.get(pk=area_id).nombre
    except:
        return ''