from datetime import datetime,timedelta, date
from .conexion_db import conexion 

connection=conexion()
data ={'Fecha':'2022-11-05'}
cursor = connection.cursor()
cursor.execute('''SELECT "IdPedidoSquare","Fecha","Hora" FROM venta_pedido WHERE "Fecha">%(Fecha)s''',data)

lista =[]
for elemento in cursor.fetchall():
    FechaHora=datetime.combine(elemento[1],elemento[2])-timedelta(hours=1)
    dic={'Id':elemento[0],
        'Hora': FechaHora.time(),
        'Fecha': FechaHora.date()}
    lista.append(dic)
    cursor.execute('''UPDATE venta_pedido
                    SET "Hora"=%(Hora)s,"Fecha"=%(Fecha)s
                    WHERE "IdPedidoSquare"=%(Id)s''',dic)
    connection.commit()









