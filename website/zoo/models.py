from __future__ import unicode_literals

from django.db import models


class Classification(models.Model):
    family = models.CharField(primary_key=True, max_length=50)
    ordr = models.CharField(max_length=50, blank=True, null=True)
    clss = models.CharField(max_length=50, blank=True, null=True)
    phylm = models.CharField(max_length=50, blank=True, null=True)
    kingdm = models.CharField(max_length=50, blank=True, null=True)
    descr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Classification'


class Exhibit(models.Model):
    zoo_name = models.ForeignKey('Zoo', models.DO_NOTHING, db_column='zoo_name')
    species = models.ForeignKey('Species', models.DO_NOTHING, db_column='species')

    class Meta:
        managed = False
        db_table = 'Exhibit'
        unique_together = (('zoo_name', 'species'),)


class Habitat(models.Model):
    habitat = models.CharField(primary_key=True, max_length=20)
    descr = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Habitat'


class Hour(models.Model):
    hour = models.CharField(primary_key=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'Hour'


class Region(models.Model):
    region = models.CharField(primary_key=True, max_length=25)
    descr = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Region'


class Species(models.Model):
    species = models.CharField(primary_key=True, max_length=100)
    common_name = models.CharField(max_length=200, blank=True, null=True)
    genus = models.CharField(max_length=50, blank=True, null=True)
    family = models.ForeignKey(Classification, models.DO_NOTHING, db_column='family', blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    habitat = models.CharField(max_length=200, blank=True, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, db_column='status', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Species'


class State(models.Model):
    abbrv = models.CharField(primary_key=True, max_length=2)
    state = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'State'


class Status(models.Model):
    status = models.CharField(primary_key=True, max_length=2)
    descr = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Status'

class Zoo(models.Model):
    zoo_name = models.CharField(primary_key=True, max_length=100)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.ForeignKey(State, models.DO_NOTHING, db_column='state', blank=True, null=True)
    address = models.CharField(unique=True, max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    num_animals = models.IntegerField(blank=True, null=True)
    acres = models.IntegerField(blank=True, null=True)
    time_open = models.CharField(max_length=5, blank=True, null=True)
    time_close = models.CharField(max_length=5, blank=True, null=True)
    annual_visitors = models.IntegerField(blank=True, null=True)
    website = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Zoo'
