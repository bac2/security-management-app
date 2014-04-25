from django.conf.urls import patterns, include, url

from website import views

urlpatterns = patterns('',
    url(r'device/(?P<device_uid>[\w\d]+)/$', views.device, name="device"),
    url(r'^$', views.index, name="index"),
    url(r'^devices$', views.device_list, name="device_list"),
    url(r'^add_device$', views.add_device, name="add_device"),
)
