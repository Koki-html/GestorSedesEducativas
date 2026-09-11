## Proyecto de Backend
---


* Este proyecto fue desarrollado por el estudiante ***Miguel Burgos*** de manera individual para la asignatura ***Programación Backend***, sección ***D-IEI-N4-P2-C2***, cursada en ***INACAP - La Serena*** y dictada por la profesora ***Mariavictoria***.

* El contenido en su totalidad fue pensado, programado y depurado por el estudiante, con apoyo de la inteligencia artificial en procesos como:
    * Generación de datos en archivos JSON.
    * Optimización del flujo de trabajo, como transcribir código o realizar ajustes grandes.
    * Organización del trabajo, como generar un paso a paso para avanzar e ir registrando el progreso.
    * Apoyo para comentar el código.

<small> Información del Proyecto </small>
Todo este trabajo fue desarrollado a partir del siguiente caso ficticio:

### 1. Contexto y problema
Donde EducaNorte administra seis sedes educativas con salas, laboratorios, oficinas y espacios comunes. El mantenimiento preventivo y correctivo se informa actualmente mediante mensajes, llamadas y planillas independientes. Esto dificulta conocer qué ocurrió, quién es responsable, qué evidencia existe, cuáles compromisos están pendientes y qué sedes presentan mejores tiempos de respuesta.
La coordinación central requiere un sistema web que permita organizar las sedes y sus responsables, registrar actividades de mantenimiento con evidencia, programar compromisos y medir resultados mediante metas e indicadores.

### 2. Objetivo general
Centralizar el registro, seguimiento, verificación y medición del mantenimiento de las sedes educativas, entregando información comparable por responsable, sede, tipo de trabajo y período.

### 3. Actores

| Actor | Responsabilidad |
|---|---|
| `Administrador` | Mantiene sedes, responsables, cargos, áreas y parámetros generales. |
| `Coordinador central` | Supervisa solicitudes, compromisos, indicadores y resultados de todas las sedes. |
| `Encargado de sede` | Registra necesidades, consulta trabajos y revisa compromisos de su sede. |
| `Técnico o responsable` | Registra actividades realizadas, avances y evidencias. |
| `Verificador` | Aprueba, rechaza o solicita corrección de evidencias. |
| `Usuario de consulta` | Consulta paneles e informes sin modificar información. |

### 4. Aplicaciones del proyecto

| Aplicación | Responsabilidad |
|---|---|
| `organizacion` | Sedes, espacios, responsables, cargos y áreas de mantenimiento. |
| `actividades` | Actividades realizadas, servicios, evidencias y validaciones. |
| `agenda` | Compromisos programados, responsables, plazos, estados y observaciones. |
| `resultados` | Períodos, metas, asignaciones, cumplimiento, semáforos, paneles e informes. |

A partir de esto y de algunas reglas adicionales se desarrolla el sistema, buscando cumplir con lo solicitado en estos puntos.

### 5. Reglas de negocio

- Cada actividad y compromiso pertenece a una sede y debe identificar un responsable.
- La prioridad puede ser baja, media, alta o crítica.
- Los compromisos utilizan los estados Ingresado, Pendiente, En proceso y Realizado.
- Una evidencia conserva código, actividad asociada, fecha, estado y observación de revisión.
- Una actividad rechazada no aumenta el avance hasta ser corregida y aprobada.
- **Cumplimiento (%) = avance aprobado / meta del período × 100.**
- **Semáforo:** verde si alcanza lo esperado, ámbar si está entre 60 % y menos de lo esperado, y rojo si está bajo 60 %.

### 6. Progreso del proyecto

| Unidad | Producto esperado | Tecnología o crecimiento |
|---|---|---|
| Unidad 1 | Prototipo de consulta con las cuatro aplicaciones, vistas, plantillas, CSS y JSON. | Sin modelos ni base de datos. |
| Unidad 2 | Persistencia de sedes, responsables, actividades, agenda, metas y resultados. | Modelos, relaciones, migraciones, MySQL y panel de administración. |
| Unidad 3 | Operación del sistema por roles. | CRUD, formularios, validaciones, autenticación y permisos. |
| Unidad 4 | Intercambio y consulta externa. | API, endpoints, pruebas y documentación. |

### 7. Aclaraciones y Limitaciones

Los archivos `db.sqlite3` y `models.py` son archivos autogenerados por Django, pero no se utilizan en el funcionamiento del proyecto.
En el momento actual de la evaluación (Unidad 1), esta versión no utiliza las siguientes tecnologías:
* Permisos
* API
* Autenticación
* CRUD
* Bases de Datos

### 8. Estructura del Proyecto

