from django.contrib import admin
from .models import Articulo, Variante, Cliente, Pedido, PedidoDetalle, PedidoBitacora 
# Register your models here.


admin.site.register(Articulo)
admin.site.register(Variante)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)
admin.site.register(PedidoBitacora)
