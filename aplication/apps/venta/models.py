from django.db import models
from colorfield.fields import ColorField
# Create your models here.

class Articulo(models.Model):
    #IdArticulo=models.AutoField(primary_key=True)
    IdArticuloSquare=models.CharField(max_length=50,primary_key=True)
    Descripcion=models.CharField(max_length=500)
    Codigo=models.IntegerField(null=True,blank=True)
    Nota1=models.CharField(max_length=500,null=True,blank=True)
    Nota2=models.CharField(max_length=500,null=True,blank=True)
    Nota3=models.CharField(max_length=500,null=True,blank=True)
    FechaCreacion=models.DateTimeField(auto_now_add=True,null=True)
    UsuarioCreacion=models.CharField(max_length=100,null=True,blank=True)
    FechaModificacion=models.DateTimeField(auto_now=True,null=True)
    UsuarioModificacion=models.CharField(max_length=100,null=True,blank=True)
    #Eliminado=models.BooleanField()
    def __str__(self):
        return self.Descripcion


class Variante(models.Model):
    #IdVariante=models.AutoField(primary_key=True)
    IdVarianteSquare=models.CharField(max_length=100,primary_key=True)
    #IdArticulo=models.IntegerField()
    Descripcion=models.CharField(max_length=500)
    IdArticulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    PrecioUnitario=models.DecimalField(max_digits=20,decimal_places=5)
    IdMoneda=models.CharField(max_length=10)
    Codigo=models.IntegerField(null=True,blank=True) 
    Nota1=models.CharField(max_length=500,null=True,blank=True)
    Nota2=models.CharField(max_length=500,null=True,blank=True)
    Nota3=models.CharField(max_length=500,null=True,blank=True)
    FechaCreacion=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    UsuarioCreacion=models.CharField(max_length=100,null=True,blank=True)
    FechaModificacion=models.DateTimeField(auto_now=True,null=True,blank=True)
    UsuarioModificacion=models.CharField(max_length=100,null=True,blank=True)
    #Eliminado=models.BooleanField()
    def __str__(self):
        return self.IdArticulo.Descripcion+' | '+self.Descripcion

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

'''
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
'''
class Estado(models.Model):
    IdEstado = models.CharField(primary_key=True,max_length=30)
    color = ColorField(default='#FF0000')
    def __str__(self):
        return self.IdEstado

class Servicio(models.Model):
    IdServicio = models.CharField(primary_key=True, max_length=30)
    Tipo = models.CharField(max_length=30)
    def __str__(self):
        return self.Tipo

class Pedido(models.Model):
    IdPedidoSquare = models.CharField(primary_key=True,max_length=100)
    NombreCliente = models.CharField(max_length=100,default='Sin nombre')
    Telefono = models.CharField(max_length=30,null=True,blank=True)
    Direccion = models.CharField(max_length=200,null=True,blank=True) 
    Fecha = models.DateField(null=True)
    Hora = models.TimeField(null=True)
    Articulos = models.ManyToManyField(Variante,through='pedido_variante')
    Notas = models.TextField()
    Servicio = models.ForeignKey(to=Servicio, on_delete=models.CASCADE,blank=True,null=True)
    Estado = models.ForeignKey(to=Estado, on_delete=models.CASCADE,blank=True,null=True,default='pendiente')
    Cancelado=models.BooleanField(default=False)
    Observacion = models.TextField(default='prueba')
    FechaCreacion = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    UsuarioCreacion = models.CharField(max_length=100,null=True,blank=True)
    FechaModificacion = models.DateTimeField(auto_now=True,null=True,blank=True)

class pedido_variante(models.Model):
    pedido = models.ForeignKey(Pedido,on_delete=models.CASCADE)
    variante = models.ForeignKey(Variante,on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    class Meta:
        verbose_name='Pedido / variante'
        verbose_name_plural='Pedido / variantess'
        db_table='venta_pedido_variante'
    def __str__(self):
        return str(self.pedido)


class PedidoBitacora(models.Model):
    IdPedidoBitacora=models.AutoField(primary_key=True)
    IdPedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    IdEstado=models.IntegerField()
    Observacion=models.CharField(max_length=500)
    FechaCreacion=models.DateTimeField(auto_now_add=True)
    UsuarioCreacion=models.CharField(max_length=100)
    FechaModificacion=models.DateTimeField(auto_now=True)
    Eliminado=models.BooleanField()




