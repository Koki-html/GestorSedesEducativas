import json
from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from django.http import Http404


def cargar_datos(nombre_archivo):
    """Carga una lista de registros desde la carpeta data del proyecto."""
    # BASE_DIR apunta a la carpeta del proyecto; desde allí se ubican los
    # archivos JSON compartidos por las aplicaciones.
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


def buscar_por_id(registros, pk):
    """Busca un registro por su identificador."""
    # next devuelve el primer registro coincidente o None si no existe.
    return next((registro for registro in registros if registro.get('id') == pk), None)


def inicio(request):
    """Renderiza la pagina inicial del modulo de organizacion."""
    # Esta vista solo necesita cargar la plantilla del módulo.
    return render(
        request,
        'organizacion/inicio.html'
    )

def lista_sedes(request):
    """Muestra las sedes educativas almacenadas en sedes.json."""
    # Se cargan todas las sedes y se envían a la plantilla con la clave
    # esperada por el contexto HTML.
    sedes = cargar_datos('sedes.json')
    return render(
        request,
        'organizacion/lista_sedes.html',
        {'sedes': sedes}
    )

def detalle_sede(request, pk):
    """Muestra el detalle de una sede o responde con un error 404."""
    sedes = cargar_datos('sedes.json')
    sede = buscar_por_id(sedes, pk)

    # Evita renderizar una página vacía cuando el identificador no existe.
    if sede is None:
        raise Http404("Sede no encontrada")
    return render(request, 'organizacion/detalle_sede.html', {'sede': sede})

def lista_responsables(request):
    """Muestra todos los responsables almacenados en responsables.json."""
    responsables = cargar_datos('responsables.json')
    return render(
        request,
        'organizacion/lista_responsables.html',
        {'responsables': responsables}
    )

def detalle_responsable(request, pk):
    """Muestra el detalle de un responsable o responde con un error 404."""
    responsables = cargar_datos('responsables.json')
    sedes = cargar_datos('sedes.json')
    responsable = buscar_por_id(responsables, pk)
    sede = buscar_por_id(sedes, responsable['sede_id'])
    
    # El responsable solicitado puede no existir en el archivo JSON.
    if responsable is None:
        raise Http404("Responsable no encontrado")
    return render(
        request,
        'organizacion/detalle_responsable.html',
        {'responsable': responsable, 'sede': sede}
    )