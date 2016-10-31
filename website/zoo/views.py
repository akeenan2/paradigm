# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Zoo,Species,Biome,Exhibit,Family

def index(request):
    return render(request,'zoo/index.html')

def list_zoos(request):
    list_zoos = Zoo.objects.all()
    return render(request,'zoo/list_zoos.html',{'list_zoos':list_zoos})

def zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    list_species = Exhibit.objects.filter(zoo_name__zoo_name=zoo.zoo_name).select_related('specie')
    #list_species = Species.objects.raw('SELECT * FROM Species, Exhibit WHERE Species.species=Exhibit.species');
    return render(request,'zoo/zoo.html',{'zoo':zoo},{'list_species':list_species})

def species(request,species_id):
    species = Species.objects.get(id=species_id)
    species_name = species.common_name.split(';')[0]
    return render(request,'zoo/species.html',{'species':species,'species_name':species_name,'list_zoos':list_zoos})

def list_species(request):
    if request.method == 'POST':
        if request.POST.get('delete'):
            species = Species.objects.filter(id__in=request.POST.getlist('species'))
            for s in species:
                Exhibit.objects.get(species=s).delete()
                s.delete()
    list_species = Species.objects.all()
    for species in list_species:
        species.common_name = species.common_name.split(';')[0]
    return render(request,'zoo/list_species.html',{'list_species':list_species})
