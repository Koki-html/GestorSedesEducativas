"""Rutas del modulo de agenda."""

from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
	path('', views.inicio, name='inicio'),
	path('lista/', views.lista_compromisos, name='lista_compromisos'),
	path('detalle/<int:pk>/', views.detalle_compromiso, name='detalle_compromiso'),
	path('resumen/', views.resumen_agenda, name='resumen_agenda'),
]
