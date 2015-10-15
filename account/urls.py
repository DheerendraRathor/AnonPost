__author__ = 'dheerendra'

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^authorize/$', views.authorize, name='authorize'),
    url(r'^logout/$', views.logout, name='logout'),
]
