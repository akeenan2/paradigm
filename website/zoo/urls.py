# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'zoo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
