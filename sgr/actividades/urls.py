"""Rutas del modulo de actividades."""

from django.urls import path
from . import views

# Permite identificar estas rutas con el espacio de nombres actividades.
app_name = 'actividades'

urlpatterns = [
    # /actividades/ es el inicio propio de este modulo.
    path('', views.inicio, name='inicio'),
    path('lista/', views.lista_actividades, name='lista_actividades'),
    path('detalle/<int:pk>/', views.detalle_actividad, name='detalle_actividad'),
    path('evidencias/', views.lista_evidencias, name='lista_evidencias'),
    path('evidencias/<int:pk>/', views.detalle_evidencia, name='detalle_evidencia'),
    path('evidence/<int:pk>/', views.evidence, name='evidence'),
]