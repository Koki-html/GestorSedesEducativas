from django.contrib import admin
from .models import Meta, Periodo, Resultado


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
	list_display = ('id', 'fecha_inicio', 'fecha_termino', 'estado')
	list_filter = ('estado',)
	date_hierarchy = 'fecha_inicio'


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'indicador',
		'periodo',
		'responsable',
		'sede',
		'valor_objetivo',
		'ponderacion',
	)
	list_filter = ('periodo', 'sede', 'responsable')
	search_fields = ('indicador',)


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
	list_display = ('meta', 'avance', 'fecha_calculo')
	list_filter = ('fecha_calculo',)
	search_fields = ('meta__indicador',)
	date_hierarchy = 'fecha_calculo'
