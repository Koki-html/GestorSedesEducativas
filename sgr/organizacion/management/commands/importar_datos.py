import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db import transaction

from actividades.models import (
    ActividadMantenimiento,
    EvidenciaMantenimiento,
    SolicitudMantenimiento,
)
from agenda.models import Compromiso
from organizacion.models import (
    Cargo,
    ComiteSede,
    Espacio,
    HitoMantenimiento,
    ParticipacionComite,
    Rol,
    Sector,
    SedeEducativa,
    Solicitante,
    SubtipoServicio,
    TipoServicio,
    UsuarioColaborador,
)
from resultados.models import AsignacionMeta, MetaMantenimiento, Resultado, Trimestre


class Command(BaseCommand):
    help = 'Importa los datos JSON de sgr/data a la base de datos.'

    def cargar_json(self, nombre_archivo):
        ruta = Path(settings.BASE_DIR) / 'data' / nombre_archivo
        with ruta.open(encoding='utf-8') as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, list):
            raise ValueError(f'{nombre_archivo} debe contener una lista JSON')
        return datos

    def guardar(self, modelo, registro, valores):
        objeto, creado = modelo.objects.update_or_create(
            pk=registro['id'],
            defaults=valores,
        )
        return objeto, creado

    @transaction.atomic
    def handle(self, *args, **options):
        sectores = self.cargar_json('sectores.json')
        cargos = self.cargar_json('cargos.json')
        roles = self.cargar_json('roles.json')
        tipos = self.cargar_json('tipos_servicio.json')
        subtipos = self.cargar_json('subtipos_servicio.json')
        trimestres = self.cargar_json('trimestres.json')
        sedes = self.cargar_json('sedes.json')
        colaboradores = self.cargar_json('usuarios_colaboradores.json')
        solicitantes = self.cargar_json('solicitantes.json')
        comites = self.cargar_json('comites_sede.json')
        participaciones = self.cargar_json('participaciones_comite.json')
        hitos = self.cargar_json('hitos_mantenimiento.json')
        metas = self.cargar_json('metas.json')
        asignaciones = self.cargar_json('asignaciones_metas.json')
        espacios = self.cargar_json('espacios.json')
        solicitudes = self.cargar_json('solicitudes_mantenimiento.json')
        actividades = self.cargar_json('actividades.json')
        evidencias = self.cargar_json('evidencias.json')
        compromisos = self.cargar_json('compromisos.json')
        resultados = self.cargar_json('resultados.json')

        for registro in sectores:
            self.guardar(Sector, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'descripcion': registro.get('descripcion', ''),
                'estado': registro['estado'],
            })
        for registro in cargos:
            self.guardar(Cargo, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'descripcion': registro.get('descripcion', ''),
                'estado': registro['estado'],
            })
        for registro in roles:
            grupo, _ = Group.objects.get_or_create(name=registro['grupo'])
            self.guardar(Rol, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'grupo': grupo,
                'estado': registro['estado'],
            })
        for registro in tipos:
            self.guardar(TipoServicio, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'descripcion': registro.get('descripcion', ''),
                'estado': registro['estado'],
            })
        for registro in subtipos:
            self.guardar(SubtipoServicio, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'tipo_id': registro['tipo_id'],
                'estado': registro['estado'],
            })
        for registro in trimestres:
            self.guardar(Trimestre, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'anio': registro['anio'],
                'numero': registro['numero'],
                'fecha_inicio': registro['fecha_inicio'],
                'fecha_termino': registro['fecha_termino'],
                'estado': registro['estado'],
            })
        for registro in sedes:
            self.guardar(SedeEducativa, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'direccion': registro['direccion'],
                'sector_id': registro['sector_id'],
                'encargado_id': registro.get('encargado_id'),
                'estado': registro['estado'],
            })
        for registro in colaboradores:
            user_data = registro['usuario']
            usuario, _ = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                },
            )
            usuario.email = user_data['email']
            usuario.first_name = user_data['first_name']
            usuario.last_name = user_data['last_name']
            usuario.save(update_fields=['email', 'first_name', 'last_name'])
            colaborador, _ = self.guardar(UsuarioColaborador, registro, {
                'usuario': usuario,
                'nombres': registro['nombres'],
                'apellidos': registro['apellidos'],
                'rut': registro['rut'],
                'correo': registro['correo'],
                'cargo_id': registro['cargo_id'],
                'sede_id': registro['sede_id'],
                'estado': registro['estado'],
            })
            colaborador.roles.set(registro.get('roles_ids', []))
        for registro in sedes:
            if registro.get('encargado_id'):
                SedeEducativa.objects.filter(pk=registro['id']).update(
                    encargado_id=registro['encargado_id']
                )
        for registro in solicitantes:
            self.guardar(Solicitante, registro, {
                'rut': registro['rut'],
                'nombres': registro['nombres'],
                'apellidos': registro['apellidos'],
                'telefono': registro['telefono'],
                'correo': registro['correo'],
                'direccion': registro['direccion'],
                'sector_id': registro['sector_id'],
                'estado': registro['estado'],
            })
        for registro in comites:
            self.guardar(ComiteSede, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'direccion': registro['direccion'],
                'sede_id': registro['sede_id'],
                'sector_id': registro['sector_id'],
                'fecha_constitucion': registro['fecha_constitucion'],
                'estado': registro['estado'],
            })
        for registro in participaciones:
            self.guardar(ParticipacionComite, registro, {
                'solicitante_id': registro['solicitante_id'],
                'comite_id': registro['comite_id'],
                'es_coordinador': registro['es_coordinador'],
                'cargo_id': registro['cargo_id'],
                'fecha_incorporacion': registro['fecha_incorporacion'],
                'estado': registro['estado'],
            })
        for registro in hitos:
            hito, _ = self.guardar(HitoMantenimiento, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'descripcion': registro['descripcion'],
                'periodicidad': registro['periodicidad'],
                'fecha_inicio': registro['fecha_inicio'],
                'fecha_termino': registro.get('fecha_termino'),
                'sede_id': registro['sede_id'],
                'sector_id': registro['sector_id'],
                'estado': registro['estado'],
            })
            hito.responsables.set(registro.get('responsables_ids', []))
        for registro in metas:
            self.guardar(MetaMantenimiento, registro, {
                'codigo': registro['codigo'],
                'nombre': registro['nombre'],
                'descripcion': registro['descripcion'],
                'tipo_id': registro['tipo_id'],
                'unidad_medida': registro['unidad_medida'],
                'requisito_evidencia': registro['requisito_evidencia'],
                'estado': registro['estado'],
            })
        for registro in asignaciones:
            self.guardar(AsignacionMeta, registro, {
                'colaborador_id': registro['colaborador_id'],
                'meta_id': registro['meta_id'],
                'trimestre_id': registro['trimestre_id'],
                'cantidad_objetivo': registro['cantidad_objetivo'],
                'ponderacion': registro['ponderacion'],
                'fecha_asignacion': registro['fecha_asignacion'],
                'observacion': registro.get('observacion', ''),
                'estado': registro['estado'],
            })
        for registro in espacios:
            self.guardar(Espacio, registro, {
                'sede_id': registro['sede_id'],
                'nombre': registro['nombre'],
                'tipo': registro['tipo'],
                'ubicacion': registro['ubicacion'],
                'estado': registro['estado'],
            })
        for registro in solicitudes:
            self.guardar(SolicitudMantenimiento, registro, {
                'fecha_ingreso': registro['fecha_ingreso'],
                'fecha_atencion': registro.get('fecha_atencion'),
                'solicitante_id': registro['solicitante_id'],
                'tipo_id': registro['tipo_id'],
                'subtipo_id': registro['subtipo_id'],
                'asignacion_meta_id': registro['asignacion_meta_id'],
                'visita': registro.get('visita', ''),
                'actuaciones': registro.get('actuaciones', ''),
                'derivacion': registro.get('derivacion', ''),
                'informe': registro.get('informe', ''),
                'solucion': registro.get('solucion', ''),
                'resultado': registro.get('resultado', ''),
                'estado': registro['estado'],
            })
        for registro in actividades:
            self.guardar(ActividadMantenimiento, registro, {
                'fecha': registro['fecha'],
                'colaborador_id': registro['colaborador_id'],
                'asignacion_meta_id': registro['asignacion_meta_id'],
                'hito_id': registro.get('hito_id'),
                'tipo_id': registro['tipo_id'],
                'descripcion': registro['descripcion'],
                'origen': registro['origen'],
                'solicitante_id': registro['solicitante_id'],
                'sector_id': registro['sector_id'],
                'responsable_id': registro['responsable_id'],
                'fecha_compromiso': registro.get('fecha_compromiso'),
                'apoyo': registro.get('apoyo', ''),
                'avance': registro.get('avance', 0),
                'estado': registro['estado'],
                'resultado': registro.get('resultado', ''),
            })
        for registro in evidencias:
            self.guardar(EvidenciaMantenimiento, registro, {
                'codigo': registro['codigo'],
                'actividad_id': registro.get('actividad_id'),
                'solicitud_id': registro.get('solicitud_id'),
                'tipo': registro['tipo'],
                'ubicacion_referencia': registro['ubicacion_referencia'],
                'autor_id': registro['autor_id'],
                'fecha': registro['fecha'],
                'estado': registro['estado'],
                'observacion': registro.get('observacion', ''),
                'verificador_id': registro.get('verificador_id'),
            })
        for registro in compromisos:
            self.guardar(Compromiso, registro, {
                'origen': registro['origen'],
                'sede_id': registro['sede_id'],
                'responsable_id': registro['responsable_id'],
                'fecha_comprometida': registro['fecha_comprometida'],
                'prioridad': registro['prioridad'],
                'estado': registro['estado'],
            })
        for registro in resultados:
            self.guardar(Resultado, registro, {
                'meta_id': registro['meta_id'],
                'avance': registro['avance'],
                'fecha_calculo': registro['fecha_calculo'],
            })

        self.stdout.write(self.style.SUCCESS('Datos JSON importados correctamente.'))
