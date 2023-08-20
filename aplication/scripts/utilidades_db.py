import asyncio
from datetime import datetime
from .consumoapi import square_bookings, square_customer, square_articulos
from .conexion_db import conexion 

async def obtiene_lista_citas(inicio,fin):
    citas_square=square_bookings(inicio,fin)
    lista_citas=[]
    try:
        connection=conexion()
        #print('Conexión exitosa a db')
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        for cita in citas_square:
            cursor.execute('''SELECT "Version" 
                    FROM migracion_citasquare 
                    WHERE "IdRef"=%(id)s AND "Version"=%(version)s''',cita)
            cursor2.execute('''SELECT "IdPedidoSquare"
                            FROM venta_pedido
                            WHERE "IdPedidoSquare"=%(id)s''',cita)
            #print(cursor2.fetchone())
            #dada = cursor.fetchone()
            #print(dada,cita['id'])
            #print(cursor.fetchone())
            #print('-----------------------')
            if cursor.fetchone() and cursor2.fetchone():
                continue
            #print(cursor.fetchone())
            #print(cita['id'])
            #print('-------')
            datos_cita = {
            'IdRef' : cita['id'],
            'customer_id':cita['customer_id'],
            'Version': cita['version'],
            'Nota' : cita.get('seller_note','sin seller note'),
            'Servicios':cita['appointment_segments'][0]['service_variation_version'],
            'Fecha' : cita['start_at'][0:10],
            'Hora' : cita['start_at'][-9:-1],
            'Observacion':'',
            'Estado': 'New',
            'Cancelado':False,
            'Confirmed_by_customer':False,
            'In_Production':False
            }
            lista_citas.append(datos_cita)
        connection.close()       
        datos_customer = await asyncio.gather(*(square_customer(datos_cita['customer_id']) for datos_cita in lista_citas))
        citas_exitosas = []
        for i, datos_cita in enumerate(lista_citas):
            if datos_customer[i][0]:
                datos_cita.update(datos_customer[i][1])
                citas_exitosas.append(datos_cita)
            else:
                ## guardo en base datos
                #print('-----------')
                #print(f"Cita_id = {datos_cita['IdRef']} Customer_id = {datos_cita['customer_id']}")
                #print('----------')
                pass
    except Exception as ex:
        raise
        #print(ex)
    return citas_exitosas

