# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^contratos/OT/$', login_required(views.OTList.as_view()), name='ot-list'),
    url(r'^contratos/OT/create/$', login_required(views.OTCreate.as_view()), name='ot-create'),
    url(r'^contratos/OT/update/(?P<pk>\d+)/$', login_required(views.OTUpdate.as_view()), name='ot-update'),
    url(r'^contratos/OT-ML/$', login_required(views.OTMLList.as_view()), name='otml-list'),
    url(r'^contratos/OT-ML/create/$', login_required(views.OTMLCreate.as_view()), name='otml-create'),
    url(r'^contratos/OT-ML/update/(?P<pk>\d+)/$', login_required(views.OTMLUpdate.as_view()), name='otml-update'),
    url(r'^contratos/SOT/$', login_required(views.SOTList.as_view()), name='sot-list'),
    url(r'^contratos/SOT/viewSOT/(?P<pk>\d+)/$', 'adm.views.viewSOT', name='sot-viewSOT'),
    url(r'^contratos/SOT/create/$', login_required(views.SOTCreate.as_view()), name='sot-create'),
    url(r'^contratos/SOT/update/(?P<pk>\d+)/$', login_required(views.SOTUpdate.as_view()), name='sot-update'),
    url(r'^contratos/RUT/$', login_required(views.RUTList.as_view()), name='rut-list'),
    url(r'^contratos/SOT/viewRUT/(?P<pk>\d+)/$', 'adm.views.viewRUT', name='rut-viewRUT'),
    url(r'^contratos/RUT/create/$', login_required(views.RUTCreate.as_view()), name='rut-create'),
    url(r'^contratos/RUT/update/(?P<pk>\d+)/$', login_required(views.RUTUpdate.as_view()), name='rut-update'),
    url(r'^contratos/SI/$', login_required(views.SIList.as_view()), name='si-list'),
    url(r'^contratos/SI/create/$', login_required(views.SICreate.as_view()), name='si-create'),
    url(r'^contratos/SI/update/(?P<pk>\d+)/$', login_required(views.SIUpdate.as_view()), name='si-update'),

    url(r'^presup/$', login_required(views.PresupuestoList.as_view()), name='presup-list'),
    url(r'^presup/viewWord/(?P<pk>\d+)/$', 'adm.views.viewWord', name='presup-viewWord'),
    #url(r'^presup/actBtn/(?P<pk>\d+)/$', 'adm.views.actualizar_precios', name='presup-actBtn'),
    url(r'^presup/update/(?P<pk>\d+)/$', login_required(views.PresupuestoUpdate.as_view()), name='presup-update'),
    url(r'^presup/update/(?P<pk>\d+)/revision/', 'adm.views.createRevision', name='presup-revision'),
    url(r'^presup/update/(?P<pk>\d+)/rollback/', 'adm.views.rollBackRevision', name='presup-rollback'),
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
