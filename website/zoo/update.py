# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from .models import Zoo,Species

def save_zoo(request,zoo_id):
    zoo = Zoo.objects.get(id=zoo_id)
    zoo.zoo_name = request.POST.get("zoo_name")
    zoo.city = request.POST.get("city")
    zoo.state = request.POST.get("state")
    zoo.address = request.POST.get("address")
    zoo.latitude = request.POST.get("latitude")
    zoo.longitude = request.POST.get("longitude")
    zoo.num_animals = request.POST.get("num_animals")
    zoo.acres = request.POST.get("acres")
    zoo.hour_open = request.POST.get("hour_open")
    zoo.hour_close = request.POST.get("hour_close")
    zoo.annual_visitors = request.POST.get("annual_visitors")
    zoo.website = request.POST.get("website")
    zoo.save()
    
def save_species(request,species_id):
    species = Species.objects.get(id=species_id)
    species.species = request.POST.get("species")
    species.common_name = request.POST.get("common_name")
    species.genus = request.POST.get("genus")
    species.familia = request.POST.get("familia")
    species.ordo = request.POST.get("ordo")
    species.classis = request.POST.get("classis")
    species.region = request.POST.get("region")
    species.habitat = request.POST.get("habitat")
    species.lifespan = request.POST.get("lifespan")
    species.status = request.POST.get("status")
    species.save()