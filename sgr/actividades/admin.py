from django.contrib import admin

from .models import (
    ActividadMantenimiento,
    EvidenciaMantenimiento,
    SolicitudMantenimiento,
)


@admin.register(ActividadMantenimiento)
class ActividadMantenimientoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fecha',
        'colaborador',
        'asignacion_meta',
        'tipo',
        'responsable',
        'estado',
    )
    list_filter = ('estado', 'tipo', 'sector')
    search_fields = ('descripcion', 'origen', 'solicitante__nombres')
    date_hierarchy = 'fecha'


@admin.register(SolicitudMantenimiento)
class SolicitudMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_ingreso', 'solicitante', 'tipo', 'estado')
    list_filter = ('estado', 'tipo', 'subtipo')
    search_fields = ('solicitante__nombres', 'solicitante__apellidos')
    date_hierarchy = 'fecha_ingreso'


@admin.register(EvidenciaMantenimiento)
class EvidenciaMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'actividad', 'solicitud', 'autor', 'fecha', 'estado')
    list_filter = ('estado', 'fecha', 'tipo')
    search_fields = ('codigo', 'observacion', 'ubicacion_referencia')
