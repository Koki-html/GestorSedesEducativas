from django.shortcuts import render

def inicio(request):
    """Muestra la portada con los modulos disponibles del sistema."""
    # Esta lista es temporal y alimenta los enlaces que aparecen en la plantilla.
    aplicaciones = [
        {
            'nombre': 'Organización',
            'ruta': '/organizacion/'
        },
        {
            'nombre': 'Actividades',
            'ruta': '/actividades/'
        },
        {
            'nombre': 'Agenda',
            'ruta': '/agenda/'
        },
        {
            'nombre': 'Resultados',
            'ruta': '/resultados/'
        }

    ]
    # render combina la plantilla con el contexto y devuelve una respuesta HTTP.
    return render(
        request, 
        'inicio.html', 
        {'aplicaciones': aplicaciones}
    )