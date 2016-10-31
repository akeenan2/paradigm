# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import connection, connections
from django.http import HttpResponseRedirect
from .models import Zoo,Species,Biome,Exhibit,Family
from .update import *

def index(request):
    return render(request,'zoo/index.html')

def list_zoos(request):
    list_zoos = Zoo.objects.all()
    return render(request,'zoo/list_zoos.html',{'list_zoos':list_zoos})

def zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    if request.method == 'POST':
        if request.POST.get('delete'):
            with connection.cursor() as cursor:
                for species in request.POST.getlist('species'):
                    cursor.execute('DELETE FROM Exhibit WHERE zoo_name=%s AND species=%s',[zoo.zoo_name,species])
            zoo = Zoo.objects.get(id=zoo_id)
        elif request.POST.get('add'):
            return HttpResponseRedirect('/zoo/'+zoo_id+'/add/')
    with connection.cursor() as cursor:
        cursor.execute('SELECT Species.id,Species.species,Species.common_name FROM Species,Exhibit WHERE Species.species=Exhibit.species AND Exhibit.zoo_name=%s',[zoo.zoo_name])
        list_species = cursor.fetchall()
    return render(request,'zoo/zoo.html',{'zoo':zoo,'list_species':list_species})

def zoo_add(request,zoo_id):
    if request.method == 'POST':
        if request.POST.get('add'):
            with connection.cursor() as cursor:

def update_zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    if request.method == 'POST':
        save_zoo(request=request,zoo_id=zoo_id)
        return HttpResponseRedirect('/zoo/'+zoo_id+'/')
    return render(request,'zoo/update_zoo.html',{'zoo':zoo})

def list_species(request):
    list_species = Species.objects.all()
    for species in list_species:
        species.common_name = species.common_name.split(';')[0]
    return render(request,'zoo/list_species.html',{'list_species':list_species})

def species(request,species_id):
    species = Species.objects.get(id=species_id)
    species_name = species.common_name.split(';')[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT Zoo.id,Zoo.zoo_name,Zoo.city,Zoo.state,Zoo.address FROM Zoo,Exhibit WHERE Zoo.zoo_name=Exhibit.zoo_name AND Exhibit.species=%s',[species.species])
        list_zoos = cursor.fetchall()
    return render(request,'zoo/species.html',{'species':species,'species_name':species_name,'list_zoos':list_zoos})

def update_species(request,species_id):
    species = Species.objects.get(id=species_id)
    if request.method == 'POST':
        save_species(request=request,species_id=species_id)
        return HttpResponseRedirect('/species/'+species_id+'/')
    species_name = species.common_name.split(';')[0]
    return render(request,'zoo/update_species.html',{'species':species,'species_name':species_name})
