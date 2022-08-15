from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q ## ESTO SIRVE PARA HACER BÚSQUEDA
from datetime import date, timedelta
import json
from .models import Pedido, Variante, Articulo, Estado, Servicio, pedido_variante
from scripts.utilidades_db import guarda_citas 
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
            # ACA DEBO IMPLEMENTAR EL GUARDADO DE PRODUCTO 
            form=request.POST
            #form = dict(queryDict.iterlists())
            print('-------------')
            print(form)
            print('-------------')
            datos_guardados=Pedido.objects.filter(IdPedidoSquare=form['IdPedido'])
            #print('-------------------')
            #print(datos_guardados)
            #print('------------------')
            datos_guardados.update(Observacion=form['Observacion'])
            #prod_json=json.loads(form['prod'])
            prod_json=form.getlist('prod')
            print(type(prod_json))
            print('------------------------')
            for producto in prod_json:
                producto=json.loads(producto)
                pedido_variante.objects.create(
                    pedido_id=form['IdPedido'],
                    variante_id=producto['name'],
                    cantidad=producto['quantity'])
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
        servicios=Servicio.objects.all
        estados=Estado.objects.all
    ctx={
            'pedidos':pedidos,
            'search':search,
            'servicios':servicios,
            'estados':estados}
    return render(request,'venta/home.html',ctx)

@login_required
def api_productos(request):
    productos=Variante.objects.all()
    lista_productos=[]
    for producto in productos:
        data_producto={}
        data_producto['value']=producto.IdVarianteSquare
        Name=Articulo.objects.get(IdArticuloSquare = producto.IdArticulo_id)
        data_producto['label']=Name.Descripcion+' - '+producto.Descripcion
        lista_productos.append(data_producto)
    IdPedido=request.GET.get('idpedido')
    ctx={'products':lista_productos}
    if IdPedido:
        ContenidoPedido=Pedido.objects.get(IdPedidoSquare=IdPedido)
        pedidos=list(pedido_variante.objects.filter(pedido_id=IdPedido).values('cantidad','variante_id__IdArticulo__Descripcion','variante_id__Descripcion','variante_id'))
        #listapedidos=[]
        #for item in pedidos:
         #   dic={
         #           'pedido':type(item.pedido),
         #           'variante':item.variante,
         #           'cantidad':item.cantidad
         #           }
          #  listapedidos.append(dic)
        print(pedidos)
        ctx={
                'Observacion':ContenidoPedido.Observacion,
                'Notas':ContenidoPedido.Notas,
                'NombreCliente':ContenidoPedido.NombreCliente,
                'Telefono':ContenidoPedido.Telefono,
                'Direccion':ContenidoPedido.Direccion,
                'FechaHora':ContenidoPedido.Fecha.strftime("%d/%m/%y")+' - ' +ContenidoPedido.Hora.strftime("%H:%m"),
                'Cancelado':ContenidoPedido.Cancelado,
                'Estado':ContenidoPedido.Estado_id,
                'Servicio':ContenidoPedido.Servicio_id,
                'ListaPedidos':pedidos
            }
    return JsonResponse(ctx)
