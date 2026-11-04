from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
import os
import pendulum
import requests
from datetime import timedelta
import xml.etree.ElementTree as ET
import logging



EST_WEATHER_API = "https://www.ilmateenistus.ee/ilma_andmed/xml/observations.php"
CONECTION_ID = "project_db"

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
}

def fetch_weather_data():
    response = requests.get(EST_WEATHER_API, timeout=10)
    response.raise_for_status()
    data = response.text
    return data



def store_weather_data(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids='fetch_weather_data')

    pg = PostgresHook(postgres_conn_id=CONECTION_ID)
    root = ET.fromstring(data)
    timestamp = int(root.attrib['timestamp'])
    observation_id = pg.get_first(
        """
        INSERT INTO observations (timestamp)
        VALUES (%s)
        ON CONFLICT (timestamp)
        DO UPDATE SET timestamp = EXCLUDED.timestamp
        RETURNING id
        """,
        parameters=(timestamp,)
    )[0]


    stations = root.findall('station')
    for station in stations:
        name = station.findtext('name')
        name = name if name else None

        wmocode = station.findtext('wmocode')
        wmocode = int(wmocode) if wmocode else None

        longitude = station.findtext('longitude')
        longitude = float(longitude) if longitude else None

        latitude = station.findtext('latitude')
        latitude = float(latitude) if latitude else None

        phenomenon = station.findtext('phenomenon') 
        phenomenon = phenomenon if phenomenon else None

        visibility = station.findtext('visibility')
        visibility = float(visibility) if visibility else None

        precipitations = station.findtext('precipitations')
        precipitations = float(precipitations) if precipitations else None

        airpressure = station.findtext('airpressure')
        airpressure = float(airpressure) if airpressure else None

        relativehumidity = station.findtext('relativehumidity')
        relativehumidity = float(relativehumidity) if relativehumidity else None

        airtemperature = station.findtext('airtemperature')
        airtemperature = float(airtemperature) if airtemperature else None

        winddirection = station.findtext('winddirection')
        winddirection = float(winddirection) if winddirection else None

        windspeed = station.findtext('windspeed')
        windspeed = float(windspeed) if windspeed else None

        windspeedmax = station.findtext('windspeedmax')
        windspeedmax = float(windspeedmax) if windspeedmax else None

        waterlevel = station.findtext('waterlevel')
        waterlevel = float(waterlevel) if waterlevel else None

        waterlevel_eh2000 = station.findtext('waterlevel_eh2000')
        waterlevel_eh2000 = float(waterlevel_eh2000) if waterlevel_eh2000 else None

        watertemperature = station.findtext('watertemperature')
        watertemperature = float(watertemperature) if watertemperature else None

        uvindex = station.findtext('uvindex')
        uvindex = float(uvindex) if uvindex else None

        sunshineduration = station.findtext('sunshineduration')
        sunshineduration = float(sunshineduration) if sunshineduration else None

        globalradiation = station.findtext('globalradiation')
        globalradiation = float(globalradiation) if globalradiation else None


        station_id = pg.get_first(
            """
            INSERT INTO stations (name, wmocode, longitude, latitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name)
            DO UPDATE SET
                wmocode = EXCLUDED.wmocode,
                longitude = EXCLUDED.longitude,
                latitude = EXCLUDED.latitude
            RETURNING id
            """,
            parameters=(name, wmocode, longitude, latitude)
        )[0]
        pg.run(
            "INSERT INTO station_observations (observation_id, station_id, phenomenon, visibility, precipitations, airpressure, relativehumidity, airtemperature, winddirection, windspeed, windspeedmax, waterlevel, waterlevel_eh2000, watertemperature, uvindex, sunshineduration, globalradiation)" \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (observation_id, station_id) DO NOTHING",
            parameters=(observation_id, station_id, phenomenon, visibility, precipitations, airpressure, relativehumidity, 
                        airtemperature, winddirection, windspeed, windspeedmax, waterlevel, 
                        waterlevel_eh2000, watertemperature, uvindex, sunshineduration, 
                        globalradiation)
        )
    print("Weather data stored successfully.")



with DAG(
    dag_id="load_raw_data",
    description="Load raw data from Elering and Estonian Weather Service API and store it in PostgreSQL",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="0 * * * *",
    catchup=False,
    max_active_runs=1,
    default_args=default_args,
    tags=["api", "data_ingestion"],
) as dag:
    t_fetch = PythonOperator(
        task_id="fetch_weather_data",
        python_callable=fetch_weather_data,
        retries=3,
    )

    t_store = PythonOperator(
        task_id="store_weather_data",
        python_callable=store_weather_data,
    )

    t_fetch >> t_store