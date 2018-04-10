from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ActivityLogView.as_view(), name='activity_log'),
]