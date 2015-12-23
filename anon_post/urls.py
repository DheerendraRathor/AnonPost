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
import redactor.urls
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

import account.urls
import post.urls
import anon_post.views

urlpatterns = [
    url(r'^$', anon_post.views.index, name='index'),
    url(r'^superuser/', include(admin.site.urls)),
    url(r'^redactor/', include(redactor.urls)),
    url(r'^about/$', anon_post.views.about, name='about'),
    url(r'^account/', include(account.urls, namespace='account')),
    url(r'^sites/$', anon_post.views.sites, name='sites'),
    url(r'^sites/(?P<site_id>\d+)/', include(post.urls, namespace='home')),
]

urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.STATIC_ROOT,
                        }),
                        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT,
                        })
                        )
