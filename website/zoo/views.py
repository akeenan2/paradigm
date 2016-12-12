# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db import connection, connections
from django.http import HttpResponseRedirect
from math import ceil
from .models import *
from .functions import convert_time,revert_time
from django.utils.safestring import mark_safe
import json

def index(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT phylm FROM Classification GROUP BY phylm')
        phylums = cursor.fetchall()
        phylums_dict = dict()
        for p in phylums:

            cursor.execute('SELECT clss FROM Classification WHERE phylm=%s GROUP BY clss',[p[0]])
            classes = cursor.fetchall()
            classes_dict = dict()
            for c in classes:

                cursor.execute('SELECT ordr FROM Classification WHERE clss=%s GROUP BY ordr',[c[0]])
                orders = cursor.fetchall()
                orders_dict = dict()
                for o in orders:

                    cursor.execute('SELECT family FROM Classification WHERE ordr=%s GROUP BY family',[o[0]])
                    families = cursor.fetchall()
                    families_dict = dict()
                    for f in families:

                        cursor.execute('SELECT genus FROM Classification c,Species s WHERE c.family=%s AND c.family=s.family GROUP BY s.genus',[f[0]])
                        genus = cursor.fetchall()
                        genus_dict = dict()
                        for g in genus:

                            cursor.execute('SELECT species FROM Species WHERE genus=%s',[g[0]])
                            species = cursor.fetchall()
                            species_children = []
                            for s in species:
                                species_children.append({'name':s[0]})
                            genus_dict[g[0]] = species_children

                        genus_children = []
                        for g in genus:
                            genus_children.append({'name':g[0],'children':genus_dict[g[0]]})
                        families_dict[f[0]] = genus_children

                    family_children = []
                    for f in families:
                        family_children.append({'name':f[0],'children':families_dict[f[0]]})
                    orders_dict[o[0]] = family_children

                order_children = []
                for o in orders:
                    order_children.append({'name':o[0],'children':orders_dict[o[0]]})
                classes_dict[c[0]] = order_children

            class_children = []
            for c in classes:  
                class_children.append({'name':c[0],'children':classes_dict[c[0]]})
            phylums_dict[p[0]] = class_children

        phylum_children = []
        for p in phylums:
            phylum_children.append({'name':p[0],'children':phylums_dict[p[0]]})
    
    classification = {"name":"animalia","children":phylum_children}
    classification_json = json.dumps(classification)

    context = {
        'classification_json':(mark_safe(classification_json))
    }

    return render(request,'zoo/index.html',context)

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
# get the relevant species from the database
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
                        cursor.execute('INSERT INTO Exhibit(species,zoo_name) VALUES(%s,%s)',[species.lower(),zoo.zoo_name])
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
        if request.POST.get('update'):
        # convert time to database format
            time_open = revert_time(request.POST.get("open_hour"),request.POST.get("open_minute"),request.POST.get("open_period"))
            time_close = revert_time(request.POST.get("close_hour"),request.POST.get("close_minute"),request.POST.get("close_period"))
            with connection.cursor() as cursor:
                cursor.execute('UPDATE Zoo SET zoo_name=%s,city=%s,state=%s,address=%s,latitude=%s,longitude=%s,num_animals=%s,acres=%s,time_open=%s,time_close=%s,annual_visitors=%s,website=%s WHERE zoo_name=%s',[request.POST.get("zoo_name"),request.POST.get("city"),request.POST.get("state"),request.POST.get("address"),request.POST.get("latitude"),request.POST.get("longitude"),request.POST.get("num_animals"),request.POST.get("acres"),time_open,time_close,request.POST.get("annual_visitors"),request.POST.get("website").lower(),zoo_name])
        # redirect back to the zoo detail page
            return HttpResponseRedirect('/zoo/'+[request.POST.get("zoo_name").replace("_"," ")+'/')
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
    statuses = Status.objects.order_by('level').values_list('status',flat=True)
    families = Classification.objects.values_list('family',flat=True)
    keywords = ''
    select_habitats = []
    select_regions = []
    select_statuses = []
    select_families = []
# empty if no conditions
    conditions = ''
    query = 'SELECT Species.species,Species.common_name,Species.family FROM Species'
    if request.method == 'POST':
        if request.POST.get('update'):
        # retrive the information selected
            select_habitats = request.POST.getlist('habitats')
            select_regions = request.POST.getlist('regions')
            select_statuses = request.POST.getlist('statuses')
            select_families = request.POST.getlist('families')
            keywords = request.POST.get('keywords')
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
                query = query + ' WHERE' + conditions
        # if keywords entered, check against common name and family description
            if keywords:
                conditions = ' AND '
                list_keywords = keywords.split(' ')
                for keyword in list_keywords[:-1]:
                    conditions = conditions + '(S.common_name LIKE "%' + keyword + '%" OR c.descr LIKE "%' + keyword + '%") AND'
                conditions = conditions + ' (S.common_name LIKE "%' + list_keywords[-1] + '%" OR c.descr LIKE "%' + list_keywords[-1] + '%")'
                query = 'SELECT S.species, S.common_name FROM Classification c, (' + query + ') S WHERE S.family=c.family' + conditions

# query the database for all the selected species
    with connection.cursor() as cursor:
        cursor.execute(query)
        list_species = cursor.fetchall()
# descriptions
    habitats_descr = Habitat.objects.all()
    regions_descr = Region.objects.all()
    statuses_descr = Status.objects.order_by('level').all()
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
        'keywords':keywords,
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
# no repeating species
    for specie in related_species:
        conditions = conditions + ' AND Species.species != "' + specie[0] + '"'
# exclude the current species
    conditions = conditions + ' AND Species.species != "' + species.species + '"'
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
                cursor.execute('INSERT INTO Region(region,descr) values(%s,%s)',[request.POST.get('new-region').lower(),request.POST.get('region-descr').lower()])
        elif request.POST.get('submit-add-habitat'):
        # add the new habitat
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Habitat(habitat,descr) values(%s,%s)',[request.POST.get('new-habitat').lower(),request.POST.get('habitat-descr').lower()])
        elif request.POST.get('submit-add-family'):
        # add family to database
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Classification(family,ordr,clss,phylm,kingdm,descr) values(%s,%s,%s,%s,%s,%s)',[request.POST.get('new-family').lower(),request.POST.get('ordr').lower(),request.POST.get('clss').lower(),request.POST.get('phylm').lower(),request.POST.get('kingdm').lower(),request.POST.get('family-descr').lower()])
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
        elif request.POST.get('update'):
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
                cursor.execute('UPDATE Species SET species=%s,common_name=%s,genus=%s,family=%s,region=%s,habitat=%s,status=%s WHERE species=%s',[request.POST.get("species").lower(),request.POST.get("common_name"),request.POST.get("genus").lower(),request.POST.get("family"),regions,habitats,request.POST.get("update-status"),_species.replace("_"," ")])
            # redirect back to the species information page
                return HttpResponseRedirect('/species/'+request.POST.get('species').replace(" ","_")+'/')
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
                cursor.execute('INSERT INTO Region(region,descr) values(%s,%s)',[request.POST.get('new-region').lower(),request.POST.get('region-descr').lower()])
        elif request.POST.get('submit-add-habitat'):
        # add the new habitat
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Habitat(habitat,descr) values(%s,%s)',[request.POST.get('new-habitat').lower(),request.POST.get('habitat-descr').lower()])
        elif request.POST.get('submit-add-family'):
        # add family to database
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO Classification(family,ordr,clss,phylm,kingdm,descr) values(%s,%s,%s,%s,%s,%s)',[request.POST.get('new-family').lower(),request.POST.get('ordr').lower(),request.POST.get('clss').lower(),request.POST.get('phylm').lower(),request.POST.get('kingdm').lower(),request.POST.get('family-descr').lower()])
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
                cursor.execute('INSERT INTO Species(species,common_name,genus,family,region,habitat,status) values(%s,%s,%s,%s,%s,%s,%s)',[request.POST.get('species').lower(),request.POST.get('common_name'),request.POST.get('genus').lower(),request.POST.get('family'),regions,habitats,request.POST.get('add-status')])
            return HttpResponseRedirect('/species/'+request.POST.get('species').replace(" ","_")+'/')
    habitats = Habitat.objects.values_list('habitat',flat=True)
    families = Classification.objects.values_list('family',flat=True)
    regions = Region.objects.values_list('region',flat=True)
    statuses = Status.objects.order_by('level').values_list('status',flat=True)
    context = {
        'families':families,
        'habitats':habitats,
        'regions':regions,
        'statuses':statuses,
    }
    return render(request,'zoo/add_species.html',context)
