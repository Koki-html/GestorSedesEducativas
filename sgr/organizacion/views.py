from django.shortcuts import get_object_or_404, render

from .models import SedeEducativa, UsuarioColaborador


def inicio(request):
    """Renderiza la página inicial del módulo de organización."""
    return render(request, 'organizacion/inicio.html')


def lista_sedes(request):
    """Muestra las sedes educativas almacenadas en la base de datos."""
    sedes = SedeEducativa.objects.select_related('sector', 'encargado').order_by('nombre')
    return render(request, 'organizacion/lista_sedes.html', {'sedes': sedes})


def detalle_sede(request, pk):
    """Muestra el detalle de una sede educativa."""
    sede = get_object_or_404(
        SedeEducativa.objects.select_related('sector', 'encargado'),
        pk=pk,
    )
    return render(request, 'organizacion/detalle_sede.html', {'sede': sede})


def lista_responsables(request):
    """Muestra los colaboradores que pueden actuar como responsables."""
    responsables = UsuarioColaborador.objects.select_related(
        'cargo',
        'sede',
    ).prefetch_related('roles').order_by('apellidos', 'nombres')
    return render(
        request,
        'organizacion/lista_responsables.html',
        {'responsables': responsables},
    )


def detalle_responsable(request, pk):
    """Muestra el detalle de un colaborador responsable."""
    responsable = get_object_or_404(
        UsuarioColaborador.objects.select_related('cargo', 'sede'),
        pk=pk,
    )
    return render(
        request,
        'organizacion/detalle_responsable.html',
        {'responsable': responsable},
    )
