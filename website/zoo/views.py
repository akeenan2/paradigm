# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Zoo, Species, Biome

def index(request):
    list_zoos = Zoo.objects.all()
    return render(request, 'zoo/list_zoos.html', {'list_zoos': list_zoos})

def zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    return render(request, 'zoo/zoo.html', {'zoo': zoo})

def species(request,species_id):
    species = Species.objects.get(id=species_id)
    species_name = species.split(';')[0]
    return render(request, 'zoo/species.html', {'species': species, 'species_name': species_name})

def list_species(request,common_name="all",genus="all",familia="all",ordo="all",classis="all",region="all",habitat="all",lifespan=-1,status="all"):
    list_species = Species.objects.all()
    return render(request, 'zoo/list_species.html', {'list_species': list_species})