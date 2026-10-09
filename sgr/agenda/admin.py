from django.contrib import admin
from .models import Compromiso


@admin.register(Compromiso)
class CompromisoAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'origen',
		'sede',
		'responsable',
		'fecha_comprometida',
		'prioridad',
		'estado',
	)
	list_filter = ('prioridad', 'estado', 'fecha_comprometida')
	search_fields = ('origen', 'sede__nombre', 'responsable__nombre')
	date_hierarchy = 'fecha_comprometida'
