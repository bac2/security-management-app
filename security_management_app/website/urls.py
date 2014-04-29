from django.conf.urls import patterns, include, url

from website import views

urlpatterns = patterns('',
    url(r'api/device/(?P<device_uid>[\w\d]+)/$', views.device_update, name="device_upload"),
    url(r'^$', views.index, name="index"),
    url(r'^devices$', views.device_list, name="device_list"),
    url(r'^add_device$', views.add_device, name="add_device"),
    url(r'device/(?P<device_uid>[\w\d]+)/$', views.device, name="device_upload"),
    url(r'^dashboarddata$', views.graph_data, name="graph_data")
)
