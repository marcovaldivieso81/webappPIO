from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import Pedido 
from scripts.utilidades_db import guarda_citas 
from django.db.models import Q ## ESTO SIRVE PARA HACER BÚSQUEDA
# Create your views here.
@login_required
def home(request): #acercade
    if request.method == 'POST':
        if request.POST['nombre'] == 'sinc':
            FechaActual=request.POST['FechaInicial']
            FechaFinal=request.POST['FechaFinal']
            guarda_citas(FechaActual+'T00:00:00Z', FechaFinal+'T23:59:00Z')
            return redirect(f'./?initial={FechaActual}&final={FechaFinal}')
        elif request.POST['nombre'] == 'search':
            search=request.POST['search']
            FechaActual=request.POST['FechaInicial']
            FechaFinal=request.POST['FechaFinal']
            return redirect(f'./?initial={FechaActual}&final={FechaFinal}&search={search}')
        elif request.POST['nombre'] == 'addproduct':
            print('-------------')
            print(request.POST)
            print('-------------')
    Finicial=request.GET.get('initial')
    Ffinal=request.GET.get('final')
    search=request.GET.get('search')
    if Finicial:
        FechaActual=date.fromisoformat(Finicial)
    else:
        FechaActual = date.today()
    if Ffinal:
        FechaFinal=date.fromisoformat(Ffinal)
    else:
        FechaFinal = FechaActual + timedelta(1)
    
    if search:
        pedidos=Pedido.objects.filter(
        Q(Fecha__gte = FechaActual)&
        Q(Fecha__lte = FechaFinal)&
        Q(NombreCliente__icontains=search) |
        Q(Telefono__icontains=search)
        ).distinct().order_by('Fecha','Hora')
    else:
        pedidos=Pedido.objects.filter(
            Fecha__gte=FechaActual,
            Fecha__lte=FechaFinal).order_by('Fecha','Hora')
        search=''
    ctx={'pedidos':pedidos,'search':search}
    return render(request,'venta/home.html',ctx)

