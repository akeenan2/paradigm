# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Zoo

def index(request):
    query_results = Zoo.objects.all()
    return render(request, 'zoo/index.html', {'query_results': query_results})