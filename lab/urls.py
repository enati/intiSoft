# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

urlpatterns = [
    url(r'^turnos/$', login_required(views.TurnoList.as_view()), name='turnos-list'),
    url(r'^turnos/calendar/LIA/$', login_required(views.LIACalendarView.as_view()), name='LIA-calendar'),
    url(r'^turnos/calendar/LIA/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIACalendarView.as_view()), name='LIA-calendar'),
    url(r'^turnos/calendar/LIM1/$', login_required(views.LIM1CalendarView.as_view()), name='LIM1-calendar'),
    url(r'^turnos/calendar/LIM1/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIM1CalendarView.as_view()), name='LIM1-calendar'),
    url(r'^turnos/calendar/LIM2/$', login_required(views.LIM2CalendarView.as_view()), name='LIM2-calendar'),
    url(r'^turnos/calendar/LIM2/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIM2CalendarView.as_view()), name='LIM2-calendar'),
    url(r'^turnos/calendar/LIM3/$', login_required(views.LIM3CalendarView.as_view()), name='LIM3-calendar'),
    url(r'^turnos/calendar/LIM3/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIM3CalendarView.as_view()), name='LIM3-calendar'),
    url(r'^turnos/calendar/LIM4/$', login_required(views.LIM4CalendarView.as_view()), name='LIM4-calendar'),
    url(r'^turnos/calendar/LIM4/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIM4CalendarView.as_view()), name='LIM4-calendar'),
    url(r'^turnos/calendar/LIM5/$', login_required(views.LIM5CalendarView.as_view()), name='LIM5-calendar'),
    url(r'^turnos/calendar/LIM5/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIM5CalendarView.as_view()), name='LIM5-calendar'),
    url(r'^turnos/calendar/LIM6/$', login_required(views.LIM6CalendarView.as_view()), name='LIM6-calendar'),
    url(r'^turnos/calendar/LIM6/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.LIM6CalendarView.as_view()), name='LIM6-calendar'),
    url(r'^turnos/calendar/EXT/$', login_required(views.EXTCalendarView.as_view()), name='EXT-calendar'),
    url(r'^turnos/calendar/EXT/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.EXTCalendarView.as_view()), name='EXT-calendar'),
    url(r'^turnos/calendar/SIS/$', login_required(views.SISCalendarView.as_view()), name='SIS-calendar'),
    url(r'^turnos/calendar/SIS/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.SISCalendarView.as_view()), name='SIS-calendar'),
    url(r'^turnos/calendar/DES/$', login_required(views.DESCalendarView.as_view()), name='DES-calendar'),
    url(r'^turnos/calendar/DES/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.DESCalendarView.as_view()), name='DES-calendar'),
    url(r'^turnos/calendar/CAL/$', login_required(views.CALCalendarView.as_view()), name='CAL-calendar'),
    url(r'^turnos/calendar/CAL/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.CALCalendarView.as_view()), name='CAL-calendar'),
    url(r'^turnos/calendar/MEC/$', login_required(views.MECCalendarView.as_view()), name='MEC-calendar'),
    url(r'^turnos/calendar/MEC/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.MECCalendarView.as_view()), name='MEC-calendar'),
    url(r'^turnos/calendar/ML/$', login_required(views.MLCalendarView.as_view()), name='ML-calendar'),
    url(r'^turnos/calendar/ML/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.MLCalendarView.as_view()), name='ML-calendar'),
    url(r'^turnos/LIA/$', login_required(views.LIAList.as_view()), name='LIA-list'),
    url(r'^turnos/LIM1/$', login_required(views.LIM1List.as_view()), name='LIM1-list'),
    url(r'^turnos/LIM2/$', login_required(views.LIM2List.as_view()), name='LIM2-list'),
    url(r'^turnos/LIM3/$', login_required(views.LIM3List.as_view()), name='LIM3-list'),
    url(r'^turnos/LIM4/$', login_required(views.LIM4List.as_view()), name='LIM4-list'),
    url(r'^turnos/LIM5/$', login_required(views.LIM5List.as_view()), name='LIM5-list'),
    url(r'^turnos/LIM6/$', login_required(views.LIM6List.as_view()), name='LIM6-list'),
    url(r'^turnos/EXT/$', login_required(views.EXTList.as_view()), name='EXT-list'),
    url(r'^turnos/SIS/$', login_required(views.SISList.as_view()), name='SIS-list'),
    url(r'^turnos/DES/$', login_required(views.DESList.as_view()), name='DES-list'),
    url(r'^turnos/CAL/$', login_required(views.CALList.as_view()), name='CAL-list'),
    url(r'^turnos/MEC/$', login_required(views.MECList.as_view()), name='MEC-list'),
    url(r'^turnos/ML/$', login_required(views.MLList.as_view()), name='ML-list'),
    url(r'^turnos/LIA/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIACreate.as_view())),
                                 name='LIA-create'),
    url(r'^turnos/LIM1/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM1Create.as_view())),
                                  name='LIM1-create'),
    url(r'^turnos/LIM2/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM2Create.as_view())),
                                  name='LIM2-create'),
    url(r'^turnos/LIM3/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM3Create.as_view())),
                                  name='LIM3-create'),
    url(r'^turnos/LIM4/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM4Create.as_view())),
                                  name='LIM4-create'),
    url(r'^turnos/LIM5/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM5Create.as_view())),
                                  name='LIM5-create'),
    url(r'^turnos/LIM6/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM6Create.as_view())),
                                  name='LIM6-create'),
    url(r'^turnos/EXT/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.EXTCreate.as_view())),
                                 name='EXT-create'),
    url(r'^turnos/SIS/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.SISCreate.as_view())),
                                 name='SIS-create'),
    url(r'^turnos/DES/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.DESCreate.as_view())),
                                 name='DES-create'),
    url(r'^turnos/CAL/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.CALCreate.as_view())),
                                 name='CAL-create'),
    url(r'^turnos/MEC/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.MECCreate.as_view())),
                                 name='MEC-create'),
    url(r'^turnos/ML/create/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.MLCreate.as_view())),
                                name='ML-create'),
    url(r'^turnos/LIA/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIAUpdate.as_view())),
                                             name='LIA-update'),
    url(r'^turnos/LIM1/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM1Update.as_view())),
                                              name='LIM1-update'),
    url(r'^turnos/LIM2/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM2Update.as_view())),
                                              name='LIM2-update'),
    url(r'^turnos/LIM3/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM3Update.as_view())),
                                              name='LIM3-update'),
    url(r'^turnos/LIM4/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM4Update.as_view())),
                                              name='LIM4-update'),
    url(r'^turnos/LIM5/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM5Update.as_view())),
                                              name='LIM5-update'),
    url(r'^turnos/LIM6/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.LIM6Update.as_view())),
                                              name='LIM6-update'),
    url(r'^turnos/EXT/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.EXTUpdate.as_view())),
                                             name='EXT-update'),
    url(r'^turnos/SIS/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.SISUpdate.as_view())),
                                             name='SIS-update'),
    url(r'^turnos/DES/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.DESUpdate.as_view())),
                                             name='DES-update'),
    url(r'^turnos/CAL/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.CALUpdate.as_view())),
                                             name='CAL-update'),
    url(r'^turnos/MEC/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.MECUpdate.as_view())),
                                             name='MEC-update'),
    url(r'^turnos/ML/update/(?P<pk>\d+)/$', cache_control(max_age=0, no_cache=True, no_store=True)(login_required(views.MLUpdate.as_view())),
                                            name='ML-update'),
    url(r'^turnos/create/$', login_required(views.TurnoCreate.as_view()), name='turnos-create'),
    url(r'^turnos/update/(?P<pk>\d+)/$', login_required(views.TurnoUpdate.as_view()), name='turnos-update'),
    url(r'^turnos/delete/(?P<pk>\d+)/$', login_required(views.TurnoDelete.as_view()), name='turnos-delete'),
    url(r'^turnos/LIA/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIA-revision'),
    url(r'^turnos/LIM1/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIM1-revision'),
    url(r'^turnos/LIM2/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIM2-revision'),
    url(r'^turnos/LIM3/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIM3-revision'),
    url(r'^turnos/LIM4/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIM4-revision'),
    url(r'^turnos/LIM5/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIM5-revision'),
    url(r'^turnos/LIM6/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='LIM6-revision'),
    url(r'^turnos/EXT/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='EXT-revision'),
    url(r'^turnos/SIS/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='SIS-revision'),
    url(r'^turnos/DES/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='DES-revision'),
    url(r'^turnos/CAL/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='CAL-revision'),
    url(r'^turnos/MEC/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='MEC-revision'),
    url(r'^turnos/ML/update/(?P<pk>\d+)/revision/', 'lab.views.createRevision', name='ML-revision'),
    url(r'^turnos/LIA/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIA-rollback'),
    url(r'^turnos/LIM1/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIM1-rollback'),
    url(r'^turnos/LIM2/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIM2-rollback'),
    url(r'^turnos/LIM3/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIM3-rollback'),
    url(r'^turnos/LIM4/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIM4-rollback'),
    url(r'^turnos/LIM5/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIM5-rollback'),
    url(r'^turnos/LIM6/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='LIM6-rollback'),
    url(r'^turnos/EXT/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='EXT-rollback'),
    url(r'^turnos/SIS/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='SIS-rollback'),
    url(r'^turnos/DES/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='DES-rollback'),
    url(r'^turnos/CAL/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='CAL-rollback'),
    url(r'^turnos/MEC/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='MEC-rollback'),
    url(r'^turnos/ML/update/(?P<pk>\d+)/rollback/', 'lab.views.rollBackRevision', name='ML-rollback'),
    url(r'^turnos/get_price/$', 'lab.views.get_price', name='ot-getprice'),
    url(r'^turnos/get_presup/$', 'lab.views.get_presup', name='presup-getdata'),

]
