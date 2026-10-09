from django.db import models
from organizacion.models import Espacio, Responsable, Sede

class Actividad(models.Model):
    """Representa una actividad realizada o programada en una sede."""

    fecha = models.DateField()
    sede = models.ForeignKey(
        Sede,
        on_delete=models.PROTECT,
        related_name='actividades',
    )
    espacio = models.ForeignKey(
        Espacio,
        on_delete=models.PROTECT,
        related_name='actividades',
    )
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    accion = models.TextField()
    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.PROTECT,
        related_name='actividades',
    )
    estado = models.CharField(max_length=50)
    aprobada = models.BooleanField(default=False)
    corregida = models.BooleanField(null=True, blank=True)
    avance_aprobado = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'Actividad {self.pk}: {self.tipo}'


class Evidencia(models.Model):
    """Representa un archivo que respalda una actividad."""

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.CASCADE,
        related_name='evidencias',
    )
    codigo = models.CharField(max_length=50)
    archivo_url = models.CharField(max_length=255)
    fecha = models.DateField()
    estado = models.CharField(max_length=50)
    observacion = models.TextField()

    def __str__(self):
        return self.codigo