from django.db import models

# Create your models here.
class Sincronizacion(models.Model):
    Abreviatura=models.CharField(max_length=20)
    Descripcion=models.CharField(max_length=500)
    FechaInicio=models.DateField()
    FechaFin=models.DateField()
    Horas=models.IntegerField()
    Observacion=models.CharField(max_length=500,blank=True,null=True)
    FechaCreacion=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    UsuarioCreacion=models.CharField(max_length=100,blank=True,null=True)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100)
    Eliminado=models.BooleanField()

class CitaSquare(models.Model):
    IdRef=models.CharField(max_length=30)
    Version = models.IntegerField(default=0)
    Nombre=models.CharField(max_length=200)
    Direccion=models.CharField(max_length=200)
    Correo=models.EmailField(max_length=100)
    Telefono=models.CharField(max_length=100)
    #Fecha=models.CharField(max_length=100)
    Fecha=models.DateField()
    #Hora=models.CharField(max_length=100)
    Hora=models.TimeField()
    Nota=models.TextField()
    Servicios=models.CharField(max_length=100)
    #Articulos=models.TextField(blank=True,null=True)
    #FlgProcesado=models.BooleanField(default=False,null=True)#,blank=True,null=True)
    Observacion=models.CharField(max_length=500,blank=True,null=True)
    FechaCreacion=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    UsuarioCreacion=models.CharField(max_length=100,blank=True,null=True)
    FechaModificacion=models.DateTimeField(auto_now=True,blank=True,null=True)
    UsuarioModificacion=models.CharField(max_length=100,blank=True,null=True)
    #Eliminado=models.BooleanField(default=False,null=True)#,blank=True,null=True)
    def __str__(self):
        return self.IdRef+' -> '+self.Nombre+' / '+self.Direccion

class Error(models.Model):
    Codigo=models.CharField(max_length=10)
    Observacion=models.TextField()
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)

