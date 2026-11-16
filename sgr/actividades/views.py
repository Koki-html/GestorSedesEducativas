from django import forms
from django.shortcuts import get_object_or_404, render

from .models import (
    ActividadMantenimiento,
    EvidenciaMantenimiento,
    SolicitudMantenimiento,
)


class ActividadMantenimientoForm(forms.ModelForm):
    """Formulario CRUD de ActividadMantenimiento."""

    class Meta:
        model = ActividadMantenimiento
        fields = '__all__'


class SolicitudMantenimientoForm(forms.ModelForm):
    """Formulario CRUD de SolicitudMantenimiento."""

    class Meta:
        model = SolicitudMantenimiento
        fields = '__all__'


class EvidenciaMantenimientoForm(forms.ModelForm):
    """Formulario CRUD de EvidenciaMantenimiento."""

    class Meta:
        model = EvidenciaMantenimiento
        fields = '__all__'


def inicio(request):
    """Renderiza la página inicial del módulo de actividades."""
    return render(request, 'actividades/inicio.html')


def lista_actividades(request):
    """Muestra las actividades de mantenimiento."""
    actividades = ActividadMantenimiento.objects.select_related(
        'colaborador',
        'asignacion_meta',
        'hito',
        'tipo',
        'solicitante',
        'sector',
        'responsable',
    ).order_by('-fecha', '-pk')
    return render(
        request,
        'actividades/lista_actividades.html',
        {'actividades': actividades},
    )


def detalle_actividad(request, pk):
    """Muestra el detalle de una actividad de mantenimiento."""
    actividad = get_object_or_404(
        ActividadMantenimiento.objects.select_related(
            'colaborador',
            'asignacion_meta',
            'hito',
            'tipo',
            'solicitante',
            'sector',
            'responsable',
        ),
        pk=pk,
    )
    return render(
        request,
        'actividades/detalle_actividad.html',
        {'actividad': actividad},
    )


def lista_evidencias(request):
    """Muestra las evidencias de mantenimiento."""
    evidencias = EvidenciaMantenimiento.objects.select_related(
        'actividad',
        'solicitud',
        'autor',
        'verificador',
    ).order_by('-fecha', '-pk')
    return render(
        request,
        'actividades/lista_evidencias.html',
        {'evidencias': evidencias},
    )


def detalle_evidencia(request, pk):
    """Muestra el detalle de una evidencia."""
    evidencia = get_object_or_404(
        EvidenciaMantenimiento.objects.select_related(
            'actividad',
            'solicitud',
            'autor',
            'verificador',
        ),
        pk=pk,
    )
    return render(
        request,
        'actividades/detalle_evidencia.html',
        {'evidencia': evidencia},
    )


def evidence(request, pk):
    """Conserva la ruta histórica para abrir el detalle de la evidencia."""
    return detalle_evidencia(request, pk)
