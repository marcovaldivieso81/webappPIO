from django.db import models

# Create your models here.

class Articulo(models.Model):
    IdArticulo=models.AutoField(primary_key=True)
    IdArticuloSquare=models.CharField(max_length=20)
    Codigo=models.IntegerField()
    Descripcion=models.CharField(max_length=500)
    Nota1=models.CharField(max_length=500)
    Nota2=models.CharField(max_length=500)
    Nota3=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100)
    Eliminado=models.BooleanField()

class Variante(models.Model):
    IdVariante=models.AutoField(primary_key=True)
    IdVarianteSquare=models.CharField(max_length=20)
    IdArticulo=models.IntegerField()
    Codigo=models.IntegerField()
    Descripcion=models.CharField(max_length=500)
    Nota1=models.CharField(max_length=500)
    Nota2=models.CharField(max_length=500)
    Nota3=models.CharField(max_length=500)
    IdMoneda=models.IntegerField()
    PrecioUnitario=models.DecimalField(max_digits=20,decimal_places=5)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    UsuarioModificacion=models.CharField(max_length=100)
    Eliminado=models.BooleanField()

class Cliente(models.Model):
    IdCliente=models.AutoField(primary_key=True)
    Nombre=models.CharField(max_length=100)
    Nombre2=models.CharField(max_length=100)
    ApellidoPaterno=models.CharField(max_length=100)
    ApellidoMaterno=models.CharField(max_length=100)
    Correo=models.EmailField(max_length=100)
    Telefono=models.CharField(max_length=20)
    Observacion=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    Eliminado=models.BooleanField()

class Pedido(models.Model):
    IdPedido=models.AutoField(primary_key=True)
    IdPedidoSquare=models.CharField(max_length=20)
    IdCliente=models.IntegerField()
    IdMoneda=models.IntegerField()
    PrecioTotal=models.DecimalField(max_digits=20,decimal_places=5)
    Notas=models.TextField()
    FechaEntregaInicial=models.DateTimeField()
    FechaEntregaFinal=models.DateTimeField()
    Direccion=models.TextField()
    FlgDelivery=models.BooleanField()
    IdEstado=models.IntegerField()
    Observacion=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    Eliminado=models.BooleanField()

class PedidoDetalle(models.Model):
    IdPedidoDetalle=models.AutoField(primary_key=True)
    IdPedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    IdArticulo=models.ForeignKey(Articulo, on_delete=models.CASCADE)
    IdVariante=models.ForeignKey(Variante, on_delete=models.CASCADE)
    IdUnidadMedida=models.IntegerField()
    Cantidad=models.DecimalField(max_digits=20,decimal_places=5)
    IdMoneda=models.IntegerField()
    PrecioUnitario=models.DecimalField(max_digits=20,decimal_places=5)
    PrecioTotal=models.DecimalField(max_digits=20,decimal_places=5)
    Nota1=models.CharField(max_length=500)
    Nota2=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    Eliminado=models.BooleanField()

class PedidoBitacora(models.Model):
    IdPedidoBitacora=models.AutoField(primary_key=True)
    IdPedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    IdEstado=models.IntegerField()
    Observacion=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    Eliminado=models.BooleanField()




