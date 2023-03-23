from django.shortcuts import render, redirect
#from django.urls import reverse
from django.contrib.auth.decorators import login_required
#from django.http import JsonResponse
#from django.http.response import HttpResponse
#from django.db.models import Q ## ESTO SIRVE PARA HACER BÚSQUEDA
#from datetime import date, timedelta
#import json
#from openpyxl import Workbook
from .models import ZonaHoraria

# Create your views here.
@login_required
def home(request): #acercade
    zonahoraria = ZonaHoraria.objects.all()[0]

    if request.method == 'POST':
        newzona = request.POST['DeltaHora']
        print('delta hora: ', newzona)
        zonahoraria.DeltaHora = newzona
        zonahoraria.save()
    ctx = {'zonahoraria':zonahoraria}
    return render(request,'configuracion/home.html',ctx)

