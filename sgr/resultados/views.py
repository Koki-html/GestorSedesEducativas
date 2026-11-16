from django.shortcuts import get_object_or_404, render

from organizacion.models import SedeEducativa, UsuarioColaborador

from .models import AsignacionMeta, MetaMantenimiento


def calcular_cumplimiento(avance, meta_periodo):
    """Calcula el porcentaje de avance respecto al objetivo asignado."""
    if not meta_periodo:
        return 0
    return round(float(avance) / float(meta_periodo) * 100, 2)


def clasificar_semaforo(cumplimiento):
    """Asigna una categoría visual según el cumplimiento."""
    if cumplimiento >= 100:
        return 'verde'
    if cumplimiento >= 60:
        return 'ambar'
    return 'rojo'


def cargar_metas(asignaciones=None):
    """Combina metas, asignaciones y resultados para las plantillas."""
    metas = MetaMantenimiento.objects.select_related('tipo').prefetch_related(
        'asignaciones__colaborador__sede',
        'asignaciones__trimestre',
        'resultado',
    )
    if asignaciones is not None:
        metas = metas.filter(asignaciones__in=asignaciones).distinct()

    metas_relacionadas = []
    for meta in metas:
        asignacion = meta.asignaciones.select_related(
            'colaborador__sede',
            'trimestre',
        ).first()
        resultado = getattr(meta, 'resultado', None)
        cumplimiento = (
            calcular_cumplimiento(resultado.avance, asignacion.cantidad_objetivo)
            if resultado and asignacion
            else 0
        )
        resultado_contexto = None
        if resultado:
            resultado_contexto = {
                'avance': resultado.avance,
                'fecha_calculo': resultado.fecha_calculo,
                'cumplimiento': cumplimiento,
                'semaforo': clasificar_semaforo(cumplimiento),
            }

        metas_relacionadas.append({
            'id': meta.pk,
            'indicador': meta.nombre,
            'nombre': meta.nombre,
            'descripcion': meta.descripcion,
            'tipo': meta.tipo,
            'tipo_indicador': meta.tipo.nombre if meta.tipo else '',
            'requisito_evidencia': meta.requisito_evidencia,
            'valor_objetivo': asignacion.cantidad_objetivo if asignacion else None,
            'trimestre': asignacion.trimestre if asignacion else None,
            'responsable': asignacion.colaborador if asignacion else None,
            'sede': asignacion.colaborador.sede if asignacion else None,
            'resultado': resultado_contexto,
        })
    return metas_relacionadas


def inicio(request):
    """Renderiza la página inicial del módulo de resultados."""
    return render(request, 'resultados/inicio.html')


def lista_metas(request):
    """Muestra todas las metas con su progreso."""
    return render(
        request,
        'resultados/lista_metas.html',
        {'metas': cargar_metas()},
    )


def detalle_meta(request, pk):
    """Muestra una meta concreta."""
    meta = next((item for item in cargar_metas() if item['id'] == pk), None)
    if meta is None:
        return get_object_or_404(MetaMantenimiento, pk=pk)
    return render(request, 'resultados/detalle_meta.html', {'meta': meta})


def informe_resumen(request):
    """Construye el resumen general de cumplimiento."""
    metas = cargar_metas()
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
            'promedio_cumplimiento': (
                round(sum(cumplimientos) / len(cumplimientos), 2)
                if cumplimientos else 0
            ),
            'semaforos': semaforos,
        },
    )


def resultado_responsable(request, pk):
    """Muestra las metas asignadas a un colaborador."""
    responsable = get_object_or_404(
        UsuarioColaborador.objects.select_related('cargo', 'sede'),
        pk=pk,
    )
    asignaciones = AsignacionMeta.objects.filter(colaborador=responsable)
    return render(
        request,
        'resultados/resultado_responsable.html',
        {
            'responsable': responsable,
            'metas': cargar_metas(asignaciones),
        },
    )


def tablero_sede(request, pk):
    """Muestra las metas asignadas a colaboradores de una sede."""
    sede = get_object_or_404(SedeEducativa, pk=pk)
    asignaciones = AsignacionMeta.objects.filter(colaborador__sede=sede)
    return render(
        request,
        'resultados/tablero_sede.html',
        {
            'sede': sede,
            'metas': cargar_metas(asignaciones),
        },
    )
