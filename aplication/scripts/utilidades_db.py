import asyncio
from pathlib import Path
import psycopg2
import environ
from consumoapi import square_bookings, square_customer, square_articulos

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

async def obtiene_lista_citas(inicio,fin):
    citas_square=square_bookings(inicio,fin)
    lista_citas=[]
    try:
        connection=conexion()
        print('Conexión exitosa a db')
        cursor = connection.cursor()
        #consultas_customer = []
        for cita in citas_square:
            cursor.execute('''SELECT "Version" 
                    FROM migracion_citasquare 
                    WHERE "IdRef"=%(id)s AND "Version"=%(version)s''',cita)
            if cursor.fetchone():
                continue
            datos_cita = {
            'IdRef' : cita['id'],
            'customer_id':cita['customer_id'],
            'Version': cita['version'],
            'Nota' : cita.get('seller_note','sin seller note'),
            'Servicios':cita['appointment_segments'][0]['service_variation_version'],
            'Fecha' : cita['start_at'][0:10],
            'Hora' : cita['start_at'][-9:-1]
                }
            lista_citas.append(datos_cita)

            #datos_cita.update(datos_customer)
            #print('procesando datos ...')
            #lista_citas.append(datos_cita)
        connection.close()       
        datos_customer = await asyncio.gather(*(square_customer(datos_cita['customer_id']) for datos_cita in lista_citas))
        for i, datos_cita in enumerate(lista_citas):
            datos_cita.update(datos_customer[i])
    except Exception as ex:
        raise
        #print(ex)
    return lista_citas

def guarda_citas(inicio,fin):
    lista = asyncio.run(obtiene_lista_citas(inicio,fin))#    
    if len(lista)>0:
        try:
            connection=conexion()
            print('Conexión exitosa a db')
            cursor = connection.cursor()
            for item in lista:
                cursor.execute('''INSERT INTO 
                    migracion_citasquare(
                    "IdRef",
                    "Nombre",
                    "Correo",
                    "Telefono",
                    "Fecha",
                    "Hora",
                    "Nota",
                    "Servicios",
                    "Version",
                    "Direccion")
                    VALUES (
                    %(IdRef)s,
                    %(Nombre)s,
                    %(Correo)s,
                    %(Telefono)s,
                    %(Fecha)s,
                    %(Hora)s,
                    %(Nota)s,
                    %(Servicios)s,
                    %(Version)s,
                    %(Direccion)s)''',item)
                connection.commit() 
                print('Cargando dato ...')
            connection.close()
            print('Guardado de datos exitoso')
            print('Conexion cerrada a db')
        except Exception as ex:
            print(ex)
    else:
        print('No hay datos nuevos')

def guarda_articulos():
    articulos = square_articulos()['objects']
    try:
        connection=conexion()
        print('Conexión exitosa a db')
        cursor = connection.cursor()
        for articulo in articulos:
            item_data = articulo.get('item_data')
            if item_data:
                data_articulo={'IdArticuloSquare': articulo['id'],
                        'Descripcion': item_data['name']}
                cursor.execute('''INSERT INTO 
                        venta_articulo(
                        "IdArticuloSquare",
                        "Descripcion") 
                        VALUES (
                        %(IdArticuloSquare)s, 
                        %(Descripcion)s) 
                        ON CONFLICT (
                        "IdArticuloSquare") 
                        DO UPDATE SET 
                        "Descripcion"  = venta_articulo."Descripcion"
                        ''',data_articulo)
                connection.commit()
                print('Articulo guardado ...')
                variantes = item_data['variations']
                for variante in variantes:
                    print('--------------------------------------')
                    v_data = variante['item_variation_data']
                    data_variante ={
                            'IdArticuloSquare':data_articulo['IdArticuloSquare'],
                            'IdVarianteSquare': v_data['item_id'],
                            'Descripcion':v_data['name'],
                            'PrecioUnitario': v_data['price_money']['amount'],
                            'IdMoneda': v_data['price_money']['currency']
                            }
                    cursor.execute('''INSERT INTO 
                    venta_variante(
                    "IdVarianteSquare",
                    "Descripcion",
                    "IdArticulo_id",
                    "PrecioUnitario",
                    "IdMoneda") 
                    VALUES (
                    %(IdVarianteSquare)s,
                    %(Descripcion)s,
                    %(IdArticuloSquare)s,
                    %(PrecioUnitario)s,
                    %(IdMoneda)s)
                    ON CONFLICT (
                    "IdVarianteSquare") 
                    DO UPDATE SET 
                    "Descripcion"  = venta_variante."Descripcion", 
                    "IdArticulo_id" = venta_variante."IdArticulo_id",
                    "PrecioUnitario" = venta_variante."PrecioUnitario", 
                    "IdMoneda"=venta_variante."IdMoneda" ''',data_variante)
                    connection.commit()
                    print('Variante guardada')
                print('======================================')
        connection.close()
    except Exception as ex:
        print(ex)

#guarda_articulos()
guarda_citas("2022-07-27T14:00:00Z","2022-07-27T17:59:00Z")
#obtiene_lista_citas("2022-07-27T14:00:00Z","2022-07-27T17:59:00Z")

