from django.shortcuts import get_object_or_404, render

from .models import Compromiso


def inicio(request):
    """Renderiza la página inicial del módulo de agenda."""
    return render(request, 'agenda/inicio.html')


def lista_compromisos(request):
    """Muestra los compromisos con sus relaciones resueltas por el ORM."""
    compromisos = Compromiso.objects.select_related(
        'sede',
        'responsable',
    ).order_by('fecha_comprometida', 'pk')
    return render(
        request,
        'agenda/lista_compromisos.html',
        {'compromisos': compromisos},
    )


def detalle_compromiso(request, pk):
    """Muestra un compromiso concreto."""
    compromiso = get_object_or_404(
        Compromiso.objects.select_related('sede', 'responsable'),
        pk=pk,
    )
    return render(
        request,
        'agenda/detalle_compromiso.html',
        {'compromiso': compromiso},
    )


def resumen_agenda(request):
    """Muestra totales de compromisos agrupados por estado y prioridad."""
    compromisos = Compromiso.objects.select_related('sede', 'responsable')

    def agrupar(campo):
        grupos = {}
        for compromiso in compromisos:
            valor = getattr(compromiso, campo)
            grupos.setdefault(valor, []).append(compromiso)
        return [
            {
                'nombre': nombre,
                campo: nombre,
                'cantidad': len(registros),
                'compromisos': registros,
            }
            for nombre, registros in sorted(grupos.items())
        ]

    return render(
        request,
        'agenda/resumen_agenda.html',
        {
            'total': compromisos.count(),
            'estados': agrupar('estado'),
            'prioridades': agrupar('prioridad'),
        },
    )
