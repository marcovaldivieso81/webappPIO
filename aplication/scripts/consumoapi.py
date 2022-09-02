import requests
import json
from pathlib import Path
import environ
import aiohttp
from datetime import datetime
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
env=environ.Env()
environ.Env.read_env(f"{BASE_DIR}/aplication/.env")

URL_SQUARE = env.str('URL_SQUARE')
LOCATION_ID_SQUARE = env.str('LOCATION_ID_SQUARE')
TOKEN_SQUARE = 'Bearer '+env.str('TOKEN_SQUARE')

def ajusta_hora(date,delta):
    date=datetime.strptime(date[0:10]+' '+date[-9:-1], '%Y-%m-%d %H:%M:%S')
    date_fin=date+timedelta(hours=delta)
    date_fin=date_fin.strftime("%Y-%m-%d")+'T'+date_fin.strftime("%H:%M:%S")+'Z'
    return date_fin

#input="2022-07-21T14:00:00Z"
#print(input)
#resultado=ajusta_hora(input,-5)
#print(resultado)

def square_bookings(inicio,fin):
    #print(inicio)
    #print(fin)
    #print('--------')
    args = {'limit':1000,
            'location_id': LOCATION_ID_SQUARE,
            'start_at_min': ajusta_hora(inicio,4), # "2022-07-21T14:00:00Z",
            'start_at_max': ajusta_hora(fin,4), #"2022-07-21T23:59:00Z"
            }
    headers = {'Authorization': TOKEN_SQUARE}
    #print(TOKEN_SQUARE)
    #print('Inicio consumo de api')
    response = requests.get(URL_SQUARE+'bookings',params=args,headers=headers)
    #print('Consumo de api realizado')
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        lista_citas=[]
        for cita in response_decode['bookings']:
            print(cita['start_at'])
            cita['start_at']=ajusta_hora(cita['start_at'],-4)
            lista_citas.append(cita)
        #print(lista_citas)
        #for cita in lista_citas:
        #    print('-----')
        #    print(cita['start_at'])
        #return response_decode['bookings']
        return lista_citas
#square_bookings("2022-09-01T00:00:00Z","2022-09-02T23:59:59Z")

#for cita in citas:
#    print("----------------------")
#    print(cita['start_at'])

async def square_customer(customer_id):
    headers = {'Authorization': TOKEN_SQUARE}
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_SQUARE+'customers'+'/'+customer_id,headers=headers) as response:
            #print(response.status)
            if response.status != 200:
                return (False,customer_id)
            content=await response.text()
            customer = json.loads(content)['customer']
            datos_customer = {
                        'Nombre': customer.get('given_name', '') + ' ' +  customer.get('family_name',''),
                        'Telefono' : customer.get('phone_number','no number'),
                        'Correo' : customer.get('email_address','sinmail@sinmail.com'),
                        }
            return (True,datos_customer)
        
def square_articulos():
    headers = {'Authorization': TOKEN_SQUARE}
    args = {'type':'ITEM'}
    response = requests.get(URL_SQUARE+'catalog/list',params = args,headers = headers)
    if response.status_code == 200:
        content = response.content
        response_decode = json.loads(content.decode('utf8'))
        #print(response_decode)
        return response_decode

