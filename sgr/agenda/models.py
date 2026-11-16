from django.db import models

from organizacion.models import SedeEducativa, UsuarioColaborador


class Compromiso(models.Model):
    origen = models.CharField(max_length=150)
    sede = models.ForeignKey(
        SedeEducativa,
        on_delete=models.PROTECT,
        related_name='compromisos',
    )
    responsable = models.ForeignKey(
        UsuarioColaborador,
        on_delete=models.PROTECT,
        related_name='compromisos',
    )
    fecha_comprometida = models.DateField()
    prioridad = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default='activo')

    def __str__(self):
        return f'{self.origen} - {self.fecha_comprometida}'
