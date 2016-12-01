# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import connection, connections
from django.http import HttpResponseRedirect
from math import ceil
from .models import *
from .functions import convert_time,revert_time

def index(request):
    return render(request,'zoo/index.html')

def help(request):
    return render(request,'zoo/help.html')

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
# only use pagination if more than 10 entries
    if len(list_species) > 10:
        use_pagination = 1
    else:
        use_pagination = 0
# make time human readable
    time_open = convert_time(zoo.time_open)
    time_open = time_open['hour'] + ':' + time_open['minute'] + time_open['period']
    time_close = convert_time(zoo.time_close)
    time_close = time_close['hour'] + ':' + time_close['minute'] + time_close['period']
    context = {
        'zoo':zoo,
        'time_open':time_open,
        'time_close':time_close,
        'list_species':list_species,
        'use_pagination':use_pagination
    }
    return render(request,'zoo/zoo.html',context)

def update_exhibit(request,_zoo_name,operation):
    zoo_name = _zoo_name.replace("_"," ");
    zoo = Zoo.objects.get(zoo_name=zoo_name)

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
    # convert time to database format
        time_open = revert_time(request.POST.get("open_hour"),request.POST.get("open_minute"),request.POST.get("open_period"))
        time_close = revert_time(request.POST.get("close_hour"),request.POST.get("close_minute"),request.POST.get("close_period"))
        with connection.cursor() as cursor:
            cursor.execute('UPDATE Zoo SET zoo_name=%s,city=%s,state=%s,address=%s,latitude=%s,longitude=%s,num_animals=%s,acres=%s,time_open=%s,time_close=%s,annual_visitors=%s,website=%s WHERE zoo_name=%s',[request.POST.get("zoo_name"),request.POST.get("city"),request.POST.get("state"),request.POST.get("address"),request.POST.get("latitude"),request.POST.get("longitude"),request.POST.get("num_animals"),request.POST.get("acres"),time_open,time_close,request.POST.get("annual_visitors"),request.POST.get("website"),zoo_name])
    # redirect back to the zoo detail page
        return HttpResponseRedirect('/zoo/'+_zoo_name+'/')
    states = State.objects.values_list('abbrv',flat=True)
    time_open = convert_time(zoo.time_open)
    time_close = convert_time(zoo.time_close)
    hours = []
    for i in range(1,13):
        hours.append(str(i))
    minutes = ['00','15','30','45']
    periods = ['AM','PM']
    context = {
        'zoo':zoo,
        'states':states,
        'hours':hours,
        'minutes':minutes,
        'periods':periods,
        'open_hour':time_open['hour'],
        'open_minute':time_open['minute'],
        'open_period':time_open['period'],
        'close_hour':time_close['hour'],
        'close_minute':time_close['minute'],
        'close_period':time_close['period']
    }
    return render(request,'zoo/update_zoo.html',context)

def list_species(request):
# default values
    habitats = Habitat.objects.values_list('habitat',flat=True)
    regions = Region.objects.values_list('region',flat=True)
    statuses = Status.objects.values_list('status',flat=True)
    families = Classification.objects.values_list('family',flat=True)
    select_habitats = []
    select_regions = []
    select_statuses = []
    select_families = []
