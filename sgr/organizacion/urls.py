"""Rutas del modulo de organizacion."""

from django.urls import path
from . import views

# Permite identificar estas rutas con el espacio de nombres organizacion.
app_name = 'organizacion'

urlpatterns = [
    # /organizacion/ es el inicio propio de este modulo.
    path('', views.inicio, name= 'inicio'),
    # /organizacion/sedes/ muestra las sedes disponibles.
    path('sedes/', views.lista_sedes, name='lista_sedes'),
    path('sedes/<int:pk>/', views.detalle_sede, name='detalle_sede'),
    path('responsables/', views.lista_responsables, name='lista_responsables'),
    path('responsables/<int:pk>/', views.detalle_responsable, name='detalle_responsable'),
]