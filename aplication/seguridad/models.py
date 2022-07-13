from django.db import models

# Create your models here.

class Usuario(models.Model):
    IdTipoUsuario=models.IntegerField()
    CodUsuario=models.CharField(max_length=50)
    Usuario=models.CharField(max_length=100)
    Contrasena=models.CharField(max_length=100)
    Nombre=models.CharField(max_length=100)
    ApellidoPaterno=models.CharField(max_length=100)
    ApellidoMaterno=models.CharField(max_length=100)
    Correo=models.EmailField(max_length=200)
    Telefono=models.CharField(max_length=20)
    Observacion=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100)
    Eliminado=models.BooleanField()
