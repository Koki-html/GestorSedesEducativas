from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from organizacion.models import UsuarioColaborador


STATUS_CHOICES = (
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
    ('terminado', 'Terminado'),
)


class Trimestre(models.Model):
    codigo = models.CharField(max_length=30, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=150, blank=True, default='')
    anio = models.PositiveSmallIntegerField(null=True, blank=True)
    numero = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        null=True,
        blank=True,
    )
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.nombre} - {self.anio}'


class MetaMantenimiento(models.Model):
    codigo = models.CharField(max_length=30, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=255, blank=True, default='')
    descripcion = models.TextField(blank=True, default='')
    tipo = models.ForeignKey(
        'organizacion.TipoServicio',
        on_delete=models.PROTECT,
        related_name='metas',
        null=True,
        blank=True,
    )
    unidad_medida = models.CharField(max_length=100, blank=True, default='')
    requisito_evidencia = models.TextField(blank=True, default='')
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class AsignacionMeta(models.Model):
    colaborador = models.ForeignKey(
        UsuarioColaborador,
        on_delete=models.PROTECT,
        related_name='asignaciones_metas',
    )
    meta = models.ForeignKey(
        MetaMantenimiento,
        on_delete=models.CASCADE,
        related_name='asignaciones',
    )
    trimestre = models.ForeignKey(
        Trimestre,
        on_delete=models.PROTECT,
        related_name='asignaciones',
    )
    cantidad_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    ponderacion = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_asignacion = models.DateField()
    observacion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'{self.meta} - {self.colaborador}'


class Resultado(models.Model):
    meta = models.OneToOneField(
        MetaMantenimiento,
        on_delete=models.CASCADE,
        related_name='resultado',
    )
    avance = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_calculo = models.DateField()

    def __str__(self):
        return f'Resultado de {self.meta_id}'
