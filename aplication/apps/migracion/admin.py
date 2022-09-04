from django.contrib import admin
from .models import Error, CitaSquare, Sincronizacion
# Register your models here.
class CitaSquareAdmin(admin.ModelAdmin):
    list_display=['IdRef','Fecha','Hora','Nombre', 'Version']
    #inlines=[pedido_varianteAdmin]
    #search_fields=['titulo']
    readonly_fields=('FechaCreacion','FechaModificacion')

class SincronizacionAdmin(admin.ModelAdmin):
    readonly_fields=('FechaCreacion','Rango','Observacion','UsuarioCreacion')


admin.site.register(CitaSquare, CitaSquareAdmin)
admin.site.register(Error)
admin.site.register(Sincronizacion, SincronizacionAdmin)
