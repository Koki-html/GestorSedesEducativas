import json
from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

def cargar_datos(nombre_archivo):
    """Carga una lista de Registros desde la carpeta data del proyecto."""
    # BASE_DIR apunta a la carpeta del proyecto; desde allí se ubican los
    # archivos JSON compartidos por las aplicaciones."""
    ruta = Path(settings.BASE_DIR) / 'data' / nombre_archivo
    contenido = ruta.read_text(encoding='utf-8').strip()

    # Un archivo vacío representa una colección sin registros.
    if not contenido:
        return []

    datos = json.loads(contenido)

    # Las vistas esperan recorrer una lista, por eso se valida la estructura
    # antes de devolver los datos.
    if not isinstance(datos, list):
        raise ValueError(f'{nombre_archivo} debe contener una lista JSON')
    return datos

def buscar_por_id(actividades, pk):
    """Busca una actividad por su identificador."""
    return next((actividad for actividad in actividades if actividad.get('id') == pk), None)

def inicio(request):
    """Renderiza la pagina inicial del modulo de actividades."""
    # Esta vista solo necesita cargar la plantilla del módulo.
    return render(
        request,
        'actividades/inicio.html'
        )
    
def lista_actividades(request):
    """Muestra las actividades almacenadas en actividades.json."""
    # Se cargan todas las actividades y se envían a la plantilla con la clave
    # esperada por el contexto HTML.
    actividades = cargar_datos('actividades.json')
    return render(
        request,
        'actividades/lista_actividades.html',
        {'actividades': actividades}
    )
    
def detalle_actividad(request, pk):
    """Muestra el detalle de una actividad o responde con un error 404."""
    actividades = cargar_datos('actividades.json')
    sedes = cargar_datos('sedes.json')
    espacios = cargar_datos('espacios.json')
    responsables = cargar_datos('responsables.json')
    actividad = buscar_por_id(actividades, pk)

    # Evita renderizar una página vacía cuando el identificador no existe.
    if actividad is None:
        raise Http404("Actividad no encontrada")

    sede = buscar_por_id(sedes, actividad['sede_id'])
    espacio = buscar_por_id(espacios, actividad['espacio_id'])
    responsable = buscar_por_id(responsables, actividad['responsable_id'])

    return render(
        request,
        'actividades/detalle_actividad.html',
        {
            'actividad': actividad,
            'sede': sede,
            'espacio': espacio,
            'responsable': responsable,
        }
    )
    
def lista_evidencias(request):
    """Muestra las evidencias almacenadas en evidencias.json."""
    evidencias = cargar_datos('evidencias.json')
    return render(
        request,
        'actividades/lista_evidencias.html',
        {'evidencias': evidencias}
    )

def detalle_evidencia(request, pk):
    """Muestra el detalle de una evidencia o responde con un error 404."""
    evidencias = cargar_datos('evidencias.json')
    evidencia = buscar_por_id(evidencias, pk)

    # Evita renderizar una página vacía cuando el identificador no existe.
    if evidencia is None:
        raise Http404("Evidencia no encontrada")

    return render(
        request,
        'actividades/detalle_evidencia.html',
        {'evidencia': evidencia}
    )

def evidence(request, pk):
    """Muestra el archivo de evidencia guardado en evidencias.json."""
    evidencias = cargar_datos('evidencias.json')
    evidencia = buscar_por_id(evidencias, pk)

    if evidencia is None:
        raise Http404("Evidencia no encontrada")

    return render(
        request,
        'actividades/evidence.html',
        {'evidencia': evidencia}
    )