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


def calcular_cumplimiento(avance, meta_periodo):
	"""Calcula el porcentaje de avance respecto al valor objetivo."""
	if not meta_periodo:
		return 0
	return round(avance / meta_periodo * 100, 2)


def clasificar_semaforo(cumplimiento):
	"""Asigna un color según el porcentaje de cumplimiento alcanzado."""
	if cumplimiento >= 100:
		return 'verde'
	if cumplimiento >= 60:
		return 'ambar'
	return 'rojo'


def cargar_metas():
	"""Carga metas y combina sus resultados y relaciones asociadas."""
	metas = cargar_datos('metas.json')
	resultados = cargar_datos('resultados.json')
	periodos = cargar_datos('periodos.json')
	sedes = cargar_datos('sedes.json')
	responsables = cargar_datos('responsables.json')
	resultados_por_meta = {
		resultado['meta_id']: resultado for resultado in resultados
	}

	# Se indexan los resultados por meta para evitar recorrerlos repetidamente.
	metas_relacionadas = []
	for meta in metas:
		resultado = resultados_por_meta.get(meta['id'])
		if resultado is not None:
			# El semáforo se calcula una sola vez y queda disponible para las vistas.
			cumplimiento = calcular_cumplimiento(
				resultado['avance'],
				meta['valor_objetivo'],
			)
			resultado = {
				**resultado,
				'cumplimiento': cumplimiento,
				'semaforo': clasificar_semaforo(cumplimiento),
			}

		metas_relacionadas.append({
			**meta,
			'resultado': resultado,
			'periodo': buscar_por_id(periodos, meta.get('periodo_id')),
			'sede': buscar_por_id(sedes, meta.get('sede_id')),
			'responsable': buscar_por_id(responsables, meta.get('responsable_id')),
		})

	return metas_relacionadas


def inicio(request):
	"""Renderiza la pagina inicial del modulo de resultados."""
	return render(request, 'resultados/inicio.html')


def lista_metas(request):
	"""Muestra todas las metas con su progreso y relaciones asociadas."""
	return render(
		request,
		'resultados/lista_metas.html',
		{'metas': cargar_metas()}
	)


def detalle_meta(request, pk):
	"""Muestra una meta concreta o responde con un error 404."""
	meta = buscar_por_id(cargar_metas(), pk)

	# Evita renderizar una página vacía cuando el identificador no existe.
	if meta is None:
		raise Http404("Meta no encontrada")

	return render(request, 'resultados/detalle_meta.html', {'meta': meta})


def informe_resumen(request):
	"""Construye el resumen general de cumplimiento de las metas."""
	metas = cargar_metas()
	# Cada grupo reúne las metas que comparten el color de su semáforo.
	semaforos = [
		{
			'nombre': nombre,
			'codigo': codigo,
			'metas': [
				meta for meta in metas
				if meta['resultado'] and meta['resultado']['semaforo'] == codigo
			],
		}
		for codigo, nombre in (
			('verde', 'Verde'),
			('ambar', 'Ámbar'),
			('rojo', 'Rojo'),
		)
	]
	for semaforo in semaforos:
		semaforo['cantidad'] = len(semaforo['metas'])
	# Solo se consideran metas con resultado para calcular el promedio.
	cumplimientos = [
		meta['resultado']['cumplimiento']
		for meta in metas
		if meta['resultado']
	]

	return render(
		request,
		'resultados/informe_resumen.html',
		{
			'metas': metas,
			'total_metas': len(metas),
			'promedio_cumplimiento': round(
				sum(cumplimientos) / len(cumplimientos), 2
			) if cumplimientos else 0,
			'semaforos': semaforos,
		}
	)


def resultado_responsable(request, pk):
	"""Muestra las metas asignadas a un responsable."""
	responsable = buscar_por_id(cargar_datos('responsables.json'), pk)

	# El responsable debe existir antes de consultar sus metas relacionadas.
	if responsable is None:
		raise Http404("Responsable no encontrado")

	metas = [meta for meta in cargar_metas() if meta['responsable_id'] == pk]
	return render(
		request,
		'resultados/resultado_responsable.html',
		{'responsable': responsable, 'metas': metas}
	)


def tablero_sede(request, pk):
	"""Muestra las metas asociadas a una sede educativa."""
	sede = buscar_por_id(cargar_datos('sedes.json'), pk)

	# La sede debe existir antes de consultar sus metas relacionadas.
	if sede is None:
		raise Http404("Sede no encontrada")

	metas = [meta for meta in cargar_metas() if meta['sede_id'] == pk]
	return render(
		request,
		'resultados/tablero_sede.html',
		{'sede': sede, 'metas': metas}
	)
