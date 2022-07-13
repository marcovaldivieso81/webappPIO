from django.db import models

# Create your models here.

class CitaSquare(models.Model):
    IdRef=models.CharField(max_length=30)
    Nombre=models.CharField(max_length=200)
    Correo=models.EmailField(max_length=100)
    Telefono=models.CharField(max_length=100)
    Fecha=models.CharField(max_length=100)
    Hora=models.CharField(max_length=100)
    Nota=models.CharField(max_length= 500)
    Servicios=models.TextField()
    Articulos=models.TextField()
    FlgProcesado=models.BooleanField()
    Observacion=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100)
    Eliminado=models.BooleanField()

class Error(models.Model):
    Codigo=models.CharField(max_length=10)
    Observacion=models.TextField()
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)

