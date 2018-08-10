# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache

urlpatterns = [
    url(r'^contratos/OT/$', login_required(views.OTList.as_view()), name='ot-list'),
    url(r'^contratos/OT/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.OTCreate.as_view())),
                                   name='ot-create'),
    url(r'^contratos/OT/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.OTUpdate.as_view())),
                                               name='ot-update'),
    url(r'^contratos/OT-ML/$', login_required(views.OTMLList.as_view()), name='otml-list'),
    url(r'^contratos/OT-ML/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.OTMLCreate.as_view())),
                                      name='otml-create'),
    url(r'^contratos/OT-ML/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.OTMLUpdate.as_view())),
                                                  name='otml-update'),
    url(r'^contratos/SOT/$', login_required(views.SOTList.as_view()), name='sot-list'),
    url(r'^contratos/SOT/viewSOT/(?P<pk>\d+)/$', views.viewSOT, name='sot-viewSOT'),
    url(r'^contratos/SOT/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.SOTCreate.as_view())),
                                    name='sot-create'),
    url(r'^contratos/SOT/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.SOTUpdate.as_view())),
                                                name='sot-update'),
    url(r'^contratos/RUT/$', login_required(views.RUTList.as_view()), name='rut-list'),
    url(r'^contratos/RUT/viewRUT/(?P<pk>\d+)/$', views.viewRUT, name='rut-viewRUT'),
    url(r'^contratos/RUT/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.RUTCreate.as_view())),
                                    name='rut-create'),
    url(r'^contratos/RUT/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.RUTUpdate.as_view())),
                                                name='rut-update'),
    url(r'^contratos/SI/$', login_required(views.SIList.as_view()), name='si-list'),
    url(r'^contratos/SI/viewSI/(?P<pk>\d+)/$', views.viewSI, name='si-viewSI'),
    url(r'^contratos/SI/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.SICreate.as_view())),
                                   name='si-create'),
    url(r'^contratos/SI/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.SIUpdate.as_view())),
                                               name='si-update'),
    url(r'^contratos/SI/(create|update/\d+)/OT_(?P<area>(LIA|LIM1|LIM2|LIM3|LIM4|LIM5|LIM6|EXT|DES|SIS|MEC|ML|CAL))/$', views.filterOT, name='filter-ot'),
    url(r'^presup/$', login_required(views.PresupuestoList.as_view()), name='presup-list'),
    url(r'^presup/viewWord/(?P<pk>\d+)/(?P<template>\w+)/$', views.viewWord, name='presup-viewWord'),
    #url(r'^presup/actBtn/(?P<pk>\d+)/$', 'adm.views.actualizar_precios', name='presup-actBtn'),
    url(r'^presup/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.PresupuestoUpdate.as_view())),
                                         name='presup-update'),
    url(r'^presup/update/(?P<pk>\d+)/revision/', views.createRevision, name='presup-revision'),
    url(r'^presup/update/(?P<pk>\d+)/rollback/', views.rollBackRevision, name='presup-rollback'),
    url(r'^presup/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.PresupuestoCreate.as_view())),
                             name='presup-create'),

    url(r'^presup/get_user/$', views.get_user, name='user-getdata'),
    url(r'^ofertatec/$', login_required(views.OfertaTecList.as_view()), name='ofertatec-list'),
    url(r'^ofertatec/delete/(?P<pk>\d+)/$', login_required(views.OfertaTecDelete.as_view()), name='ofertatec-delete'),
    url(r'^ofertatec/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.OfertaTecUpdate.as_view())),
                                            name='ofertatec-update'),
    url(r'^ofertatec/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.OfertaTecCreate.as_view())),
                                name='ofertatec-create'),

    url(r'^usuarios/$', login_required(views.UsuarioList.as_view()), name='usuarios-list'),
    url(r'^usuarios/delete/(?P<pk>\d+)/$', login_required(views.UsuarioDelete.as_view()), name='usuarios-delete'),
    url(r'^usuarios/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.UsuarioUpdate.as_view())),
                                           name='usuarios-update'),
    url(r'^usuarios/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.UsuarioCreate.as_view())),
                               name='usuarios-create'),
    url(r'^usuarios/create-modal/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.UsuarioCreateModal.as_view())),
                               name='usuarios-create-modal'),
    url(r'^usuarios/update-modal/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.UsuarioUpdateModal.as_view())),
                               name='usuarios-update-modal'),
    url(r'^pdt/$', login_required(views.PDTList.as_view()), name='pdt-list'),
    url(r'^pdt/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.PDTCreate.as_view())),
                               name='pdt-create'),
    url(r'^pdt/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.PDTUpdate.as_view())),
                                            name='pdt-update'),
    url(r'^pdt/detail/(?P<pk>\d+)/$', never_cache(login_required(views.PDTDetail.as_view())), name='pdt-detail'),
    url(r'^pdt/viewPDF/(?P<pk>\d+)/$', never_cache(views.pdtToPdf), name='pdt-viewPDF'),
    url(r'^pdt/viewXLS/(?P<pk>\d+)/$', never_cache(views.pdtToXls), name='pdt-viewXLS'),
    url(r'^contactos/create-modal/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.ContactoCreateModal.as_view())),
                                             name='contactos-create-modal'),
    url(r'^contactos/update-modal/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.ContactoUpdateModal.as_view())),
                                             name='contactos-update-modal'),
    url(r'^ajax/contactos/$', views.load_contactos, name='ajax_load_contactos'),
]
