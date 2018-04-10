"""intiSoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .forms import MyAuthenticationForm
from . import views as myViews
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lab/', include('lab.urls', namespace="lab")),
    url(r'^adm/', include('adm.urls', namespace="adm")),
    url(r'^recent_activity/', include('activity_log.urls', namespace="activity_log")),
    url(r'^login/$', views.login,
        {'template_name': 'intiSoft/login.html',
        'authentication_form': MyAuthenticationForm},
        name='user-login'),
    url(r'^logout/$', views.logout,
        {'template_name': 'intiSoft/logout.html'},
        name='user-logout'),
    url('^$', myViews.index, name='index'),
    url(r'^profile/(?P<pk>\d+)/$', myViews.ProfileView.as_view(),
        name='user-profile'),

]
