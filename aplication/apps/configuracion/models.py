from django.db import models

# Create your models here.
class ZonaHoraria(models.Model):
    DeltaHora=models.IntegerField()
    FechaCreacion=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    FechaModificacion=models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return str(self.DeltaHora)



