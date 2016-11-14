# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import connection, connections
from django.http import HttpResponseRedirect
from math import ceil
from .models import Zoo,Species,Classification,Exhibit,Habitat,Region,Status

def index(request):
    return render(request,'zoo/index.html')

def list_zoos(request):
# select all the objects in the list of zoos
    list_zoos = Zoo.objects.all()
    return render(request,'zoo/list_zoos.html',{'list_zoos':list_zoos})

def zoo(request,_zoo_name):
# replace the underscores with spaces
    zoo_name = _zoo_name.replace("_"," ");
# select all objects from the Zoo database with the given zoo name
    zoo = Zoo.objects.get(zoo_name=zoo_name)
# if a post request was submitted
    if request.method == 'POST':
        if request.POST.get('remove'):
            return HttpResponseRedirect('/zoo/'+_zoo_name+'/remove/')
        elif request.POST.get('add'):
            return HttpResponseRedirect('/zoo/'+_zoo_name+'/add/')
# query the database for the zoo's animal exhibits
    with connection.cursor() as cursor:
        cursor.execute('SELECT Species.species,Species.common_name FROM Species,Exhibit WHERE Species.species=Exhibit.species AND Exhibit.zoo_name=%s',[zoo.zoo_name])
        list_species = cursor.fetchall()
    num_species = len(list_species)
    return render(request,'zoo/zoo.html',{'zoo':zoo,'list_species':list_species,'num_species':num_species})

def update_exhibit(request,_zoo_name,operation):
    zoo_name = _zoo_name.replace("_"," ");
    zoo = Zoo.objects.get(zoo_name=zoo_name)
    list_species = Species.objects.all()
    with connection.cursor() as cursor:
    # select all species animals not currently exhibited
        if operation == 'add':
            cursor.execute('SELECT Species.species,Species.common_name FROM Species WHERE Species.species NOT IN (SELECT Species.species FROM Species,Exhibit,Zoo WHERE Exhibit.species=Species.species AND Exhibit.zoo_name=Zoo.zoo_name AND Exhibit.zoo_name=%s)',[zoo.zoo_name])
    # select all species exhibited
        elif operation == 'remove':
            cursor.execute('SELECT Species.species,Species.common_name FROM Species,Exhibit,Zoo WHERE Exhibit.species=Species.species AND Exhibit.zoo_name=Zoo.zoo_name AND Exhibit.zoo_name=%s',[zoo.zoo_name])
        list_species = cursor.fetchall()
    if request.method == 'POST':
        if request.POST.get('operation'):
            with connection.cursor() as cursor:
                for species in request.POST.getlist('species'):
                # add the species to the zoo exhibit
                    if operation == 'add':
                        cursor.execute('INSERT INTO Exhibit(species,zoo_name) VALUES(%s,%s)',[species,zoo.zoo_name])
                # remove the species from the zoo exhibit
                    elif operation == 'remove':
                        cursor.execute('DELETE FROM Exhibit WHERE zoo_name=%s AND species=%s',[zoo.zoo_name,species])
        return HttpResponseRedirect('/zoo/'+_zoo_name+'/')
    return render(request,'zoo/update_exhibit.html',{'zoo':zoo,'list_species':list_species,'operation':operation})

def update_zoo(request,_zoo_name):
    zoo_name = _zoo_name.replace("_"," ");
    zoo = Zoo.objects.get(zoo_name=zoo_name)
# update the specific zoo
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Zoo SET zoo_name=%s,city=%s,state=%s,address=%s,latitude=%s,longitude=%s,num_animals=%s,acres=%s,hour_open=%s,hour_close=%s,annual_visitors=%s,website=%s WHERE zoo_name=%s',[request.POST.get("zoo_name"),request.POST.get("city"),request.POST.get("state"),request.POST.get("address"),request.POST.get("latitude"),request.POST.get("longitude"),request.POST.get("num_animals"),request.POST.get("acres"),request.POST.get("hour_open"),request.POST.get("hour_close"),request.POST.get("annual_visitors"),request.POST.get("website"),zoo_name])
    # redirect back to the zoo detail page
        return HttpResponseRedirect('/zoo/'+_zoo_name+'/')
    return render(request,'zoo/update_zoo.html',{'zoo':zoo})

def list_species(request):
    habitats = Habitat.objects.all()
    families = Classification.objects.all()
    regions = Region.objects.all()
    statuses = Status.objects.all()
    if request.method == 'POST':
# to be modified
        list_species = Species.objects.all()
# default everything displayed
    else:
        list_species = Species.objects.all()
        for species in list_species:
            species.common_name = species.common_name.split(';')[0]
    return render(request,'zoo/list_species.html',{'list_species':list_species,'families':families,'habitats':habitats,'regions':regions,'statuses':statuses})

def species(request,_species):
    if request.method == 'POST':
        if request.POST.get('update'):
            species = request.POST.get('update');
            _species = species.replace(" ","_")
            return HttpResponseRedirect('/species/'+_species+'/update/')
    species = Species.objects.get(species=_species.replace("_"," "))
    classification = Classification.objects.get(family=species.family);
    species_name = species.common_name.split(';')[0]
# select all zoos that exhibit the specific species
    with connection.cursor() as cursor:
        cursor.execute('SELECT Zoo.zoo_name,Zoo.city,Zoo.state,Zoo.address FROM Zoo,Exhibit WHERE Zoo.zoo_name=Exhibit.zoo_name AND Exhibit.species=%s',[species.species])
        list_zoos = cursor.fetchall()
    return render(request,'zoo/species.html',{'species':species,'species_name':species_name,'classification':classification,'list_zoos':list_zoos})

def update_species(request,_species):
    species = Species.objects.get(species=_species.replace("_"," "))
    if request.method == 'POST':
# update the species with a query
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Species SET species=%s,common_name=%s,genus=%s,family=%s,region=%s,habitat=%s,status=%s WHERE species=%s',[request.POST.get("species"),request.POST.get("common_name"),request.POST.get("genus"),request.POST.get("family"),request.POST.get("region"),request.POST.get("habitat"),request.POST.get("status"),_species.replace("_"," ")])
        # redirect back to the species information page
            return HttpResponseRedirect('/species/'+_species+'/')
# show only the first common name
    species_name = species.common_name.split(';')[0]
    return render(request,'zoo/update_species.html',{'species':species,'species_name':species_name})
