create table Biome (
    habitat varchar(20) primary key,
    description varchar(200)
);

create table Family (
    family varchar(25) primary key,
    description varchar(200)
);

create table Zoo (
    id int(11) primary key auto_increment,
    zoo_name varchar(25) unique,
    city varchar(200),
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
    familia varchar(50),
    ordo varchar(50),
    classis varchar(50),
    region varchar(100),
    habitat varchar(200),
    lifespan int(11),
    status char(2)
);

create table Exhibit (
    zoo_name varchar(100),
    species varchar(100),
    primary key (zoo_name,species),
    foreign key (zoo_name) references Zoo(zoo_name),
    foreign key (species) references Species(species)
);

load data local infile 'biome.csv' into table Biome
    fields terminated by ','
    lines terminated by '\n'
    (habitat,description);

load data local infile 'family.csv' into table Family
    fields terminated by ','
    lines terminated by '\n'
    (family,description);

load data local infile 'zoo.csv' into table Zoo
    fields terminated by ','
    lines terminated by '\n'
    (zoo_name,city,state,address,latitude,longitude,num_animals,acres,hour_open,hour_close,annual_visitors,website);

load data local infile 'species.csv' into table Species
    fields terminated by ','
    lines terminated by '\n'
    (species,common_name,genus,familia,ordo,classis,region,habitat,lifespan,status);

load data local infile 'exhibit.csv' into table Exhibit
    fields terminated by ','
    lines terminated by '\n'
    (zoo_name,species);

biomes(habitat,description)
exhibit(zoo_name,species)
family(family,description)
species(habitat,description)
zoo(zoo_name,city,state,address,latitude,longitude,num_animals,acres,hour_open,hour_close,annual_visitors,website)

command to auto-create models:
python manage.py inspectdb > models.py
