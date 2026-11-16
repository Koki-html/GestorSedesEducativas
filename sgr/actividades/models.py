from django.db import models

from organizacion.models import (
    HitoMantenimiento,
    Sector,
    Solicitante,
    SubtipoServicio,
    TipoServicio,
    UsuarioColaborador,
)


STATUS_CHOICES = (
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
    ('terminado', 'Terminado'),
)


class ActividadMantenimiento(models.Model):
    fecha = models.DateField()
    colaborador = models.ForeignKey(
        UsuarioColaborador,
        on_delete=models.PROTECT,
        related_name='actividades_colaborador',
        null=True,
        blank=True,
    )
    asignacion_meta = models.ForeignKey(
        'resultados.AsignacionMeta',
        on_delete=models.PROTECT,
        related_name='actividades',
        null=True,
        blank=True,
    )
    hito = models.ForeignKey(
        HitoMantenimiento,
        on_delete=models.PROTECT,
        related_name='actividades',
        null=True,
        blank=True,
    )
    tipo = models.ForeignKey(TipoServicio, on_delete=models.PROTECT, related_name='actividades')
    descripcion = models.TextField()
    origen = models.CharField(max_length=150, blank=True, default='')
    solicitante = models.ForeignKey(
        Solicitante,
        on_delete=models.PROTECT,
        related_name='actividades',
        null=True,
        blank=True,
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.PROTECT,
        related_name='actividades',
        null=True,
        blank=True,
    )
    responsable = models.ForeignKey(
        UsuarioColaborador,
        on_delete=models.PROTECT,
        related_name='actividades_responsable',
        null=True,
        blank=True,
    )
    fecha_compromiso = models.DateField(null=True, blank=True)
    apoyo = models.TextField(blank=True, null=True)
    avance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')
    resultado = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Actividad {self.pk}: {self.descripcion[:40]}'


class SolicitudMantenimiento(models.Model):
    fecha_ingreso = models.DateField()
    fecha_atencion = models.DateField(null=True, blank=True)
    solicitante = models.ForeignKey(
        Solicitante,
        on_delete=models.PROTECT,
        related_name='solicitudes',
    )
    tipo = models.ForeignKey(TipoServicio, on_delete=models.PROTECT, related_name='solicitudes')
    subtipo = models.ForeignKey(
        SubtipoServicio,
        on_delete=models.PROTECT,
        related_name='solicitudes',
    )
    asignacion_meta = models.ForeignKey(
        'resultados.AsignacionMeta',
        on_delete=models.PROTECT,
        related_name='solicitudes',
    )
    visita = models.TextField(blank=True)
    actuaciones = models.TextField(blank=True)
    derivacion = models.TextField(blank=True)
    informe = models.TextField(blank=True)
    solucion = models.TextField(blank=True)
    resultado = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')

    def __str__(self):
        return f'Solicitud {self.pk} - {self.solicitante}'


class EvidenciaMantenimiento(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    actividad = models.ForeignKey(
        ActividadMantenimiento,
        on_delete=models.CASCADE,
        related_name='evidencias',
        null=True,
        blank=True,
    )
    solicitud = models.ForeignKey(
        SolicitudMantenimiento,
        on_delete=models.CASCADE,
        related_name='evidencias',
        null=True,
        blank=True,
    )
    tipo = models.CharField(max_length=100, blank=True, default='')
    ubicacion_referencia = models.CharField(max_length=255, blank=True, default='')
    autor = models.ForeignKey(
        UsuarioColaborador,
        on_delete=models.PROTECT,
        related_name='evidencias_autor',
        null=True,
        blank=True,
    )
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='activo')
    observacion = models.TextField(blank=True)
    verificador = models.ForeignKey(
        UsuarioColaborador,
        on_delete=models.PROTECT,
        related_name='evidencias_verificadas',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.codigo
