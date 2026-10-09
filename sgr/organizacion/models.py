from django.db import models


class Sede(models.Model):
	"""Representa una sede educativa administrada por el sistema."""

	nombre = models.CharField(max_length=150)
	direccion = models.CharField(max_length=255)
	comuna = models.CharField(max_length=100)
	encargado = models.CharField(max_length=150)
	estado = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre


class Espacio(models.Model):
	"""Representa un espacio físico perteneciente a una sede."""

	sede = models.ForeignKey(
		Sede,
		on_delete=models.PROTECT,
		related_name='espacios',
	)
	nombre = models.CharField(max_length=150)
	tipo = models.CharField(max_length=100)
	ubicacion = models.CharField(max_length=255)
	estado = models.CharField(max_length=50)

	def __str__(self):
		return f'{self.sede.nombre} - {self.nombre}'


class Responsable(models.Model):
	"""Representa a una persona responsable asociada a una sede."""

	nombre = models.CharField(max_length=150)
	cargo = models.CharField(max_length=150)
	especialidad = models.CharField(max_length=150)
	sede = models.ForeignKey(
		Sede,
		on_delete=models.PROTECT,
		related_name='responsables',
	)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre
