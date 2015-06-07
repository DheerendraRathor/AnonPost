__author__ = 'dheerendra'

from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index),
    url('^add_complaint/$', views.add_complaint),
    url('^add_reply/(?P<id>[0-9]+)/$', views.add_reply),
    url('^get_complaints/$', views.get_complaints),
    url('^get_replies/(?P<complaint_id>[0-9]+)/$', views.get_replies),
    url('^get_all_complaints/(?P<offset>[0-9]+)/$', views.get_all_complaints)
]