Esta es la estructura principal del proyecto y de los archivos trabajados:
```text
📦 GestorSedesEducativas
└── 📁 sgr/                              Proyecto Django
    ├── 📁 sgr/                           Configuración utilizada
    │   ├── ⚙️ settings.py                Configuración del proyecto
    │   ├── 🔗 urls.py                    Rutas principales
    │   └── 👁️ views.py                   Vista de inicio
    │
    ├── 📁 organizacion/                  Sedes y responsables
    │   ├── 🔗 urls.py                    Rutas de organización
    │   └── 👁️ views.py                   Vistas del módulo
    │
    ├── 📁 actividades/                   Actividades y evidencias
    │   ├── 🔗 urls.py                    Rutas de actividades
    │   └── 👁️ views.py                   Vistas del módulo
    │
    ├── 📁 agenda/                        Compromisos y prioridades
    │   ├── 🔗 urls.py                    Rutas de agenda
    │   └── 👁️ views.py                   Vistas del módulo
    │
    ├── 📁 resultados/                    Metas, avances e informes
    │   ├── 🔗 urls.py                    Rutas de resultados
    │   └── 👁️ views.py                   Vistas del módulo
    │
    ├── 📁 data/                          Datos del sistema en JSON
    │   ├── 📄 sedes.json
    │   ├── 📄 espacios.json
    │   ├── 📄 responsables.json
    │   ├── 📄 actividades.json
    │   ├── 📄 evidencias.json
    │   ├── 📄 compromisos.json
    │   ├── 📄 periodos.json
    │   ├── 📄 metas.json
    │   └── 📄 resultados.json
    │
    ├── 📁 templates/                     Plantillas HTML
    │   ├── 📄 base.html                  Plantilla base
    │   ├── 📄 inicio.html                Página principal
    │   ├── 📁 organizacion/
    │   │   ├── 📄 inicio.html
    │   │   ├── 📄 lista_sedes.html
    │   │   ├── 📄 detalle_sede.html
    │   │   ├── 📄 lista_responsables.html
    │   │   └── 📄 detalle_responsable.html
    │   ├── 📁 actividades/
    │   │   ├── 📄 inicio.html
    │   │   ├── 📄 lista_actividades.html
    │   │   ├── 📄 detalle_actividad.html
    │   │   ├── 📄 lista_evidencias.html
    │   │   ├── 📄 detalle_evidencia.html
    │   │   └── 📄 evidence.html
    │   ├── 📁 agenda/
    │   │   ├── 📄 inicio.html
    │   │   ├── 📄 lista_compromisos.html
    │   │   ├── 📄 detalle_compromiso.html
    │   │   ├── 📄 lista_reuniones.html
    │   │   └── 📄 resumen_agenda.html
    │   └── 📁 resultados/
    │       ├── 📄 inicio.html
    │       ├── 📄 lista_metas.html
    │       ├── 📄 detalle_meta.html
    │       ├── 📄 resultado_responsable.html
    │       ├── 📄 tablero_sede.html
    │       └── 📄 informe_resumen.html
    │
    └── 📁 static/css/                    Estilos generales
        └── 🎨 style.css
```

El árbol muestra únicamente los archivos funcionales trabajados para este prototipo. Se omiten los archivos estándar generados por Django, como `admin.py`, `apps.py`, `models.py`, `tests.py`, `migrations/`, `manage.py`, `asgi.py`, `wsgi.py` y `db.sqlite3`. La información se consulta desde los archivos JSON de `sgr/data/`; las carpetas de cada aplicación contienen sus vistas y rutas, mientras que `templates/` y `static/` concentran la presentación visual del sistema.

### 9. Uso del proyecto

Tecnologías utilizadas

| Tecnología | Versión usada |
|---|---|
| Python | 3.14.7 |
| Django | 6.1.1 |

En PowerShell, CMD o tu terminal de preferencia debes ejecutar el comando

```
python .\sgr\manage.py check
```

al ejecutar este comando debe de aparecer lo siguente:

```
System check identified no issues (0 silenced).
```

Tras ello, se puede iniciar el servidor con el siguente comando:

```
python .\sgr\manage.py runserver
```

De ahí, simplemente hay que abrir el navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Todos los datos para el uso de esta aplicación están en la carpeta [sgr/data/](sgr/data/).

Para detener el servidor, presiona `Ctrl + C`.

#### Alcance actual

El proyecto implementa actualmente la **Unidad 1**: funciona como un prototipo de consulta construido con Django, cuatro aplicaciones, plantillas, CSS y archivos JSON. Las Unidades 2, 3 y 4 corresponden a etapas posteriores de crecimiento y todavía no forman parte de esta versión.

