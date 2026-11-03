from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
import os
import pendulum
import requests
from datetime import timedelta

EST_WEATHER_API = "https://www.ilmateenistus.ee/ilma_andmed/xml/observations.php"
CONECTION_ID = "project_db"

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
}

def fetch_weather_data():
    pass



def store_weather_data(**context):
    pass
