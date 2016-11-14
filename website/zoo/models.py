from __future__ import unicode_literals

from django.db import models


class Classification(models.Model):
    family = models.CharField(primary_key=True, max_length=50)
    ordr = models.CharField(max_length=50, blank=True, null=True)
    clss = models.CharField(max_length=50, blank=True, null=True)
    phylm = models.CharField(max_length=50, blank=True, null=True)
    kingdm = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Classification'


class Exhibit(models.Model):
    zoo_name = models.ForeignKey('Zoo', models.DO_NOTHING, db_column='zoo_name', primary_key=True)
    species = models.ForeignKey('Species', models.DO_NOTHING, db_column='species')

    class Meta:
        managed = False
        db_table = 'Exhibit'
        unique_together = (('zoo_name', 'species'),)


class Habitat(models.Model):
    habitat = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Habitat'


class Region(models.Model):
    region = models.CharField(primary_key=True, max_length=25)
    description = models.CharField(max_length=50, blank=True, null=True)

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


class Status(models.Model):
    status = models.CharField(primary_key=True, max_length=2)
    description = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Status'


class Zoo(models.Model):
    zoo_name = models.CharField(primary_key=True, max_length=100)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    num_animals = models.IntegerField(blank=True, null=True)
    acres = models.IntegerField(blank=True, null=True)
    hour_open = models.CharField(max_length=5, blank=True, null=True)
    hour_close = models.CharField(max_length=5, blank=True, null=True)
    annual_visitors = models.IntegerField(blank=True, null=True)
    website = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Zoo'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
