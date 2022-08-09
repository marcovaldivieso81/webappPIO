from django.contrib import admin
from .models import Articulo, Variante, Cliente, Pedido, PedidoBitacora, Estado, pedido_variante, Servicio 
# Register your models here.

class pedido_varianteAdmin(admin.TabularInline):
    model=pedido_variante
    extra=1
    autocomplete_fields=['variante']

class PedidoAdmin(admin.ModelAdmin):
    list_display=['Fecha','Estado','Hora','Servicio','Cancelado','NombreCliente', 'Telefono', 'Direccion']
    inlines=[pedido_varianteAdmin]
    list_filter=['Estado','Servicio']
    list_editable=['Cancelado']
    search_fields=['NombreCliente']

    list_per_page=20

    #search_fields=['titulo']
    #readonly_fields=('created','updated')

class VarianteAdmin(admin.ModelAdmin):
    search_fields=['IdArticulo_id__Descripcion']
    #inlines=[alternativaAdmin]
    #readonly_fields=('created','updated')
    class Meta:
        model=Variante

admin.site.register(Articulo)
admin.site.register(Variante, VarianteAdmin)
admin.site.register(Cliente)
admin.site.register(Pedido,PedidoAdmin)
admin.site.register(PedidoBitacora)
admin.site.register(Estado)
admin.site.register(Servicio)
