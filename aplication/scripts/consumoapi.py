import requests
import json
from pathlib import Path
import environ
import aiohttp

BASE_DIR = Path(__file__).resolve().parent.parent
env=environ.Env()
environ.Env.read_env(f"{BASE_DIR}/aplication/.env")

URL_SQUARE = env.str('URL_SQUARE')
LOCATION_ID_SQUARE = env.str('LOCATION_ID_SQUARE')
TOKEN_SQUARE = 'Bearer '+env.str('TOKEN_SQUARE')

def square_bookings(inicio,fin):
    args = {'limit':100,
            'location_id': LOCATION_ID_SQUARE,
            'start_at_min': inicio, # "2022-07-21T14:00:00Z",
            'start_at_max': fin, #"2022-07-21T23:59:00Z"
            }
    headers = {'Authorization': TOKEN_SQUARE}
    print('Inicio consumo de api')
    response = requests.get(URL_SQUARE+'bookings',params=args,headers=headers)
    print('Consumo de api realizado')
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        return response_decode['bookings']

async def square_customer(customer_id):
    headers = {'Authorization': TOKEN_SQUARE}
    #response = requests.get(URL_SQUARE+'customers'+'/'+customer_id,headers=headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_SQUARE+'customers'+'/'+customer_id,headers=headers) as response:
            if response.status == 200:
                content=await response.text()
                customer = json.loads(content)['customer']
                if 'address' in customer:
                    linea1 = customer['address'].get('address_line_1','')
                    linea2 = customer['address'].get('address_line_2','')
                    locality = customer['address'].get('locality','')
                    distrito = customer['address'].get('administrative_district_level_1','')
                    code =  customer['address'].get('postal_code')
                    country =  customer['address'].get('country')
                    direccion = f'{linea1} {linea2} {locality} {distrito} {code} {country}'
                else:
                    direccion ='sin direccion'
                datos_customer = {
                        'Nombre': customer.get('given_name', '') +  customer.get('family_name',''),
                        'Telefono' : customer.get('phone_number','no number'),
                        'Correo' : customer.get('email_address','no email'),
                        'Direccion':direccion
                        }
                return datos_customer


        
def square_articulos():
    headers = {'Authorization': TOKEN_SQUARE}
    args = {'type':'ITEM'}
    response = requests.get(URL_SQUARE+'catalog/list',params = args,headers = headers)
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        return response_decode


#print(obtiene_lista_citas("2022-07-26T14:00:00Z","2022-07-26T23:59:00Z"))