# empty if no conditions
    conditions = ''
    if request.method == 'POST':
        if request.POST.get('update'):
        # retrive the information selected
            select_habitats = request.POST.getlist('habitats')
            select_regions = request.POST.getlist('regions')
            select_statuses = request.POST.getlist('statuses')
            select_families = request.POST.getlist('families')
        # if a habitat was selected
            if select_habitats:
            # remove selected habitats from list of habitats (so as to display seperately)
                habitats = sorted(set(habitats) - set(select_habitats))
            # add parenthesis to seperate the lists
                conditions = conditions + ' ('
                for habitat in select_habitats[:-1]:
                    conditions = conditions + 'Species.habitat LIKE "%' + habitat + '%" OR '
                conditions = conditions + 'Species.habitat LIKE "%' + select_habitats[-1] + '%")'
        # if a region was selected
            if select_regions:
                regions = sorted(set(regions) - set(select_regions))
                regions.sort()
                if conditions: # add an and to connect conditions
                    conditions = conditions + ' AND';
                conditions = conditions + ' ('
                for region in select_regions[:-1]:
                    conditions = conditions + 'Species.region LIKE "%' + region + '%" OR '
                conditions = conditions + 'Species.region LIKE "%' + select_regions[-1] + '%")';
        # if a status was selected
            if select_statuses:
                statuses = sorted(set(statuses) - set(select_statuses))
            # if a condition was selected before, concatenate new list to end
                if conditions:
                    conditions = conditions + ' AND';
                conditions = conditions + ' ('
                for status in select_statuses[:-1]:
                    conditions = conditions + 'Species.status="' + status + '" OR '
                conditions = conditions + 'Species.status="' + select_statuses[-1] + '")'
        # if a family was selected
            if select_families:
                families = sorted(set(families) - set(select_families))
                if conditions:
                    conditions = conditions + ' AND';
                conditions = conditions + ' ('
                for family in select_families[:-1]:
                    conditions = conditions + 'Species.family="' + family + '" OR '
                conditions = conditions + 'Species.family="' + select_families[-1] +'")'
        # if selected conditions, add to the query
            if conditions:
                conditions = ' WHERE' + conditions;
# query the database for all the selected species
    with connection.cursor() as cursor:
        query = 'SELECT Species.species,Species.common_name FROM Species' + conditions
        cursor.execute(query)
        list_species = cursor.fetchall()
# descriptions
    habitats_descr = Habitat.objects.all()
    regions_descr = Region.objects.all()
    statuses_descr = Status.objects.all()
    families_descr = Classification.objects.all()
# only use pagination if more than 10 entries
    if len(list_species) > 10:
        use_pagination = 1
    else:
        use_pagination = 0
# variables to pass into html
    context = {
        'list_species':list_species,
        'families':families,
        'habitats':habitats,
        'regions':regions,
        'statuses':statuses,
        'select_families':select_families,
        'select_habitats':select_habitats,
        'select_regions':select_regions,
        'select_statuses':select_statuses,
        'habitats_descr':habitats_descr,
        'regions_descr':regions_descr,
        'statuses_descr':statuses_descr,
        'families_descr':families_descr,
        'use_pagination':use_pagination,
    }
    return render(request,'zoo/list_species.html',context)

def species(request,_species):
    if request.method == 'POST':
        if request.POST.get('update'):
            species = request.POST.get('update');
            _species = species.replace(" ","_")
            return HttpResponseRedirect('/species/'+_species+'/update/')
    species = Species.objects.get(species=_species.replace("_"," "))
    species_name = species.common_name.split(';')[0]
    if len(species.common_name.split(';')) > 1:
        other_names = species.common_name.split(';')[1:]
    else:
        other_names = ''
# select all zoos that exhibit the specific species
    with connection.cursor() as cursor:
        cursor.execute('SELECT Zoo.zoo_name,Zoo.city,Zoo.state,Zoo.address FROM Zoo,Exhibit WHERE Zoo.zoo_name=Exhibit.zoo_name AND Exhibit.species=%s',[species.species])
        list_zoos = cursor.fetchall()
    # fetch relevant information to the family of the current species
        cursor.execute('SELECT Classification.family,Classification.ordr,Classification.clss,Classification.phylm FROM Classification WHERE Classification.family=%s',[species.family.family])
    # all species of the same family
        cursor.execute('SELECT s.species FROM Species s WHERE s.family=%s AND s.species!=%s ORDER BY RAND() LIMIT 5',[species.family.family,species.species])
        related_species = cursor.fetchall()
        if len(related_species) < 5:
        # same order
            cursor.execute('SELECT s.species FROM Species s, Classification c WHERE c.family=s.family AND c.ordr=%s AND s.species!=%s ORDER BY RAND() LIMIT 5',[species.family.ordr,species.species])
            related_species = cursor.fetchall()
            if len(related_species) < 5:
            # same class
                cursor.execute('SELECT s.species FROM Species s, Classification c WHERE c.family=s.family AND c.clss=%s AND s.species!=%s ORDER BY RAND() LIMIT 5',[species.family.clss,species.species])
                related_species = cursor.fetchall()
                if len(related_species) < 5:
                # same phylum
                    cursor.execute('SELECT s.species FROM Species s, Classification c WHERE c.family=s.family AND c.phylum=%s AND s.species!=%s ORDER BY RAND() LIMIT 5',[species.family.phylum,species.species])
                    related_species = cursor.fetchall()
