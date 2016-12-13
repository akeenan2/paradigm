drop table Exhibit;
drop table Species;
drop table Zoo;
drop table Region;
drop table Status;
drop table Classification;
drop table Habitat;
drop table State;

create table State (
    abbrv char(2) primary key,
    state varchar(20)
);

create table Habitat (
    habitat varchar(20) primary key,
    descr varchar(200)
);

create table Classification (
    family varchar(50) primary key,
    ordr varchar(50),
    clss varchar(50),
    phylm varchar(50),
    kingdm varchar(50),
    descr varchar(200)
);

create table Status (
    level int(10) unique,
    status char(2) primary key,
    descr varchar(25)
);

create table Region (
    region varchar(20) primary key,
    descr varchar(200)
);

create table Zoo (
    zoo_name varchar(100) primary key,
    city varchar(50),
    state char(2),
    address varchar(100) unique,
    num_animals int(10),
    acres int(10),
    time_open char(5),
    time_close char(5),
    annual_visitors int(10),
    website varchar(100) unique,
    foreign key (state) references State(abbrv)
);

create table Species (
    species varchar(100) primary key,
    common_name varchar(200),
    genus varchar(50),
    family varchar(50),
    region varchar(200),
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

load data local infile 'state.csv' into table State
    fields terminated by ','
    lines terminated by '\n'
    (abbrv,state);

load data local infile 'habitat.csv' into table Habitat
    fields terminated by ','
    lines terminated by '\n'
    (habitat,descr);

load data local infile 'classification.csv' into table Classification
    fields terminated by ','
    lines terminated by '\n'
    (family,ordr,clss,phylm,kingdm,descr);

load data local infile 'status.csv' into table Status
    fields terminated by ','
    lines terminated by '\n'
    (level,status,descr);

load data local infile 'region.csv' into table Region
    fields terminated by ','
    lines terminated by '\n'
    (region,descr);

load data local infile 'zoo.csv' into table Zoo
    fields terminated by ','
    lines terminated by '\n'
    (zoo_name,city,state,address,num_animals,acres,time_open,time_close,annual_visitors,website);

load data local infile 'species.csv' into table Species
    fields terminated by ','
    lines terminated by '\n'
    (species,common_name,genus,family,region,habitat,status);

load data local infile 'exhibit.csv' into table Exhibit
    fields terminated by ','
    lines terminated by '\n'
    (zoo_name,species);
