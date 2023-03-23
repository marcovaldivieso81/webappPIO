from django.contrib import admin

# Register your models here.
from .models import ZonaHoraria
# Register your models here.
class ZonaHorariaAdmin(admin.ModelAdmin):
    list_display=['DeltaHora','FechaModificacion']
    #inlines=[pedido_varianteAdmin]
    #search_fields=['titulo']
    readonly_fields=('FechaCreacion','FechaModificacion')


admin.site.register(ZonaHoraria, ZonaHorariaAdmin)
