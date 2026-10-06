# Raw tabels

## Elering dashboard API

### electricity_price_data

| Column | Data type | Key | Nullable | Description |
| -------- | ------- | -------- | ------- | -------- |
|timestamp | BIGINT | PK |  | Unix timestamp |
| date_and_time |  DATETIME |  |  | Observation time |
| NPS_Estonia |  DECIMAL(8,2) |  |  | Nord Pool electricity price in Estonia |

### electricity_system_data

| Column | Data type | Key | Nullable | Description |
| -------- | ------- | -------- | ------- | -------- |
| timestamp |BIGINT | PK |   |Unix timestamp |
| date_and_time | DATETIME |   |   | Observation time |
| production | DECIMAL(8,1) |   |   | Actual electricity production |
| consumption | DECIMAL(8,1) |   |   | Actual electricity consumption |
| wind_prod | DECIMAL(8,1)|   |   | Electricity produced by wind farms |
| solar_prod | DECIMAL(8,1)|   |   | Electricity produced by solar farms|
| solar_prod_forecast | DECIMAL(8,1)|   |Yes|Forecast of solar production|
| solar_prod_forecast2 | DECIMAL(8,1)|   |Yes|Solar production forecast made by the system operator|
| frequency | DECIMAL(8,1) |  |Yes|System frequency|
| balance | DECIMAL(8,1) | | Yes|Actual system balance|
| AC_balance | DECIMAL(8,1) |  |Yes|Actual alternating-current balance|
| planned_prod | DECIMAL(8,1) |  | Yes|Planned electricity production|
| planned_cons | DECIMAL(8,1) |   |Yes|Planned electricity consumption|
| wind_prod_forecast | DECIMAL(8,1) |   |Yes|Forecast of wind production|
| wind_prod_forecast2 | DECIMAL(8,1) ||Yes|Wind production forecast made by the system operator|
| planned_losses | DECIMAL(8,1) ||Yes|Planned electricity losses|
| planned_balance | DECIMAL(8,1) ||Yes|Planned system balance|
| Planned_AC_balance | DECIMAL(8,1) ||Yes|Planned alternating-current balance|||


## Estonian Environment Agency

### observations

| Column | Data type | Key | Nullable | Description |
| -------- | ------- | -------- | ------- | -------- |
|ID|BIGINT|PK|No|Unique observation id|
|timestamp|BIGINT||No|Unique timestamp for observation|