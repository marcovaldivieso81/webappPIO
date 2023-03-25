from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from sendfile import sendfile

from datetime import date
from datetime import datetime

from .models import ZonaHoraria
##ejecucion de comandos de terminal
import subprocess
## se importan variables de entorno
from pathlib import Path
import environ
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env(f"{BASE_DIR}/aplication/.env")

# Create your views here.
@login_required
def home(request): #acercade
    zonahoraria = ZonaHoraria.objects.all()[0]

    if request.method == 'POST':
        if request.POST['tipopost'] == 'zonahoraria':
            newzona = request.POST['DeltaHora']
            print('delta hora: ', newzona)
            zonahoraria.DeltaHora = newzona
            zonahoraria.save()
        elif request.POST['tipopost'] == 'backup':
            host = env.str('DATA_BASE_HOST'),
            user = env.str('DATA_BASE_USER'), 
            password = env.str('DATA_BASE_PASSWORD'),
            database = env.str('DATA_BASE_NAME')
            dir_backup = str(BASE_DIR)+'/backups' 
            now = str(datetime.now())
            print(now)
            guardabd = subprocess.run(['pg_dump', '-U',user[0],'-d', database, '-f', dir_backup+'/copiabd_'+now+'.sql'])
            return sendfile(request,dir_backup+'/copiabd_'+now+'.sql') 
    ctx = {'zonahoraria':zonahoraria}
    return render(request,'configuracion/home.html',ctx)

