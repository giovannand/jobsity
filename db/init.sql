CREATE DATABASE jobsity;
\c jobsity;


GRANT ALL PRIVILEGES ON DATABASE jobsity TO postgres;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";



CREATE TABLE trips(
    id UUID DEFAULT uuid_generate_v4(),
    region varchar(150) NOT NULL ,
    origin_coord text NOT NULL,
    destination_coord text NOT NULL ,
    trip_datetime timestamp NOT NULL ,
    datasource varchar(150) NOT NULL  
);
