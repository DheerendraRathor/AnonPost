"""anon_post URL Configuration

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
from django.conf.urls import patterns, url, include
import account.urls
import views
import post.urls
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^account/', include(account.urls, namespace='account')),
    url(r'^home/', include(post.urls, namespace='home')),
]

urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.STATIC_ROOT,
                        }),
                        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT,
                        })
                        )
