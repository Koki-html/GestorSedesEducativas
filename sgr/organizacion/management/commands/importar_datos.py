import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from actividades.models import Actividad, Evidencia
from agenda.models import Compromiso
from organizacion.models import Espacio, Responsable, Sede
from resultados.models import Meta, Periodo, Resultado


class Command(BaseCommand):
    """Importa los registros JSON del proyecto a la base de datos Django."""

    help = 'Importa todos los archivos JSON de sgr/data a la base de datos.'

    def cargar_json(self, nombre_archivo):
        """Lee un archivo JSON y devuelve su lista de registros."""
        ruta = Path(settings.BASE_DIR) / 'data' / nombre_archivo
        with ruta.open(encoding='utf-8') as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError(f'{nombre_archivo} debe contener una lista JSON')
        return datos

    def guardar_registros(
        self,
        modelo,
        registros,
        preparar_valores,
        clave_id='id',
    ):
        """Crea o actualiza registros conservando el ID de cada JSON."""
        creados = 0
        actualizados = 0
        for registro in registros:
            _, creado = modelo.objects.update_or_create(
                pk=registro[clave_id],
                defaults=preparar_valores(registro),
            )
            if creado:
                creados += 1
            else:
                actualizados += 1
        return creados, actualizados

    @transaction.atomic
    def handle(self, *args, **options):
        """Importa los datos en una transacción para evitar cargas parciales."""
        sedes = self.cargar_json('sedes.json')
        espacios = self.cargar_json('espacios.json')
        responsables = self.cargar_json('responsables.json')
        actividades = self.cargar_json('actividades.json')
        evidencias = self.cargar_json('evidencias.json')
        compromisos = self.cargar_json('compromisos.json')
        periodos = self.cargar_json('periodos.json')
        metas = self.cargar_json('metas.json')
        resultados = self.cargar_json('resultados.json')

        resumen = []

        resumen.append(('Sedes', self.guardar_registros(
            Sede,
            sedes,
            lambda registro: {
                'nombre': registro['nombre'],
                'direccion': registro['direccion'],
                'comuna': registro['comuna'],
                'encargado': registro['encargado'],
                'estado': registro['estado'],
            },
        )))
        resumen.append(('Espacios', self.guardar_registros(
            Espacio,
            espacios,
            lambda registro: {
                'sede_id': registro['sede_id'],
                'nombre': registro['nombre'],
                'tipo': registro['tipo'],
                'ubicacion': registro['ubicacion'],
                'estado': registro['estado'],
            },
        )))
        resumen.append(('Responsables', self.guardar_registros(
            Responsable,
            responsables,
            lambda registro: {
                'nombre': registro['nombre'],
                'cargo': registro['cargo'],
                'especialidad': registro['especialidad'],
                'sede_id': registro['sede_id'],
                'activo': registro['activo'],
            },
        )))
        resumen.append(('Actividades', self.guardar_registros(
            Actividad,
            actividades,
            lambda registro: {
                'fecha': registro['fecha'],
                'sede_id': registro['sede_id'],
                'espacio_id': registro['espacio_id'],
                'tipo': registro['tipo'],
                'descripcion': registro['descripcion'],
                'accion': registro['accion'],
                'responsable_id': registro['responsable_id'],
                'estado': registro['estado'],
                'aprobada': registro['aprobada'],
                'corregida': registro.get('corregida'),
                'avance_aprobado': registro.get('avance_aprobado'),
            },
        )))
        resumen.append(('Evidencias', self.guardar_registros(
            Evidencia,
            evidencias,
            lambda registro: {
                'actividad_id': registro['actividad_id'],
                'codigo': registro['codigo'],
                'archivo_url': registro['archivo_url'],
                'fecha': registro['fecha'],
                'estado': registro['estado'],
                'observacion': registro['observacion'],
            },
        )))
        resumen.append(('Compromisos', self.guardar_registros(
            Compromiso,
            compromisos,
            lambda registro: {
                'origen': registro['origen'],
                'sede_id': registro['sede_id'],
                'responsable_id': registro['responsable_id'],
                'fecha_comprometida': registro['fecha_comprometida'],
                'prioridad': registro['prioridad'],
                'estado': registro['estado'],
            },
        )))
        resumen.append(('Períodos', self.guardar_registros(
            Periodo,
            periodos,
            lambda registro: {
                'fecha_inicio': registro['fecha_inicio'],
                'fecha_termino': registro['fecha_termino'],
                'estado': registro['estado'],
            },
        )))
        resumen.append(('Metas', self.guardar_registros(
            Meta,
            metas,
            lambda registro: {
                'periodo_id': registro['periodo_id'],
                'responsable_id': registro.get('responsable_id'),
                'sede_id': registro.get('sede_id'),
                'indicador': registro['indicador'],
                'valor_objetivo': registro['valor_objetivo'],
                'ponderacion': registro['ponderacion'],
            },
        )))
        resumen.append(('Resultados', self.guardar_registros(
            Resultado,
            resultados,
            lambda registro: {
                'meta_id': registro['meta_id'],
                'avance': registro['avance'],
                'fecha_calculo': registro['fecha_calculo'],
            },
            clave_id='meta_id',
        )))

        for nombre, (creados, actualizados) in resumen:
            self.stdout.write(
                self.style.SUCCESS(
                    f'{nombre}: {creados} creados, {actualizados} actualizados.'
                )
            )