# same region and habitat
    regions = species.region.split(';')
    habitats = species.habitat.split(';')
    conditions = ' WHERE ('
    for region in regions[:-1]:
        conditions = conditions + 'Species.region LIKE "%' + region + '%" OR '
    conditions = conditions + 'Species.region LIKE "%' + regions[-1] + '%")';
    conditions = conditions + ' AND ('
    for habitat in habitats[:-1]:
        conditions = conditions + 'Species.habitat LIKE "%' + habitat + '%" OR '
    conditions = conditions + 'Species.habitat LIKE "%' + habitats[-1] + '%")';
    for specie in related_species:
        conditions = conditions + ' AND Species.species != "' + specie[0] + '"'
# query the database for all the related species
    with connection.cursor() as cursor:
        query = 'SELECT Species.species FROM Species' + conditions + ' ORDER BY RAND() LIMIT 5'
        cursor.execute(query)
        similar_species = cursor.fetchall()
# only use pagination if more than 10 entries
    if len(list_zoos) > 10:
        use_pagination = 1
    else:
        use_pagination = 0
    # variables to pass into html
    context = {
        'species':species,
        'species_name':species_name,
        'other_names':other_names,
        'list_zoos':list_zoos,
        'related_species':related_species,
        'similar_species':similar_species,
        'use_pagination':use_pagination
    }
    return render(request,'zoo/species.html',context)

def update_species(request,_species):
    families = Classification.objects.values_list('family',flat=True)
    statuses = Status.objects.order_by('level').values_list('status',flat=True)
    species = Species.objects.get(species=_species.replace("_"," "))
# update the data based on user input
    if request.method == 'POST':
        if request.POST.get('submit-add-region'):
        # add the new region
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Region(region,descr) values(%s,%s)',[request.POST.get('new-region'),request.POST.get('region-descr')])
        elif request.POST.get('submit-add-habitat'):
        # add the new habitat
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Habitat(habitat,descr) values(%s,%s)',[request.POST.get('new-habitat'),request.POST.get('habitat-descr')])
        elif request.POST.get('submit-add-family'):
        # add family to database
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Classification(family,ordr,clss,phylm,kingdm,descr) values(%s,%s,%s,%s,%s,%s)',[request.POST.get('new-family'),request.POST.get('ordr'),request.POST.get('clss'),request.POST.get('phylm'),request.POST.get('kingdm'),request.POST.get('family-descr')])
        elif request.POST.get('submit-remove-region'):
        # remove regions
            with connection.cursor() as cursor:
                for region in request.POST.getlist('remove-regions'):
                    cursor.execute('DELETE FROM Region WHERE region=%s',[region])
        elif request.POST.get('submit-remove-habitat'):
        # remove habitats
            with connection.cursor() as cursor:
                for habitat in request.POST.getlist('remove-habitats'):
                    cursor.execute('DELETE FROM Habitat WHERE habitat=%s',[habitat])
        elif request.POST.get('submit-remove-family'):
        # remove families
            with connection.cursor() as cursor:
                for family in request.POST.getlist('remove-families'):
                    cursor.execute('DELETE FROM Classification WHERE family=%s',[family])
        elif request.POST.get('submit'):
        # update the species
            select_habitats = request.POST.getlist('update-habitats')
            select_regions = request.POST.getlist('update-regions')
            habitats = ''
            for habitat in select_habitats[:-1]:
                habitats = habitats + habitat + ';'
            habitats = habitats + select_habitats[-1]
            regions = ''
            for region in select_regions[:-1]:
                regions = regions + region + ';'
            regions = regions + select_regions[-1]
        # update the species with a query
            with connection.cursor() as cursor:
                cursor.execute('UPDATE Species SET species=%s,common_name=%s,genus=%s,family=%s,region=%s,habitat=%s,status=%s WHERE species=%s',[request.POST.get("species"),request.POST.get("common_name"),request.POST.get("genus"),request.POST.get("family"),regions,habitats,request.POST.get("update-status"),_species.replace("_"," ")])
            # redirect back to the species information page
                return HttpResponseRedirect('/species/'+_species+'/')
