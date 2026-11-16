"""Rutas del modulo de resultados."""

from django.urls import path
from . import views
from .models import AsignacionMeta, MetaMantenimiento, Resultado, Trimestre
from sgr.crud import (
    CrudCreateView,
    CrudDeleteView,
    CrudDetailView,
    CrudListView,
    CrudUpdateView,
)

app_name = 'resultados'

urlpatterns = [
	path('', views.inicio, name='inicio'),
	path('metas/', views.lista_metas, name='lista_metas'),
	path('metas/<int:pk>/', views.detalle_meta, name='detalle_meta'),
	path('informe/', views.informe_resumen, name='informe_resumen'),
	path('responsables/<int:pk>/', views.resultado_responsable, name='resultado_responsable'),
	path('sedes/<int:pk>/', views.tablero_sede, name='tablero_sede'),
]


def crud_paths(model, slug):
    """Construye las operaciones CRUD de un modelo de resultados."""
    options = {'model': model, 'crud_namespace': app_name, 'crud_name': slug}
    return [
        path(f'crud/{slug}/', CrudListView.as_view(**options), name=f'{slug}_list'),
        path(
            f'crud/{slug}/nuevo/',
            CrudCreateView.as_view(**options),
            name=f'{slug}_create',
        ),
        path(
            f'crud/{slug}/<int:pk>/',
            CrudDetailView.as_view(**options),
            name=f'{slug}_detail',
        ),
        path(
            f'crud/{slug}/<int:pk>/editar/',
            CrudUpdateView.as_view(**options),
            name=f'{slug}_update',
        ),
        path(
            f'crud/{slug}/<int:pk>/eliminar/',
            CrudDeleteView.as_view(**options),
            name=f'{slug}_delete',
        ),
    ]


# Trimestre: períodos de evaluación.
urlpatterns += crud_paths(Trimestre, 'trimestres')
# MetaMantenimiento: objetivos de mantenimiento.
urlpatterns += crud_paths(MetaMantenimiento, 'metas_crud')
# AsignacionMeta: meta asignada a un colaborador y trimestre.
urlpatterns += crud_paths(AsignacionMeta, 'asignaciones')
# Resultado: avance calculado de una meta.
urlpatterns += crud_paths(Resultado, 'resultados_crud')
