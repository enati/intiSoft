# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^presup/$', login_required(views.PresupuestoList.as_view()), name='presup-list'),
    url(r'^presup/viewWord/(?P<pk>\d+)/$', 'adm.views.viewWord', name='presup-viewWord'),
    #url(r'^presup/actBtn/(?P<pk>\d+)/$', 'adm.views.actualizar_precios', name='presup-actBtn'),
    url(r'^presup/update/(?P<pk>\d+)/$', login_required(views.PresupuestoUpdate.as_view()), name='presup-update'),
    url(r'^presup/create/$', login_required(views.PresupuestoCreate.as_view()), name='presup-create'),

    url(r'^presup/get_user/$', 'adm.views.get_user', name='user-getdata'),
    url(r'^ofertatec/$', login_required(views.OfertaTecList.as_view()), name='ofertatec-list'),
    url(r'^ofertatec/delete/(?P<pk>\d+)/$', login_required(views.OfertaTecDelete.as_view()), name='ofertatec-delete'),
    url(r'^ofertatec/update/(?P<pk>\d+)/$', login_required(views.OfertaTecUpdate.as_view()), name='ofertatec-update'),
    url(r'^ofertatec/create/$', login_required(views.OfertaTecCreate.as_view()), name='ofertatec-create'),

    url(r'^usuarios/$', login_required(views.UsuarioList.as_view()), name='usuarios-list'),
    url(r'^usuarios/delete/(?P<pk>\d+)/$', login_required(views.UsuarioDelete.as_view()), name='usuarios-delete'),
    url(r'^usuarios/update/(?P<pk>\d+)/$', login_required(views.UsuarioUpdate.as_view()), name='usuarios-update'),
    url(r'^usuarios/create/$', login_required(views.UsuarioCreate.as_view()), name='usuarios-create'),
]
