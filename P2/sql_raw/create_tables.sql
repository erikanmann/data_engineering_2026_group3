CREATE TABLE IF NOT EXISTS electricity_price_data (
    timestamp BIGINT PRIMARY KEY,
    date_and_time DATETIME NOT NULL,
    NPS_Estonia DECIMAL(8,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS electricity_system_data (
    timestamp BIGINT PRIMARY KEY,
    date_and_time DATETIME NOT NULL,
    production DECIMAL(8,1) NOT NULL,
    consumption DECIMAL(8,1) NOT NULL,
    wind_prod DECIMAL(8,1) NOT NULL,
    solar_prod DECIMAL(8,1) NOT NULL,
    solar_prod_forecast DECIMAL(8,1) ,
    solar_prod_forecast2 DECIMAL(8,1),
    frequency DECIMAL(8,1),
    balance DECIMAL(8,1),
    AC_balance DECIMAL(8,1),
    planned_prod DECIMAL(8,1),
    planned_cons DECIMAL(8,1),
    wind_prod_forecast DECIMAL(8,1),
    wind_prod_forecast2 DECIMAL(8,1),
    planned_losses DECIMAL(8,1),
    planned_balance DECIMAL(8,1),
    Planned_AC_balance DECIMAL(8,1)
);

CREATE TABLE IF NOT EXISTS observations (
    ID BIGINT PRIMARY KEY,
    timestamp BIGINT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS stations (
    ID BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    wmocode INT,
    longitude NUMERIC,
    latitude NUMERIC
);

CREATE TABLE IF NOT EXISTS station_observations (
    ID BIGINT PRIMARY KEY,
    observation_id BIGINT NOT NULL REFERENCES observations(ID),
    station_id BIGINT NOT NULL REFERENCES stations(ID),
    phenomenon VARCHAR(100),
    visibility NUMERIC,
    precipitations NUMERIC,
    airpressure NUMERIC,
    relativehumidity NUMERIC,
    airtemperature NUMERIC,
    winddirection NUMERIC,
    windspeed NUMERIC,
    windspeedmax NUMERIC,
    waterlevel NUMERIC,
    waterlevel_eh2000 NUMERIC,
    watertemperature NUMERIC,
    uvindex NUMERIC,
    sunshineduration NUMERIC,
    globalradiation NUMERIC
);