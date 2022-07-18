from django.shortcuts import render

# Create your views here.

def home(request): #acercade
    #contenido=Contenido.objects.filter(titulo='acercade')
    #ctx={'contenido':contenido[0]}
    return render(request,'seguridad/home.html')


