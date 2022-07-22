from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def handle_not_found(request,exception):
    #messages.error(request,'La página a la que intentas acceder no existe.')
    return redirect('login')
'''
def home(request): #acercade
    if request.user.is_authenticated:
        return redirect('venta/home.html')
    #contenido=Contenido.objects.filter(titulo='acercade')
    #ctx={'contenido':contenido[0]}
    return render(request,'seguridad/home.html')

'''
