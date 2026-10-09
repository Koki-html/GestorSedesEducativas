from django.contrib import admin
from .models import Actividad, Evidencia


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
	list_display = ('id', 'fecha', 'tipo', 'sede', 'responsable', 'estado', 'aprobada')
	list_filter = ('estado', 'tipo', 'aprobada', 'corregida')
	search_fields = ('descripcion', 'accion', 'tipo')
	date_hierarchy = 'fecha'


@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'actividad', 'fecha', 'estado')
	list_filter = ('estado', 'fecha')
	search_fields = ('codigo', 'observacion')