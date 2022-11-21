import psycopg2
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env=environ.Env()
environ.Env.read_env(f"{BASE_DIR}/aplication/.env")

def conexion():
    connection = psycopg2.connect(
            host = env.str('DATA_BASE_HOST'),
            user = env.str('DATA_BASE_USER'), 
            password = env.str('DATA_BASE_PASSWORD'),
            database = env.str('DATA_BASE_NAME')
            )
    return connection

def conexion2():
    connection = psycopg2.connect(
            host = env.str('DATA_BASE_HOST'),
            user = env.str('DATA_BASE_USER'), 
            password = env.str('DATA_BASE_PASSWORD'),
            database = env.str('DB_NAME_OLD')
            )
    return connection


