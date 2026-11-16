from django.contrib import admin

from .models import AsignacionMeta, MetaMantenimiento, Resultado, Trimestre


@admin.register(Trimestre)
class TrimestreAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'anio', 'numero', 'fecha_inicio', 'fecha_termino', 'estado')
    list_filter = ('anio', 'numero', 'estado')
    search_fields = ('codigo', 'nombre')
    date_hierarchy = 'fecha_inicio'


@admin.register(MetaMantenimiento)
class MetaMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'unidad_medida', 'estado')
    list_filter = ('estado', 'tipo')
    search_fields = ('codigo', 'nombre', 'descripcion')


@admin.register(AsignacionMeta)
class AsignacionMetaAdmin(admin.ModelAdmin):
    list_display = (
        'meta',
        'colaborador',
        'trimestre',
        'cantidad_objetivo',
        'ponderacion',
        'fecha_asignacion',
        'estado',
    )
    list_filter = ('estado', 'trimestre', 'colaborador')
    search_fields = ('meta__nombre', 'colaborador__nombres', 'colaborador__apellidos')
    date_hierarchy = 'fecha_asignacion'


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('meta', 'avance', 'fecha_calculo')
    list_filter = ('fecha_calculo',)
    search_fields = ('meta__nombre',)
    date_hierarchy = 'fecha_calculo'
