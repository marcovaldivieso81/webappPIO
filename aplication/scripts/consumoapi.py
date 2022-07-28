import requests
import json

URL_SQUARE = "https://connect.squareup.com/v2/"
LOCATION_ID = '1ABD34R8HF94M'
TOKEN = 'Bearer EAAAEF3-kndT3YiRN2_JTFytc6Q-6c8i-4SymP1y3LsqZAmqKPHKZXlLbpXEgK-o' 

def square_bookings(inicio,fin):
    args = {'limit':100,
            'location_id': LOCATION_ID,
            'start_at_min': inicio, # "2022-07-21T14:00:00Z",
            'start_at_max': fin, #"2022-07-21T23:59:00Z"
            }
    headers = {'Authorization': TOKEN}
    print('Inicio consumo de api')
    response = requests.get(URL_SQUARE+'bookings',params=args,headers=headers)
    print('Consumo de api realizado')
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        return response_decode['bookings']

def square_customer(customer_id):
    headers = {'Authorization': TOKEN}
    response = requests.get(URL_SQUARE+'customers'+'/'+customer_id,headers=headers)
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        return response_decode

def square_articulos():
    headers = {'Authorization': TOKEN}
    args = {'type':'ITEM'}
    response = requests.get(URL_SQUARE+'catalog/list',params = args,headers = headers)
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        return response_decode

def obtiene_lista_citas(inicio,fin):
    citas_square=square_bookings(inicio,fin)
    lista_citas=[]
    for cita in citas_square:
        #print(cita['customer_id'])
        customer_square = square_customer(cita['customer_id'])['customer']
        if 'address' in customer_square:
            linea1 = customer_square['address'].get('address_line_1','')
            linea2 = customer_square['address'].get('address_line_2','')
            locality = customer_square['address'].get('locality','')
            distrito = customer_square['address'].get('administrative_district_level_1','')
            code =  customer_square['address'].get('postal_code')
            country =  customer_square['address'].get('country')
            direccion = f'{linea1} {linea2} {locality} {distrito} {code} {country}'
        else:
            direccion ='sin direccion'
        nombre = customer_square.get('given_name', '')
        apellido = customer_square.get('family_name','')
        diccionario_cita = {
            'IdRef' : cita['id'],
            'Nota' : cita.get('seller_note','sin seller note'),
            'Nombre' : f'{nombre} {apellido}',
            'Telefono' : customer_square.get('phone_number','no number'),
            'Correo' : customer_square.get('email_address','no email'),
            'Direccion': direccion,
            'Fecha' : cita['created_at'][0:10],
            'Hora' : cita['created_at'][-9:-1]
            }
        lista_citas.append(diccionario_cita)
        print('procesando datos ...')
        print(diccionario_cita)
        print('-------------------------------------')
    return lista_citas

print(obtiene_lista_citas("2022-07-26T14:00:00Z","2022-07-26T23:59:00Z"))
