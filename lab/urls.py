# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^turnos/$', login_required(views.TurnoList.as_view()), name='turnos-list'),
    url(r'^turnos/LIA/$', login_required(views.LIAList.as_view()), name='LIA-list'),
    url(r'^turnos/LIM1/$', login_required(views.LIM1List.as_view()), name='LIM1-list'),
    url(r'^turnos/LIM2/$', login_required(views.LIM2List.as_view()), name='LIM2-list'),
    url(r'^turnos/LIM3/$', login_required(views.LIM3List.as_view()), name='LIM3-list'),
    url(r'^turnos/LIM6/$', login_required(views.LIM6List.as_view()), name='LIM6-list'),
    url(r'^turnos/EXT/$', login_required(views.EXTList.as_view()), name='EXT-list'),
    url(r'^turnos/SIS/$', login_required(views.SISList.as_view()), name='SIS-list'),
    url(r'^turnos/DES/$', login_required(views.DESList.as_view()), name='DES-list'),
    url(r'^turnos/LIA/create/$', login_required(views.LIACreate.as_view()), name='LIA-create'),
    url(r'^turnos/LIM1/create/$', login_required(views.LIM1Create.as_view()), name='LIM1-create'),
    url(r'^turnos/LIM2/create/$', login_required(views.LIM2Create.as_view()), name='LIM2-create'),
    url(r'^turnos/LIM3/create/$', login_required(views.LIM3Create.as_view()), name='LIM3-create'),
    url(r'^turnos/LIM6/create/$', login_required(views.LIM6Create.as_view()), name='LIM6-create'),
    url(r'^turnos/EXT/create/$', login_required(views.EXTCreate.as_view()), name='EXT-create'),
    url(r'^turnos/SIS/create/$', login_required(views.SISCreate.as_view()), name='SIS-create'),
    url(r'^turnos/DES/create/$', login_required(views.DESCreate.as_view()), name='DES-create'),
    url(r'^turnos/LIA/update/(?P<pk>\d+)/$', login_required(views.LIAUpdate.as_view()), name='LIA-update'),
    url(r'^turnos/LIM1/update/(?P<pk>\d+)/$', login_required(views.LIM1Update.as_view()), name='LIM1-update'),
    url(r'^turnos/LIM2/update/(?P<pk>\d+)/$', login_required(views.LIM2Update.as_view()), name='LIM2-update'),
    url(r'^turnos/LIM3/update/(?P<pk>\d+)/$', login_required(views.LIM3Update.as_view()), name='LIM3-update'),
    url(r'^turnos/LIM6/update/(?P<pk>\d+)/$', login_required(views.LIM6Update.as_view()), name='LIM6-update'),
    url(r'^turnos/EXT/update/(?P<pk>\d+)/$', login_required(views.EXTUpdate.as_view()), name='EXT-update'),
    url(r'^turnos/SIS/update/(?P<pk>\d+)/$', login_required(views.SISUpdate.as_view()), name='SIS-update'),
    url(r'^turnos/DES/update/(?P<pk>\d+)/$', login_required(views.DESUpdate.as_view()), name='DES-update'),
    url(r'^turnos/create/$', login_required(views.TurnoCreate.as_view()), name='turnos-create'),
    url(r'^turnos/update/(?P<pk>\d+)/$', login_required(views.TurnoUpdate.as_view()), name='turnos-update'),
    url(r'^turnos/delete/(?P<pk>\d+)/$', login_required(views.TurnoDelete.as_view()), name='turnos-delete'),
    url(r'^turnos/get_price/$', 'lab.views.get_price', name='ot-getprice'),
    url(r'^turnos/get_presup/$', 'lab.views.get_presup', name='presup-getdata'),
]