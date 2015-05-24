__author__ = 'dheerendra'

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.login, name="login"),
]
