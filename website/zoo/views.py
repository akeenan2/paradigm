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
    list_species = Species.objects.all()
    zoo = Zoo.objects.get(id=zoo_id)
    if request.method == 'POST':
        if request.POST.get('add'):
            with connection.cursor() as cursor:
                for species in request.POST.getlist('species'):
                    cursor.execute('INSERT INTO Exhibit(species,zoo_name) VALUES(%s,%s)',[species,zoo.zoo_name])
        return HttpResponseRedirect('/zoo/'+zoo_id+'/')
    return render(request,'zoo/zoo_add.html',{'zoo':zoo,'list_species':list_species})

def update_zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Zoo SET zoo_name=%s,city=%s,state=%s,address=%s,latitude=%s,longitude=%s,num_animals=%s,acres=%s,hour_open=%s,hour_close=%s,annual_visitors=%s,website=%s WHERE id=%s',[request.POST.get("zoo_name"),request.POST.get("city"),request.POST.get("state"),request.POST.get("address"),request.POST.get("latitude"),request.POST.get("longitude"),request.POST.get("num_animals"),request.POST.get("acres"),request.POST.get("hour_open"),request.POST.get("hour_close"),request.POST.get("annual_visitors"),request.POST.get("website")])
        return HttpResponseRedirect('/zoo/'+zoo_id+'/')
    return render(request,'zoo/update_zoo.html',{'zoo':zoo})

def list_species(request):
    if request.method == 'POST':
        print 'post'
    list_species = Species.objects.all()
    for species in list_species:
        species.common_name = species.common_name.split(';')[0]
    return render(request,'zoo/list_species.html',{'list_species':list_species})

def species(request,_species):
    species = Species.objects.get(species = _species.replace("_"," "))
    species_name = species.common_name.split(';')[0]
    with connection.cursor() as cursor:
        cursor.execute('SELECT Zoo.id,Zoo.zoo_name,Zoo.city,Zoo.state,Zoo.address FROM Zoo,Exhibit WHERE Zoo.zoo_name=Exhibit.zoo_name AND Exhibit.species=%s',[species.species])
        list_zoos = cursor.fetchall()
    return render(request,'zoo/species.html',{'species':species,'species_name':species_name,'list_zoos':list_zoos})

def update_species(request,_species):
    species = Species.objects.get(species=_species.replace("_"," "))
    if request.method == 'POST':
        with connection.cursor as cursor:
            cursor.execute('UPDATE Species SET species=%s,common_name=%s,genus=%s,familia=%s,ordo=%s,classis=%s,region=%s,habitat=%s,lifespan=%s,status=%s WHERE species=%s',[_species.replace("_"," "),request.POST.get("species"),request.POST.get("common_name"),request.POST.get("genus"),request.POST.get("familia"),request.POST.get("ordo"),request.POST.get("classis"),request.POST.get("region"),request.POST.get("habitat"),request.POST.get("lifespan"),request.POST.get("status")])
            return HttpResponseRedirect('/species/'+_species+'/')
    species_name = species.common_name.split(';')[0]
    return render(request,'zoo/update_species.html',{'species':species,'species_name':species_name})
