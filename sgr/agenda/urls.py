"""Rutas del modulo de agenda."""

from django.urls import path
from . import views
from .models import Compromiso
from sgr.crud import (
    CrudCreateView,
    CrudDeleteView,
    CrudDetailView,
    CrudListView,
    CrudUpdateView,
)

app_name = 'agenda'

urlpatterns = [
	path('', views.inicio, name='inicio'),
	path('lista/', views.lista_compromisos, name='lista_compromisos'),
	path('detalle/<int:pk>/', views.detalle_compromiso, name='detalle_compromiso'),
	path('resumen/', views.resumen_agenda, name='resumen_agenda'),
]


# Compromiso: pendientes calendarizados por sede y responsable.
_crud_options = {
	'model': Compromiso,
	'crud_namespace': app_name,
	'crud_name': 'compromisos',
}
urlpatterns += [
	path(
	    'crud/compromisos/',
	    CrudListView.as_view(**_crud_options),
	    name='compromisos_list',
	),
	path(
	    'crud/compromisos/nuevo/',
	    CrudCreateView.as_view(**_crud_options),
	    name='compromisos_create',
	),
	path(
	    'crud/compromisos/<int:pk>/',
	    CrudDetailView.as_view(**_crud_options),
	    name='compromisos_detail',
	),
	path(
	    'crud/compromisos/<int:pk>/editar/',
	    CrudUpdateView.as_view(**_crud_options),
	    name='compromisos_update',
	),
	path(
	    'crud/compromisos/<int:pk>/eliminar/',
	    CrudDeleteView.as_view(**_crud_options),
	    name='compromisos_delete',
	),
]
