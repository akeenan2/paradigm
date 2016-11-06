# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import connection, connections
from django.http import HttpResponseRedirect
from math import ceil
from .models import Zoo,Species,Classification,Exhibit,Habitat
from .update import *

def index(request):
    return render(request,'zoo/index.html')

def list_zoos(request):
    list_zoos = Zoo.objects.all()
    return render(request,'zoo/list_zoos.html',{'list_zoos':list_zoos})

def zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    if request.method == 'POST':
        if request.POST.get('remove'):
            return HttpResponseRedirect('/zoo/'+zoo_id+'/remove/')
        elif request.POST.get('add'):
            return HttpResponseRedirect('/zoo/'+zoo_id+'/add/')
    with connection.cursor() as cursor:
        cursor.execute('SELECT Species.species,Species.common_name FROM Species,Exhibit WHERE Species.species=Exhibit.species AND Exhibit.zoo_name=%s',[zoo.zoo_name])
        list_species = cursor.fetchall()
    num_species = len(list_species)
    return render(request,'zoo/zoo.html',{'zoo':zoo,'list_species':list_species,'num_species':num_species})

def update_exhibit(request,zoo_id,operation):
    zoo = Zoo.objects.get(id=zoo_id)
    list_species = Species.objects.all()
    with connection.cursor() as cursor:
        if operation == 'add':
            cursor.execute('SELECT Species.species,Species.common_name FROM Species WHERE Species.species NOT IN (SELECT Species.species FROM Species,Exhibit,Zoo WHERE Exhibit.species=Species.species AND Exhibit.zoo_name=Zoo.zoo_name AND Exhibit.zoo_name=%s)',[zoo.zoo_name])
        elif operation == 'remove':
            cursor.execute('SELECT Species.species,Species.common_name FROM Species,Exhibit,Zoo WHERE Exhibit.species=Species.species AND Exhibit.zoo_name=Zoo.zoo_name AND Exhibit.zoo_name=%s',[zoo.zoo_name])
        list_species = cursor.fetchall()
    if request.method == 'POST':
        if request.POST.get('operation'):
            with connection.cursor() as cursor:
                for species in request.POST.getlist('species'):
                    if operation == 'add':
                        cursor.execute('INSERT INTO Exhibit(species,zoo_name) VALUES(%s,%s)',[species,zoo.zoo_name])
                    elif operation == 'remove':
                        cursor.execute('DELETE FROM Exhibit WHERE zoo_name=%s AND species=%s',[zoo.zoo_name,species])
        return HttpResponseRedirect('/zoo/'+zoo_id+'/')
    return render(request,'zoo/update_exhibit.html',{'zoo':zoo,'list_species':list_species,'operation':operation})

def update_zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Zoo SET zoo_name=%s,city=%s,state=%s,address=%s,latitude=%s,longitude=%s,num_animals=%s,acres=%s,hour_open=%s,hour_close=%s,annual_visitors=%s,website=%s WHERE id=%s',[request.POST.get("zoo_name"),request.POST.get("city"),request.POST.get("state"),request.POST.get("address"),request.POST.get("latitude"),request.POST.get("longitude"),request.POST.get("num_animals"),request.POST.get("acres"),request.POST.get("hour_open"),request.POST.get("hour_close"),request.POST.get("annual_visitors"),request.POST.get("website"),zoo_id])
        return HttpResponseRedirect('/zoo/'+zoo_id+'/')
    return render(request,'zoo/update_zoo.html',{'zoo':zoo})

def list_species(request):
    list_species = Species.objects.all()
    for species in list_species:
        species.common_name = species.common_name.split(';')[0]
    return render(request,'zoo/list_species.html',{'list_species':list_species})

def species(request,_species):
    if request.method == 'POST':
        if request.POST.get('update'):
            species = request.POST.get('update');
            _species = species.replace(" ","_")
            return HttpResponseRedirect('/species/'+_species+'/update/')
    species = Species.objects.get(species=_species.replace("_"," "))
    classification = Classification.objects.get(family=species.family);
    species_name = species.common_name.split(';')[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT Zoo.id,Zoo.zoo_name,Zoo.city,Zoo.state,Zoo.address FROM Zoo,Exhibit WHERE Zoo.zoo_name=Exhibit.zoo_name AND Exhibit.species=%s',[species.species])
        list_zoos = cursor.fetchall()
    return render(request,'zoo/species.html',{'species':species,'species_name':species_name,'classification':classification,'list_zoos':list_zoos})

def update_species(request,_species):
    species = Species.objects.get(species=_species.replace("_"," "))
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Species SET species=%s,common_name=%s,genus=%s,family=%s,region=%s,habitat=%s,lifespan=%s,status=%s WHERE species=%s',[request.POST.get("species"),request.POST.get("common_name"),request.POST.get("genus"),request.POST.get("family"),request.POST.get("region"),request.POST.get("habitat"),request.POST.get("lifespan"),request.POST.get("status"),_species.replace("_"," ")])
            return HttpResponseRedirect('/species/'+_species+'/')
    species_name = species.common_name.split(';')[0]
    return render(request,'zoo/update_species.html',{'species':species,'species_name':species_name})
