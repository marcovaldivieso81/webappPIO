from django.db import models

# Create your models here.

class TipoCatalogo(models.Model):
    IdTipoCatalogo=models.AutoField(primary_key=True)
    Nombre=models.CharField(max_length=100)
    Identificador=models.CharField(max_length=100,unique=True)
    Observacion=models.CharField(max_length=500,null=True,blank=True)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100,null=True,blank=True)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100,null=True,blank=True)
    Eliminado=models.BooleanField(default=False)

class Catalogo(models.Model):
    IdCatalogo=models.AutoField(primary_key=True)
    IdTipoCatalogo=models.ForeignKey(TipoCatalogo,on_delete=models.CASCADE)
    Codigo=models.CharField(max_length=50)
    Nombre=models.CharField(max_length=200)
    Descripcion=models.CharField(max_length=500,null=True,blank=True)
    Abrev=models.CharField(max_length=10,null=True,blank=True)
    Nota1=models.CharField(max_length=50,null=True,blank=True)
    Nota2=models.CharField(max_length=50,null=True,blank=True)
    Nota3=models.CharField(max_length=50,null=True,blank=True)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100,null=True,blank=True)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100,null=True,blank=True)
    Eliminado=models.BooleanField(default=False)
