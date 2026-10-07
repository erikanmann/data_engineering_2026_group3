# Raw tables

## Elering dashboard API

### electricity_price_data

|Column|Data type|Key|Nullable|Description|
|--------|-------|--------|-------|--------|
|timestamp|BIGINT|PK|No|Unix timestamp|
|date_and_time|DATETIME||No|Observation time|
|NPS_Estonia|DECIMAL(8,2)||No|Nord Pool electricity price in Estonia|

### electricity_system_data

|Column|Data type|Key|Nullable|Description|
|--------|-------|--------|-------|--------|
|timestamp|BIGINT|PK|No|Unix timestamp|
|date_and_time|DATETIME||No|Observation time|
|production|DECIMAL(8,1)||No|Actual electricity production|
|consumption|DECIMAL(8,1)||No|Actual electricity consumption|
|wind_prod|DECIMAL(8,1)||No|Electricity produced by wind farms|
|solar_prod|DECIMAL(8,1)||No|Electricity produced by solar farms|
|solar_prod_forecast|DECIMAL(8,1)||Yes|Forecast of solar production|
|solar_prod_forecast2|DECIMAL(8,1)||Yes|Solar production forecast made by the system operator|
|frequency|DECIMAL(8,1)||Yes|System frequency|
|balance|DECIMAL(8,1)||Yes|Actual system balance|
|AC_balance|DECIMAL(8,1)||Yes|Actual alternating-current balance|
|planned_prod|DECIMAL(8,1)||Yes|Planned electricity production|
|planned_cons|DECIMAL(8,1)||Yes|Planned electricity consumption|
|wind_prod_forecast|DECIMAL(8,1)||Yes|Forecast of wind production|
|wind_prod_forecast2|DECIMAL(8,1)||Yes|Wind production forecast made by the system operator|
|planned_losses|DECIMAL(8,1)||Yes|Planned electricity losses|
|planned_balance|DECIMAL(8,1)||Yes|Planned system balance|
|Planned_AC_balance|DECIMAL(8,1)||Yes|Planned alternating-current balance|


## Estonian Environment Agency

### observations

|Column|Data type|Key|Nullable|Description|
|--------|-------|--------|-------|--------|
|ID|BIGINT|PK|No|Unique observation id|
|timestamp|BIGINT||No|Unique timestamp for observation|

### stations

|Column|Data type|Key|Nullable|Description|
|--------|-------|--------|-------|--------|
|ID|BIGINT|PK|No|Unique station id|
|name|VARCHAR(100)||No|Name of the station|
|wmocode|INT||Yes|Stations WMO code|
|longitude|NUMERIC||Yes|Station location coordinate|
|latitude|NUMERIC||Yes|Station location coordinate|

### station_observations

|Column|Data type|Key|Nullable|Description|
|--------|-------|--------|-------|--------|
|ID|BIGINT|PK|No|Unique station observation id|
|observation_id|BIGINT|FK|No|References observations.id|
|station_id|BIGINT|FK|No|References stations.id|
|phenomenon|VARCHAR(100)||Yes|Weather phenomenon occurring at the station|
|visibility|NUMERIC||Yes|Visibility (km)|
|precipitations|NUMERIC||Yes|Precipitation (mm) in the last hour|
|airpressure|NUMERIC||Yes|Air pressure (hPa)|
|relativehumidity|NUMERIC||Yes|Relative humidity (%)|
|airtemperature|NUMERIC||Yes|Air temperature (°C)|
|winddirection|NUMERIC||Yes|Wind direction (°)|
|windspeed|NUMERIC||Yes|Average wind speed (m/s)|
|windspeedmax|NUMERIC||Yes|Maximum wind speed or gusts (m/s)|
|waterlevel|NUMERIC||Yes|Water level of inland waters (cm) relative to Amsterdam zero|
|waterlevel_eh2000|NUMERIC||Yes|Sea water level (cm) relative to Amsterdam zero|
|watertemperature|NUMERIC||Yes|Water temperature (°C)|
|uvindex|NUMERIC||Yes|UV index|
|sunshineduration|NUMERIC||Yes|Daily sunshine duration (min) on the day of the query|
|globalradiation|NUMERIC||Yes|Total radiation, 1 hour average (W/m 2)|
