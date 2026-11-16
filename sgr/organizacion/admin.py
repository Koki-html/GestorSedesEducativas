from django.contrib import admin

from .models import (
    Cargo,
    ComiteSede,
    Espacio,
    HitoMantenimiento,
    ParticipacionComite,
    Rol,
    Sector,
    SedeEducativa,
    Solicitante,
    SubtipoServicio,
    TipoServicio,
    UsuarioColaborador,
)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('codigo', 'nombre')


@admin.register(SedeEducativa)
class SedeEducativaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'sector', 'encargado', 'estado')
    list_filter = ('estado', 'sector')
    search_fields = ('codigo', 'nombre', 'direccion')


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('codigo', 'nombre')


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'grupo', 'estado')
    list_filter = ('estado', 'grupo')
    search_fields = ('codigo', 'nombre')


@admin.register(UsuarioColaborador)
class UsuarioColaboradorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'cargo', 'sede', 'estado', 'ultimo_acceso')
    list_filter = ('estado', 'cargo', 'sede', 'roles')
    search_fields = ('rut', 'nombres', 'apellidos', 'correo')


@admin.register(Solicitante)
class SolicitanteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'sector', 'estado')
    list_filter = ('estado', 'sector')
    search_fields = ('rut', 'nombres', 'apellidos', 'correo')


@admin.register(ComiteSede)
class ComiteSedeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'sede', 'sector', 'fecha_constitucion', 'estado')
    list_filter = ('estado', 'sede', 'sector')
    search_fields = ('codigo', 'nombre')


@admin.register(ParticipacionComite)
class ParticipacionComiteAdmin(admin.ModelAdmin):
    list_display = ('comite', 'solicitante', 'cargo', 'es_coordinador', 'estado')
    list_filter = ('estado', 'es_coordinador', 'comite')


@admin.register(HitoMantenimiento)
class HitoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'sede', 'periodicidad', 'estado')
    list_filter = ('estado', 'sede', 'sector')
    search_fields = ('codigo', 'nombre')


@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sede', 'tipo', 'estado')
    list_filter = ('tipo', 'estado', 'sede')
    search_fields = ('nombre', 'ubicacion')


@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('codigo', 'nombre')


@admin.register(SubtipoServicio)
class SubtipoServicioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'estado')
    list_filter = ('estado', 'tipo')
    search_fields = ('codigo', 'nombre')
