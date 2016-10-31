# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Zoo,Species,Biome,Exhibit,Family
from django.db import connection, connections
def index(request):
    return render(request,'zoo/index.html')

def list_zoos(request):
    list_zoos = Zoo.objects.all()
    return render(request,'zoo/list_zoos.html',{'list_zoos':list_zoos})

def zoo(request,zoo_id):
    if request.method == 'POST':
        if request.POST.get('delete'):
            species = Species.objects.filter(id__in=request.POST.getlist('species')).delete()
    zoo = Zoo.objects.get(id=zoo_id)
    with connection.cursor() as cursor:
        cursor.execute('SELECT Species.id,Species.species,Species.common_name FROM Species,Exhibit WHERE Species.species=Exhibit.species AND Exhibit.zoo_name=%s',[zoo.zoo_name])
        list_species = cursor.fetchall()
    return render(request,'zoo/zoo.html',{'zoo':zoo,'list_species':list_species})

def update_zoo(request,zoo_id):
    if request.method == 'POST':
        print 'post'
    zoo= Zoo.objects.get(id=zoo_id)
    return render(request,'zoo/update_zoo.html',{'zoo':zoo})

def species(request,species_id):
    species = Species.objects.get(id=species_id)
    species_name = species.common_name.split(';')[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT Zoo.id,Zoo.zoo_name,Zoo.city,Zoo.state,Zoo.address FROM Zoo,Exhibit WHERE Zoo.zoo_name=Exhibit.zoo_name AND Exhibit.species=%s',[species.species])
        list_zoos = cursor.fetchall()
    return render(request,'zoo/species.html',{'species':species,'species_name':species_name,'list_zoos':list_zoos})

def list_species(request):
    list_species = Species.objects.all()
    for species in list_species:
        species.common_name = species.common_name.split(';')[0]
    return render(request,'zoo/list_species.html',{'list_species':list_species})
