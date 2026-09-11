import json
from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.shortcuts import render


def cargar_datos(nombre_archivo):
	"""Carga una lista de registros desde la carpeta data del proyecto."""
	ruta = Path(settings.BASE_DIR) / 'data' / nombre_archivo
	contenido = ruta.read_text(encoding='utf-8').strip()
	return json.loads(contenido) if contenido else []


def buscar_por_id(registros, pk):
	"""Busca un registro por su identificador y devuelve None si no existe."""
	return next((registro for registro in registros if registro.get('id') == pk), None)


def cargar_relaciones(compromisos):
	"""Agrega a cada compromiso los datos de su sede y responsable."""
	sedes = cargar_datos('sedes.json')
	responsables = cargar_datos('responsables.json')

	# Se conservan los datos originales y se anexan las relaciones necesarias
	# para que las plantillas no tengan que resolver identificadores.
	return [
		{
			**compromiso,
			'sede': buscar_por_id(sedes, compromiso.get('sede_id')),
			'responsable': buscar_por_id(responsables, compromiso.get('responsable_id')),
		}
		for compromiso in compromisos
	]

def inicio(request):
	"""Renderiza la pagina inicial del modulo de agenda."""
	return render(
		request,
		'agenda/inicio.html'
	)

def lista_compromisos(request):
	"""Muestra todos los compromisos con sus relaciones resueltas."""
	compromisos = cargar_relaciones(cargar_datos('compromisos.json'))
	return render(
		request,
		'agenda/lista_compromisos.html',
		{'compromisos': compromisos}
	)

def detalle_compromiso(request, pk):
	"""Muestra un compromiso concreto o responde con un error 404."""
	compromisos = cargar_relaciones(cargar_datos('compromisos.json'))
	compromiso = buscar_por_id(compromisos, pk)

	# Evita renderizar una página vacía cuando el identificador no existe.
	if compromiso is None:
		raise Http404("Compromiso no encontrado")

	return render(
		request,
		'agenda/detalle_compromiso.html',
		{'compromiso': compromiso}
	)

def agrupar_compromisos(compromisos, campo):
	"""Agrupa compromisos por un campo y calcula la cantidad de cada grupo."""
	categorias = {}
	for compromiso in compromisos:
		nombre = compromiso[campo]
		categorias.setdefault(nombre, []).append(compromiso)

	# La lista resultante tiene la estructura que utiliza el resumen de agenda.
	return [
		{
			'nombre': nombre,
			'cantidad': len(registros),
			'compromisos': registros,
		}
		for nombre, registros in categorias.items()
	]

def resumen_agenda(request):
	"""Muestra totales de compromisos agrupados por estado y prioridad."""
	compromisos = cargar_relaciones(cargar_datos('compromisos.json'))
	prioridades = agrupar_compromisos(compromisos, 'prioridad')
	# Define un orden estable para presentar las prioridades de mayor a menor
	# urgencia, incluso cuando los datos contienen una prioridad desconocida.
	prioridad_orden = {'critica': 0, 'crítica': 0, 'alta': 1, 'media': 2, 'baja': 3}
	prioridades.sort(
		key=lambda prioridad: prioridad_orden.get(
			prioridad['nombre'].lower(),
			len(prioridad_orden),
		)
	)

	return render(
		request,
		'agenda/resumen_agenda.html',
		{
			'total': len(compromisos),
			'estados': agrupar_compromisos(compromisos, 'estado'),
			'prioridades': prioridades,
		}
	)
