# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Zoo

def index(request):
    zoos = Zoo.objects.all()
    return render(request, 'zoo/zoos.html', {'zoos': zoos})

def zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    return render(request, 'zoo/zoo.html', {'zoo': zoo})

def species(request,species_id):
    species = Zoo.objects.get(id=species_id)
    return render(request, 'zoo/species.html', {'species': species})
