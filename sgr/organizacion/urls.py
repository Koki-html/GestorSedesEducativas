"""Rutas del modulo de organizacion."""

from django.urls import path
from . import views
from .models import (
    Cargo,
    ComiteSede,
    Espacio,
    HitoMantenimiento,
    ParticipacionComite,
    Rol,
    Sector,
    SedeEducativa,
    Solicitante,
    SubtipoServicio,
    TipoServicio,
    UsuarioColaborador,
)
from sgr.crud import (
    CrudCreateView,
    CrudDeleteView,
    CrudDetailView,
    CrudListView,
    CrudUpdateView,
)

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


def crud_paths(model, slug):
    """Construye las cinco operaciones CRUD para un modelo."""
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


# Sector: catálogo de sectores educativos.
urlpatterns += crud_paths(Sector, 'sectores')
# SedeEducativa: sedes, dirección, sector y encargado.
urlpatterns += crud_paths(SedeEducativa, 'sedes_crud')
# Cargo: catálogo de cargos de colaboradores.
urlpatterns += crud_paths(Cargo, 'cargos')
# Rol: roles vinculados a grupos de Django.
urlpatterns += crud_paths(Rol, 'roles')
# UsuarioColaborador: perfil laboral asociado a User.
urlpatterns += crud_paths(UsuarioColaborador, 'colaboradores')
# Solicitante: personas que ingresan solicitudes.
urlpatterns += crud_paths(Solicitante, 'solicitantes')
# ComiteSede: comités asociados a una sede y sector.
urlpatterns += crud_paths(ComiteSede, 'comites')
# ParticipacionComite: integrantes y cargos dentro de un comité.
urlpatterns += crud_paths(ParticipacionComite, 'participaciones')
# HitoMantenimiento: hitos preventivos y sus responsables.
urlpatterns += crud_paths(HitoMantenimiento, 'hitos')
# Espacio: espacios físicos de una sede.
urlpatterns += crud_paths(Espacio, 'espacios')
# TipoServicio: catálogo principal de servicios.
urlpatterns += crud_paths(TipoServicio, 'tipos_servicio')
# SubtipoServicio: catálogo dependiente de TipoServicio.
urlpatterns += crud_paths(SubtipoServicio, 'subtipos_servicio')