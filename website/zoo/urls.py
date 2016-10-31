# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'zoo'
urlpatterns = [
    url(r'^$',views.index),
    url(r'^zoo/$',views.list_zoos),
    url(r'^zoo/(?P<zoo_id>[0-9]+)/$',views.zoo),
    url(r'^zoo/(?P<zoo_id>[0-9]+)/(?P<operation>('add','delete'))/$',views.update_exhibit),
    url(r'^zoo/(?P<zoo_id>[0-9]+)/update/$',views.update_zoo),
    url(r'^species/$',views.list_species),
    url(r'^species/(?P<_species>\w+)/$',views.species),
    url(r'^species/(?P<_species>\w+)/update/$',views.update_species),
]
