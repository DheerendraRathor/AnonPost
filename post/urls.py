__author__ = 'dheerendra'

from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^admin/$', views.admin_page, name='admin'),
    url(r'^post/(?P<post_id>[0-9]+)/$', views.get_post, name='post'),
    url('^add_post/$', views.add_post, name='add_post'),
    url('^add_reply/(?P<id_>[0-9]+)/$', views.add_reply, name='add_reply'),
    url('^get_posts/$', views.get_posts, name='get_posts'),
    url('^get_replies/(?P<post_id>[0-9]+)/$', views.get_replies, name='get_replies'),
    url('^get_all_posts/$', views.get_all_posts, name='get_all_posts_0'),
    url('^get_all_posts/(?P<offset>[0-9]+)/$', views.get_all_posts, name='get_all_posts')
]
