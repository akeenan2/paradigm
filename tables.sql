drop table Exhibit;
drop table Species;
drop table Zoo;
drop table Region;
drop table Status;
drop table Classification;
drop table Habitat;

create table Habitat (
    habitat varchar(20) primary key,
    description varchar(200)
);

create table Classification (
    family varchar(50) primary key,
    ordr varchar(50),
    clss varchar(50),
    phylm varchar(50),
    kingdm varchar(50),
    description varchar(200)
);

create table Status (
    status char(2) primary key,
    description varchar(25)
);

create table Region (
    region varchar(25) primary key,
    description varchar(50)
);

create table Zoo (
    zoo_name varchar(100) primary key,
    city varchar(50),
    state char(2),
    address varchar(100),
    latitude float(10,6),
    longitude float(10,6),
    num_animals int,
    acres int,
    hour_open char(5),
    hour_close char(5),
    annual_visitors int,
    website varchar(100) unique
);

create table Species (
    species varchar(100) primary key,
    common_name varchar(200),
    genus varchar(50),
    family varchar(50),
    region varchar(100),
    habitat varchar(200),
    status char(2),
    foreign key (status) references Status(status),
    foreign key (family) references Classification(family)
);

create table Exhibit (
    zoo_name varchar(100),
    species varchar(100),
    primary key (zoo_name,species),
    foreign key (zoo_name) references Zoo(zoo_name),
    foreign key (species) references Species(species)
);

load data local infile 'habitat.csv' into table Habitat
    fields terminated by ','
    lines terminated by '\n'
    (habitat,description);

load data local infile 'classification.csv' into table Classification
    fields terminated by ','
    lines terminated by '\n'
    (family,ordr,clss,phylm,kingdm,description);

load data local infile 'status.csv' into table Status
    fields terminated by ','
    lines terminated by '\n'
    (status,description);

load data local infile 'region.csv' into table Region
    fields terminated by ','
    lines terminated by '\n'
    (region,description);

load data local infile 'zoo.csv' into table Zoo
    fields terminated by ','
    lines terminated by '\n'
    (zoo_name,city,state,address,latitude,longitude,num_animals,acres,hour_open,hour_close,annual_visitors,website);

load data local infile 'species.csv' into table Species
    fields terminated by ','
    lines terminated by '\n'
    (species,common_name,genus,family,region,habitat,status);

load data local infile 'exhibit.csv' into table Exhibit
    fields terminated by ','
    lines terminated by '\n'
    (zoo_name,species);

command to auto-create models:
python manage.py inspectdb > models.py
