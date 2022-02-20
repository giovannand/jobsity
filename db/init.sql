CREATE DATABASE jobsity;
\c jobsity;


GRANT ALL PRIVILEGES ON DATABASE jobsity TO postgres;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;


CREATE TABLE trips(
    id UUID DEFAULT uuid_generate_v4(),
    region varchar(150) NOT NULL ,
    origin_coord geometry NOT NULL,
    destination_coord geometry NOT NULL ,
    trip_datetime timestamp NOT NULL ,
    datasource varchar(150) NOT NULL  
);
