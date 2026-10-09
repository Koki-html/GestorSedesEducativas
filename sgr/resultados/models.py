from django.db import models
from organizacion.models import Responsable, Sede


class Periodo(models.Model):
	"""Representa un período de evaluación de resultados."""

	fecha_inicio = models.DateField()
	fecha_termino = models.DateField()
	estado = models.CharField(max_length=50)

	def __str__(self):
		return f'{self.fecha_inicio} - {self.fecha_termino}'


class Meta(models.Model):
	"""Representa un indicador objetivo para una persona o sede."""

	periodo = models.ForeignKey(
		Periodo,
		on_delete=models.PROTECT,
		related_name='metas',
	)
	responsable = models.ForeignKey(
		Responsable,
		on_delete=models.PROTECT,
		related_name='metas',
		null=True,
		blank=True,
	)
	sede = models.ForeignKey(
		Sede,
		on_delete=models.PROTECT,
		related_name='metas',
		null=True,
		blank=True,
	)
	indicador = models.CharField(max_length=255)
	valor_objetivo = models.DecimalField(max_digits=5, decimal_places=2)
	ponderacion = models.DecimalField(max_digits=4, decimal_places=2)

	def __str__(self):
		return self.indicador


class Resultado(models.Model):
	"""Representa el avance calculado para una meta."""

	meta = models.OneToOneField(
		Meta,
		on_delete=models.CASCADE,
		related_name='resultado',
	)
	avance = models.DecimalField(max_digits=5, decimal_places=2)
	fecha_calculo = models.DateField()

	def __str__(self):
		return f'Resultado de {self.meta_id}'
