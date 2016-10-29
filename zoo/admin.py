# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models


class Biomes(models.Model):
    habitat = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Biomes'


class Exhibit(models.Model):
    zoo_name = models.ForeignKey('Zoo', models.DO_NOTHING, db_column='zoo_name')
    species = models.ForeignKey('Species', models.DO_NOTHING, db_column='species')

    class Meta:
        managed = False
        db_table = 'Exhibit'
        unique_together = (('zoo_name', 'species'),)


class Family(models.Model):
    family = models.CharField(primary_key=True, max_length=25)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Family'


class Species(models.Model):
    species = models.CharField(primary_key=True, max_length=100)
    common_name = models.CharField(max_length=200, blank=True, null=True)
    genus = models.CharField(max_length=50, blank=True, null=True)
    familia = models.CharField(max_length=50, blank=True, null=True)
    ordo = models.CharField(max_length=50, blank=True, null=True)
    classis = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    habitat = models.CharField(max_length=200, blank=True, null=True)
    lifespan = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Species'


class Zoo(models.Model):
    zoo_name = models.CharField(max_length=25)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    num_animals = models.IntegerField(blank=True, null=True)
    acres = models.IntegerField(blank=True, null=True)
    hour_open = models.CharField(max_length=5, blank=True, null=True)
    hour_close = models.CharField(max_length=5, blank=True, null=True)
    annual_visitors = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Zoo'
        unique_together = (('zoo_name', 'city'),)

