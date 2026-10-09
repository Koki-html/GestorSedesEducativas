from django.db import models
from organizacion.models import Responsable, Sede


class Compromiso(models.Model):
	"""Representa un compromiso con responsable, sede y fecha límite."""

	origen = models.CharField(max_length=150)
	sede = models.ForeignKey(
		Sede,
		on_delete=models.PROTECT,
		related_name='compromisos',
	)
	responsable = models.ForeignKey(
		Responsable,
		on_delete=models.PROTECT,
		related_name='compromisos',
	)
	fecha_comprometida = models.DateField()
	prioridad = models.CharField(max_length=20)
	estado = models.CharField(max_length=50)

	def __str__(self):
		return f'{self.origen} - {self.fecha_comprometida}'
