# Gestor de Sedes Educativas

Aplicación web desarrollada con Django para centralizar la gestión de sedes
educativas, espacios, colaboradores, solicitudes de mantenimiento, actividades,
evidencias, compromisos y resultados.

El proyecto fue desarrollado individualmente por el estudiante **Miguel
Burgos** para la asignatura **Programación Backend**, sección
**D-IEI-N4-P2-C2**, de **INACAP - La Serena**. Se utilizó inteligencia
artificial como herramienta de apoyo para generar datos, revisar código,
organizar el trabajo y redactar documentación. La revisión, integración y
validación final corresponden al autor del proyecto. El detalle se encuentra
en [`declaracion_de_uso_de_ia.md`](declaracion_de_uso_de_ia.md).

## Contenido

- [Características](#características)
- [Módulos](#módulos)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración de la base de datos](#configuración-de-la-base-de-datos)
- [Carga de datos iniciales](#carga-de-datos-iniciales)
- [Ejecución](#ejecución)
- [Rutas principales](#rutas-principales)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Modelo de datos](#modelo-de-datos)
- [Matriz CRUD](#matriz-crud)
- [Permisos y autenticación](#permisos-y-autenticación)
- [Estado actual y limitaciones](#estado-actual-y-limitaciones)
- [Seguridad](#seguridad)

## Características

- Panel web construido con Django y plantillas HTML.
- Persistencia en MySQL mediante el backend `mysqlclient`.
- Administración de catálogos y entidades mediante el panel de Django y vistas
  CRUD protegidas por autenticación y permisos.
- Inicio de sesión y cierre de sesión integrados con el sistema de usuarios de
  Django.
- Importación idempotente de datos iniciales desde archivos JSON.
- Seguimiento de actividades, solicitudes, evidencias, compromisos, metas,
  asignaciones y resultados.
- Paneles e informes organizados por sede, responsable y meta.

## Módulos

| Aplicación | Responsabilidad |
|---|---|
| `organizacion` | Sectores, sedes educativas, espacios, cargos, roles, colaboradores, solicitantes, comités y servicios. |
| `actividades` | Solicitudes de mantenimiento, actividades y evidencias. |
| `agenda` | Compromisos, responsables, fechas, prioridades y estados. |
| `resultados` | Trimestres, metas de mantenimiento, asignaciones y resultados. |

### Reglas de negocio representadas

- Las entidades se relacionan con sedes, sectores, colaboradores, servicios y
  trimestres según corresponda.
- Los catálogos y entidades principales utilizan códigos únicos cuando el
  modelo los requiere.
- Los estados se controlan mediante opciones como `activo`, `inactivo` y
  `terminado`.
- Las evidencias pueden asociarse a una actividad o a una solicitud y registrar
  autor, verificador, fecha, estado y observaciones.
- Las metas se asignan a colaboradores y trimestres mediante
  `AsignacionMeta`.
- El avance y el resultado se almacenan en los modelos de actividades y
  resultados para su consulta en los paneles.

## Requisitos

- Python 3.14 o una versión compatible con las dependencias del proyecto.
- MySQL en ejecución y una base de datos creada para la aplicación.
- `pip` y un entorno virtual recomendado.
- En Windows, los requisitos de compilación que `mysqlclient` pueda necesitar
  durante su instalación.

Las versiones declaradas actualmente están en
[`requirements.txt`](requirements.txt), incluyendo Django 6.1.1,
`mysqlclient` 2.3.0 y `python-dotenv` 1.2.4.

## Instalación

Desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

## Configuración de la base de datos

La configuración se lee desde un archivo `.env` ubicado en la raíz del
repositorio, al mismo nivel que `requirements.txt`. Este archivo está excluido
del control de versiones.

Crear `.env` con las siguientes variables:

```dotenv
DB_NAME=gestiondesedes
DB_USER=tu_usuario
DB_PASSWORD=tu_clave
DB_HOST=localhost
DB_PORT=3306
```

La base de datos `gestiondesedes` debe existir antes de ejecutar las
migraciones. Por ejemplo, desde el cliente de MySQL:

```sql
CREATE DATABASE gestiondesedes;
```

El proyecto utiliza MySQL en la configuración actual de
[`sgr/sgr/settings.py`](sgr/sgr/settings.py); el archivo `db.sqlite3` no es la
base configurada para esta instalación.

## Carga de datos iniciales

Aplicar las migraciones:

```powershell
python .\sgr\manage.py migrate
```

Importar los datos JSON:

```powershell
python .\sgr\manage.py importar_datos
```

El comando carga los archivos de [`sgr/data/`](sgr/data/) en el orden necesario
para respetar sus relaciones. Utiliza el identificador de cada registro y
`update_or_create`, por lo que puede ejecutarse nuevamente para actualizar los
datos sin duplicarlos.

Los archivos de datos incluyen catálogos, sedes, colaboradores, comités,
espacios, solicitudes, actividades, evidencias, compromisos, trimestres, metas,
asignaciones y resultados.

## Ejecución

Comprobar la configuración del proyecto:

```powershell
python .\sgr\manage.py check
```

Iniciar el servidor de desarrollo:

```powershell
python .\sgr\manage.py runserver
```

Abrir en el navegador:

- Sitio principal: <http://127.0.0.1:8000/>
- Inicio de sesión: <http://127.0.0.1:8000/login/>
- Panel administrativo: <http://127.0.0.1:8000/admin/>

Crear un usuario administrador para el panel:

```powershell
python .\sgr\manage.py createsuperuser
```

Para detener el servidor, presionar `Ctrl+C`.

## Rutas principales

| Ruta | Funcionalidad |
|---|---|
| `/` | Portada del sistema. |
| `/login/` y `/logout/` | Autenticación de usuarios. |
| `/admin/` | Panel administrativo de Django. |
| `/organizacion/` | Consulta de sedes y responsables, además de CRUD de organización. |
| `/actividades/` | Consulta de actividades y evidencias, además de CRUD de mantenimiento. |
| `/agenda/` | Consulta, resumen y CRUD de compromisos. |
| `/resultados/` | Metas, resultados, informes y tableros. |

Cada módulo también expone rutas CRUD bajo `/crud/`, por ejemplo:
`/organizacion/crud/sectores/` y
`/actividades/crud/actividades_crud/`.

## Estructura del proyecto

```text
GestorSedesEducativas/
├── .env                         Configuración local, no versionada
├── requirements.txt             Dependencias de Python
├── readme.MD                    Documentación del proyecto
├── cambios.md                   Registro de cambios
├── sgr/
│   ├── manage.py                Entrada para comandos Django
│   ├── sgr/
│   │   ├── settings.py          Configuración
│   │   ├── urls.py              Rutas principales
│   │   ├── views.py             Vista de inicio
│   │   ├── crud.py              Vistas CRUD reutilizables
│   │   ├── asgi.py              Punto de entrada ASGI
│   │   └── wsgi.py              Punto de entrada WSGI
│   ├── organizacion/            Aplicación de organización
│   ├── actividades/             Aplicación de mantenimiento
│   ├── agenda/                  Aplicación de compromisos
│   ├── resultados/              Aplicación de metas y resultados
│   ├── data/                    Datos iniciales en JSON
│   ├── templates/                Plantillas HTML
│   └── static/                  CSS e imágenes
└── .gitignore
```

Cada aplicación contiene sus modelos, vistas, rutas, administración,
migraciones y pruebas. Las plantillas y los recursos estáticos se encuentran
en las carpetas del proyecto Django (`sgr/templates/` y `sgr/static/`).

## Modelo de datos

Las entidades principales son:

- **Organización:** `Sector`, `SedeEducativa`, `Espacio`, `Cargo`, `Rol`,
  `UsuarioColaborador`, `Solicitante`, `ComiteSede`,
  `ParticipacionComite`, `HitoMantenimiento`, `TipoServicio` y
  `SubtipoServicio`.
- **Actividades:** `SolicitudMantenimiento`, `ActividadMantenimiento` y
  `EvidenciaMantenimiento`.
- **Agenda:** `Compromiso`.
- **Resultados:** `Trimestre`, `MetaMantenimiento`, `AsignacionMeta` y
  `Resultado`.

Los modelos se encuentran en `sgr/<aplicacion>/models.py` y sus cambios de
esquema se registran en las carpetas `migrations/`.

## Matriz CRUD

La siguiente matriz resume las operaciones disponibles mediante las vistas CRUD
del sistema. Todas las operaciones están protegidas por autenticación y por el
permiso Django correspondiente al modelo.

| Aplicación | Entidad | Ruta base CRUD | Crear | Leer | Actualizar | Eliminar |
|---|---|---|:---:|:---:|:---:|:---:|
| `organizacion` | `Sector` | `/organizacion/crud/sectores/` | Sí | Sí | Sí | Sí |
| `organizacion` | `SedeEducativa` | `/organizacion/crud/sedes_crud/` | Sí | Sí | Sí | Sí |
| `organizacion` | `Cargo` | `/organizacion/crud/cargos/` | Sí | Sí | Sí | Sí |
| `organizacion` | `Rol` | `/organizacion/crud/roles/` | Sí | Sí | Sí | Sí |
| `organizacion` | `UsuarioColaborador` | `/organizacion/crud/colaboradores/` | Sí | Sí | Sí | Sí |
| `organizacion` | `Solicitante` | `/organizacion/crud/solicitantes/` | Sí | Sí | Sí | Sí |
| `organizacion` | `ComiteSede` | `/organizacion/crud/comites/` | Sí | Sí | Sí | Sí |
| `organizacion` | `ParticipacionComite` | `/organizacion/crud/participaciones/` | Sí | Sí | Sí | Sí |
| `organizacion` | `HitoMantenimiento` | `/organizacion/crud/hitos/` | Sí | Sí | Sí | Sí |
| `organizacion` | `Espacio` | `/organizacion/crud/espacios/` | Sí | Sí | Sí | Sí |
| `organizacion` | `TipoServicio` | `/organizacion/crud/tipos_servicio/` | Sí | Sí | Sí | Sí |
| `organizacion` | `SubtipoServicio` | `/organizacion/crud/subtipos_servicio/` | Sí | Sí | Sí | Sí |
| `actividades` | `ActividadMantenimiento` | `/actividades/crud/actividades_crud/` | Sí | Sí | Sí | Sí |
| `actividades` | `SolicitudMantenimiento` | `/actividades/crud/solicitudes/` | Sí | Sí | Sí | Sí |
| `actividades` | `EvidenciaMantenimiento` | `/actividades/crud/evidencias_crud/` | Sí | Sí | Sí | Sí |
| `agenda` | `Compromiso` | `/agenda/crud/compromisos/` | Sí | Sí | Sí | Sí |
| `resultados` | `Trimestre` | `/resultados/crud/trimestres/` | Sí | Sí | Sí | Sí |
| `resultados` | `MetaMantenimiento` | `/resultados/crud/metas_crud/` | Sí | Sí | Sí | Sí |
| `resultados` | `AsignacionMeta` | `/resultados/crud/asignaciones/` | Sí | Sí | Sí | Sí |
| `resultados` | `Resultado` | `/resultados/crud/resultados_crud/` | Sí | Sí | Sí | Sí |

Cada ruta base dispone de las siguientes acciones:

- `.../`: listado.
- `.../nuevo/`: creación.
- `.../<id>/`: detalle.
- `.../<id>/editar/`: actualización.
- `.../<id>/eliminar/`: eliminación.

## Permisos y autenticación

Las vistas CRUD requieren un usuario autenticado y el permiso Django
correspondiente para ver, crear, modificar o eliminar cada modelo. Los roles
del dominio se relacionan con grupos de Django mediante el modelo `Rol`.

Después de crear un superusuario, los grupos, usuarios y permisos pueden
administrarse desde `/admin/`. El comando `importar_datos` también crea los
grupos asociados a los roles definidos en `sgr/data/roles.json`.

## Estado actual y limitaciones

El proyecto implementa una aplicación Django funcional con persistencia,
migraciones, importación de datos, autenticación, permisos CRUD, panel
administrativo, consultas y vistas de seguimiento.

Actualmente:

- No existe una API pública o documentación de endpoints REST.
- La configuración está orientada al desarrollo local.
- Los formularios y vistas están implementados con Django y plantillas; no se
  incluye un frontend separado.
- No se incluye un flujo de despliegue automatizado para producción.
- La configuración de producción debe definir una `SECRET_KEY` segura,
  desactivar `DEBUG` y establecer `ALLOWED_HOSTS` antes de publicar el sistema.

## Seguridad

- No subir `.env`, contraseñas ni claves privadas al repositorio.
- No usar credenciales reales en archivos JSON de datos o documentación.
- Crear usuarios y asignar permisos desde Django en lugar de compartir
  credenciales.

## Créditos y uso de IA

La declaración completa sobre el uso de inteligencia artificial está en
[`declaracion_de_uso_de_ia.md`](declaracion_de_uso_de_ia.md).
