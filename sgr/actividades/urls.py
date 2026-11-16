"""Rutas del modulo de actividades."""

from django.urls import path
from . import views
from .models import (
    ActividadMantenimiento,
    EvidenciaMantenimiento,
    SolicitudMantenimiento,
)
from .views import (
    ActividadMantenimientoForm,
    EvidenciaMantenimientoForm,
    SolicitudMantenimientoForm,
)
from sgr.crud import (
    CrudCreateView,
    CrudDeleteView,
    CrudDetailView,
    CrudListView,
    CrudUpdateView,
)

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


def crud_paths(model, slug, form_class):
    """Construye las operaciones CRUD de un modelo de actividades."""
    options = {
        'model': model,
        'form_class': form_class,
        'crud_namespace': app_name,
        'crud_name': slug,
    }
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


# ActividadMantenimiento: acciones ejecutadas y su avance.
urlpatterns += crud_paths(
    ActividadMantenimiento,
    'actividades_crud',
    ActividadMantenimientoForm,
)
# SolicitudMantenimiento: solicitudes ingresadas por los solicitantes.
urlpatterns += crud_paths(
    SolicitudMantenimiento,
    'solicitudes',
    SolicitudMantenimientoForm,
)
# EvidenciaMantenimiento: respaldos asociados a actividades o solicitudes.
urlpatterns += crud_paths(
    EvidenciaMantenimiento,
    'evidencias_crud',
    EvidenciaMantenimientoForm,
)