"""Rutas del modulo de resultados."""

from django.urls import path
from . import views

app_name = 'resultados'

urlpatterns = [
	path('', views.inicio, name='inicio'),
	path('metas/', views.lista_metas, name='lista_metas'),
	path('metas/<int:pk>/', views.detalle_meta, name='detalle_meta'),
	path('informe/', views.informe_resumen, name='informe_resumen'),
	path('responsables/<int:pk>/', views.resultado_responsable, name='resultado_responsable'),
	path('sedes/<int:pk>/', views.tablero_sede, name='tablero_sede'),
]
