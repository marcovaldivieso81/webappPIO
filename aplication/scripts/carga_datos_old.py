#from datetime import datetime,timedelta, date
from .conexion_db import conexion, conexion2 

connection=conexion2()
date ={'Fecha':'2022-11-12'}
cursor = connection.cursor()
cursor.execute('''SELECT "IdPedidoSquare", "NombreCliente", "Telefono", "Direccion", "Fecha", "Hora", "Notas", "Cancelado", "Observacion", "Estado_id", "Servicio_id", "Confirmed_by_customer","In_Production" FROM venta_pedido WHERE "Fecha" < DATE('2022-11-12')''')
respuesta=cursor.fetchall()
print(respuesta)
print("Base datos antigua importada\nPreparando carga ...")
connection.close()

connection2=conexion()
cursor2 = connection2.cursor()
for fila in respuesta:
    cursor2.execute('INSERT INTO venta_pedido ("IdPedidoSquare", "NombreCliente", "Telefono", "Direccion", "Fecha", "Hora", "Notas", "Cancelado", "Observacion", "Estado_id", "Servicio_id", "Confirmed_by_customer","In_Production")  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',fila)
    connection2.commit()
connection2.close()
#print('Datos antiguos importados')




#cursor.execute('''UPDATE venta_pedido
#                    SET "Hora"=%(Hora)s,"Fecha"=%(Fecha)s
#                    WHERE "IdPedidoSquare"=%(Id)s''',dic)
#connection.commit()





