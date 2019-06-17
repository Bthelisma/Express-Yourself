from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin', views.signin),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^login/show/(?P<id>\d+)$', views.show),
    url(r'^login/edit/(?P<id>\d+)$', views.edit),
    url(r'^edit/(?P<action>\w+)$', views.edit_process),
    url(r'^process/(?P<action>\w+)$', views.process),
    url(r'^login/new$', views.new),
    url(r'^login/destroy/(?P<id>\d+)$', views.destroy),
    
]