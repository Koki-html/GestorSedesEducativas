# Registro de cambios

Historial de modificaciones realizadas en el proyecto **Gestor de Sedes
Educativas**.

> Los cambios realizados durante una tarea deben registrarse aquí. Los cambios
> hechos manualmente fuera de una tarea deben indicarse para poder documentarlos.

## Índice

- [2026-11-16](#2026-11-16)
- [2026-11-15](#2026-11-15)

---

## 2026-11-16

### Renombrado de metas de mantenimiento

**Archivos afectados**

- `sgr/resultados/models.py`
- `sgr/resultados/admin.py`
- `sgr/organizacion/management/commands/importar_datos.py`
- `sgr/resultados/migrations/0002_rename_meta_mantenimiento.py`

**Cambios**

- Se renombró el modelo `Meta` a `MetaMantenimiento`.
- Se actualizaron sus referencias en resultados, administración, importación de
  datos y migraciones.

**Motivo**

Identificar explícitamente las metas relacionadas con mantenimiento sin perder
los registros existentes.

### Consolidación de trimestres

**Archivos afectados**

- `sgr/resultados/models.py`
- `sgr/resultados/admin.py`
- `sgr/resultados/views.py`
- `sgr/templates/resultados/detalle_meta.html`
- `sgr/organizacion/management/commands/importar_datos.py`
- `sgr/resultados/migrations/0003_rename_periodo_trimestre.py`
- `readme.MD`

**Cambios**

- Se estableció `Trimestre` como nombre definitivo de la entidad.
- Se renombró la relación `MetaMantenimiento.periodo` a
  `MetaMantenimiento.trimestre`.
- Se actualizaron la administración, el importador, las vistas, la plantilla,
  la documentación y la migración de base de datos.

**Motivo**

Completar la transición desde `Periodo` a `Trimestre` sin perder los registros
existentes.

### Ampliación del modelo de datos

**Archivos afectados**

- `sgr/organizacion/models.py`
- `sgr/actividades/models.py`
- `sgr/agenda/models.py`
- `sgr/resultados/models.py`
- Archivos `admin.py` relacionados
- `sgr/organizacion/management/commands/importar_datos.py`

**Cambios**

- Se transcribieron y reorganizaron las entidades de organización, catálogos,
  personas, comités, mantenimiento, solicitudes, metas y trimestres.
- Se agregaron relaciones con usuarios y grupos de Django.
- Se incorporaron estados controlados, códigos únicos, validaciones y registros
  administrativos.

**Motivo**

Alinear el modelo de datos con los requisitos mínimos de catálogos, operación,
metas y seguridad del proyecto.

---

## 2026-11-15

### Reorganización de la organización

**Archivos afectados**

- `sgr/organizacion/models.py`

**Cambios**

- Se agregó `Sector`.
- Se renombró `Sede` como `SedeEducativa`.
- Se actualizó la relación de `Espacio` con las sedes.
- Se agregaron `Cargo` y `Rol`.
- Se renombró `Responsable` como `UsuarioColaborador`.
- Se vincularon cargos y roles mediante claves foráneas.
- Se agregaron `TipoServicio` y `SubTipoServicio`.
- Se corrigió `max_lenght` por `max_length`.
- Se normalizaron las indentaciones.

**Motivo**

Incorporar entidades y relaciones para representar sectores, colaboradores,
cargos, roles y clasificación de servicios.

### Renombrado de actividades y evidencias

**Archivos afectados**

- `sgr/actividades/models.py`
- `sgr/actividades/admin.py`
- `sgr/organizacion/management/commands/importar_datos.py`
- `sgr/actividades/migrations/0003_rename_actividad_evidencia_mantenimiento.py`

**Cambios**

- Se renombró `Actividad` como `ActividadMantenimiento`.
- Se renombró `Evidencia` como `EvidenciaMantenimiento`.
- Se actualizaron los registros administrativos, el importador y la migración.

**Motivo**

Diferenciar explícitamente las entidades relacionadas con el mantenimiento.
