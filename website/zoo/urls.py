# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'zoo'
urlpatterns = [
    url(r'^$',views.index),
    url(r'^zoo/$',views.list_zoos),
    url(r'^zoo/(?P<_zoo_name>.[^/]+)/$',views.zoo),
    url(r'^zoo/(?P<_zoo_name>.[^/]+)/(?P<operation>add|remove)/$',views.update_exhibit),
    url(r'^zoo/(?P<_zoo_name>.[^/]+)/update/$',views.update_zoo),
    url(r'^species/$',views.list_species),
    url(r'^species/(?P<_species>.[^/]+)/$',views.species),
    url(r'^species/(?P<_species>.[^/]+)/update/$',views.update_species),
    url(r'^add/species/$',views.add_species),
]
