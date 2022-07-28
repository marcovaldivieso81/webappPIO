from pathlib import Path
import environ
import psycopg2

from consumoapi import obtiene_lista_citas 

BASE_DIR = Path(__file__).resolve().parent.parent
env=environ.Env()
environ.Env.read_env(f"{BASE_DIR}/aplication/.env")

lista = obtiene_lista_citas("2022-07-27T14:00:00Z","2022-07-27T23:59:00Z")
try:
    connection = psycopg2.connect(
            host = env.str('DATA_BASE_HOST'),
            user = env.str('DATA_BASE_USER'), 
            password = env.str('DATA_BASE_PASSWORD'),
            database = env.str('DATA_BASE_NAME')
            )
    print('Conexión exitosa a db')
    cursor = connection.cursor()
    for item in lista:
        cursor.execute(f"INSERT INTO migracion_citasquare(\"IdRef\",\"Nombre\", \"Correo\", \"Telefono\", \"Fecha\", \"Hora\", \"Nota\", \"Servicios\") VALUES ('{item['IdRef']}', '{item['Nombre']}','{item['Correo']}', '{item['Telefono']}', '{item['Fecha']}', '{item['Hora']}', '{item['Nota']}', 'bla bla')")
        connection.commit() 
        print('Cargando dato ...')
    #row = cursor.fetchone()
    #print(listacitas)
    
except Exception as ex:
    print(ex)

print('Guardado de datos exitoso')



#print(settings.BASE_DIR)