# fetch the current data
    all_habitats = Habitat.objects.values_list('habitat',flat=True)
    all_regions = Region.objects.values_list('region',flat=True)
# tuples for the information (0 if not selected, 1 if selected)
    def_habitats = []
    def_regions = []
# sort through the regions
    for region in all_regions:
        if region in species.region.split(';'):
            def_regions.append(('1',region))
        else:
            def_regions.append(('0',region))
# sort through the habitats
    for habitat in all_habitats:
        if habitat in species.habitat.split(';'):
            def_habitats.append(('1',habitat))
        else:
            def_habitats.append(('0',habitat))
# show only the first common name
    species_name = species.common_name.split(';')[0]
    context = {
        'families':families,
        'def_habitats':def_habitats,
        'habitats':all_habitats,
        'def_regions':def_regions,
        'regions':all_regions,
        'statuses':statuses,
        'species':species,
        'species_name':species_name
    }
    return render(request,'zoo/update_species.html',context)

def add_species(request):
# add the species based on user input
    if request.method == 'POST':
        if request.POST.get('submit-add-region'):
        # add the new region
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Region(region,descr) values(%s,%s)',[request.POST.get('new-region'),request.POST.get('region-descr')])
        elif request.POST.get('submit-add-habitat'):
        # add the new habitat
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Habitat(habitat,descr) values(%s,%s)',[request.POST.get('new-habitat'),request.POST.get('habitat-descr')])
        elif request.POST.get('submit-add-family'):
        # add family to database
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Classification(family,ordr,clss,phylm,kingdm,descr) values(%s,%s,%s,%s,%s,%s)',[request.POST.get('new-family'),request.POST.get('ordr'),request.POST.get('clss'),request.POST.get('phylm'),request.POST.get('kingdm'),request.POST.get('family-descr')])
        elif request.POST.get('submit-remove-region'):
        # remove regions
            with connection.cursor() as cursor:
                for region in request.POST.getlist('remove-regions'):
                    cursor.execute('DELETE FROM Region WHERE region=%s',[region])
        elif request.POST.get('submit-remove-habitat'):
        # remove habitats
            with connection.cursor() as cursor:
                for habitat in request.POST.getlist('remove-habitats'):
                    cursor.execute('DELETE FROM Habitat WHERE habitat=%s',[habitat])
        elif request.POST.get('submit-remove-family'):
        # remove families
            with connection.cursor() as cursor:
                for family in request.POST.getlist('remove-families'):
                    cursor.execute('DELETE FROM Classification WHERE family=%s',[family])
        elif request.POST.get('submit'):
        # get input and modify to fit database format
            select_habitats = request.POST.getlist('add-habitats')
            select_regions = request.POST.getlist('add-regions')
            habitats = ''
            for habitat in select_habitats[:-1]:
                habitats = habitats + habitat + ';'
            habitats = habitats + select_habitats[-1]
            regions = ''
            for region in select_regions[:-1]:
                regions = regions + region + ';'
            regions = regions + select_regions[-1]
        # update the database
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Species(species,common_name,genus,family,region,habitat,status) values(%s,%s,%s,%s,%s,%s,%s)',[request.POST.get('species'),request.POST.get('common_name'),request.POST.get('genus'),request.POST.get('family'),regions,habitats,request.POST.get('add-status')])
            return HttpResponseRedirect('/species/')
    # if chose to add a family, redirect to appropriate page
        elif request.POST.get('add-family'):
            return HttpResponseRedirect('/add/family/'+request.POST.get('family').replace(" ","_")+'/')
    habitats = Habitat.objects.values_list('habitat',flat=True)
    families = Classification.objects.values_list('family',flat=True)
    regions = Region.objects.values_list('region',flat=True)
    statuses = Status.objects.values_list('status',flat=True)
    context = {
        'families':families,
        'habitats':habitats,
        'regions':regions,
        'statuses':statuses,
    }
    return render(request,'zoo/add_species.html',context)
