__author__ = 'dheerendra'

from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^admin/$', views.admin_page, name='admin'),
    url(r'^complaint/(?P<complaint_id>[0-9]+)/$', views.get_complaint, name='post'),
    url('^add_complaint/$', views.add_complaint, name='add_post'),
    url('^add_reply/(?P<id_>[0-9]+)/$', views.add_reply, name='add_reply'),
    url('^get_complaints/$', views.get_complaints, name='get_posts'),
    url('^get_replies/(?P<complaint_id>[0-9]+)/$', views.get_replies, name='get_replies'),
    url('^get_all_complaints/$', views.get_all_complaints, name='get_all_posts_0'),
    url('^get_all_complaints/(?P<offset>[0-9]+)/$', views.get_all_complaints, name='get_all_posts')
]