def guarda_citas(inicio,fin,usuario='system'):
    lista = asyncio.run(obtiene_lista_citas(inicio,fin))#    
    if len(lista)>0:
        try:
            ## iteración para eliminar valores de servicios no permitidos
            valores_permitidos = [1658428294592, 1650382159084]
            ## seria importante poder obtener los valores permitidos haciendo una consulta a bd
            #lista = nueva_lista = [diccionario for diccionario in lista if diccionario['Servicios'] in valores_permitidos]

            connection=conexion()
            #print('Conexión exitosa a db')
            cursor = connection.cursor()
            cursor2 = connection.cursor()
            cursorsinc = connection.cursor()
            texto="PEDIDOS:\n\n"
            for item in lista:
                texto += f"{item['IdRef']} - {item['Nombre']}\n"
                #print(item['Nombre'])
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
                    "Observacion"
                    )
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
                    %(Observacion)s
                    )''',item)
                #print('Cargando dato ...')
                ## ACA SE ACTUALIZA LOS PEDIDOS
                if item['Servicios'] not in valores_permitidos:
                    continue
                cursor2.execute('''INSERT INTO 
                        venta_pedido(
                        "IdPedidoSquare",
                        "NombreCliente",
                        "Telefono",
                        "Servicio_id",
                        "Notas",
                        "Observacion",
                        "Fecha",
                        "Hora",
                        "Estado_id",
                        "Cancelado",
                        "Confirmed_by_customer",
                        "In_Production"
                        ) 
                        VALUES (
                        %(IdRef)s, 
                        %(Nombre)s,
                        %(Telefono)s,
                        %(Servicios)s,
                        %(Nota)s,
                        %(Observacion)s,
                        %(Fecha)s,
                        %(Hora)s,
                        %(Estado)s,
                        %(Cancelado)s,
                        %(Confirmed_by_customer)s,
                        %(In_Production)s
                        ) 
                        ON CONFLICT (
                        "IdPedidoSquare") 
                        DO UPDATE SET 
                        "Notas"  = %(Nota)s
                        ''',item)
                connection.commit()
            datos_sinc={
                    'Fecha':datetime.now(),
                    'Texto':texto,
                    'Usuario':usuario,
                    'Rango':inicio+' - '+fin
                    }
            #print(datos_sinc)
            #print('----')
            cursorsinc.execute('''INSERT INTO 
                    migracion_sincronizacion(
                    "FechaCreacion",
                    "UsuarioCreacion",
                    "Observacion",
                    "Rango"
                    )
                    VALUES (
                    %(Fecha)s,
                    %(Usuario)s,
                    %(Texto)s,
                    %(Rango)s
                    )''',datos_sinc)

            connection.commit()
                #################################
            connection.close()
            #print('Guardado de datos exitoso')
            #print('Conexion cerrada a db')
        except Exception as ex:
            #print(ex)
            raise
    else:
        print('No hay datos nuevos')

def guarda_articulos():
    consulta = square_articulos()
    articulos = consulta['objects']
    cursor = consulta['cursor'] 
    while cursor:
        consulta = square_articulos(cursor)
        articulos += consulta['objects']
        cursor = consulta.get('cursor',False)
    try:
        connection=conexion()
        #print('Conexión exitosa a db')
        cursor = connection.cursor()
        for articulo in articulos:
            item_data = articulo.get('item_data')
            if item_data:
                desc=item_data['name']
                if desc.isdigit():
                    pass
                else:
                    #print(articulo['is_deleted'])
                    #print('-------------')
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
                #print('Articulo guardado ...')
                    variantes = item_data['variations']
                    for variante in variantes:
                 #   print('--------------------------------------')
                        v_data = variante['item_variation_data']
                    #print('---------')
                        #if(variante['is_deleted']):
                            #print(variante['is_deleted'])
                            #print('---------')
                        data_variante ={
                            'IdArticuloSquare':data_articulo['IdArticuloSquare'],
                            'IdVarianteSquare': variante['id'],
                            'Descripcion':v_data['name'],
                            'PrecioUnitario': v_data['price_money']['amount'],
                            'IdMoneda': v_data['price_money']['currency'],
                            'Activo':variante['is_deleted']
                            }
                        cursor.execute('''INSERT INTO 
                            venta_variante(
                            "IdVarianteSquare",
                            "Descripcion",
                            "IdArticulo_id",
                            "PrecioUnitario",
                            "IdMoneda",
                            "Activo") 
                            VALUES (
                            %(IdVarianteSquare)s,
                            %(Descripcion)s,
                            %(IdArticuloSquare)s,
                            %(PrecioUnitario)s,
                            %(IdMoneda)s,
                            %(Activo)s)
                            ON CONFLICT (
                            "IdVarianteSquare") 
                            DO UPDATE SET 
                            "Descripcion"  = venta_variante."Descripcion", 
                            "IdArticulo_id" = venta_variante."IdArticulo_id",
                            "PrecioUnitario" = venta_variante."PrecioUnitario", 
                            "IdMoneda"=venta_variante."IdMoneda",
                            "Activo"=venta_variante."Activo" ''',data_variante)
                        connection.commit()
                            #print('Variante guardada')
                            #print('======================================')
        connection.close()
    except Exception as ex:
        print(ex)



#guarda_articulos()
#guarda_citas("2022-08-08T00:00:00Z","2022-08-10T23:59:00Z")
#obtiene_lista_citas("2022-07-27T14:00:00Z","2022-07-27T17:59:00Z")

