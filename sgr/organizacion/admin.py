from django.contrib import admin
from .models import Espacio, Responsable, Sede


@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'comuna', 'encargado', 'estado')
	list_filter = ('estado', 'comuna')
	search_fields = ('nombre', 'direccion', 'encargado')


@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'sede', 'tipo', 'estado')
	list_filter = ('tipo', 'estado', 'sede')
	search_fields = ('nombre', 'ubicacion')


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'cargo', 'especialidad', 'sede', 'activo')
	list_filter = ('activo', 'cargo', 'sede')
	search_fields = ('nombre', 'cargo', 'especialidad')
