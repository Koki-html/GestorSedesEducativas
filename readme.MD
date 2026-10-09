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
La organización administra sedes educativas con salas, laboratorios, oficinas y espacios comunes. El sistema centraliza el registro de actividades, responsables, evidencias, compromisos y resultados para facilitar el seguimiento y la toma de decisiones.

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

### 7. Estado actual y limitaciones

El proyecto utiliza modelos Django, migraciones y el panel administrativo para gestionar
los registros de organización, actividades, agenda y resultados. Los archivos JSON se
conservan como fuente inicial de datos y pueden importarse a la base de datos mediante el
comando `importar_datos`.

Todavía no se incluyen:
* API pública.
* Formularios personalizados fuera del administrador.
* Permisos específicos por rol.
* Autenticación de usuarios finales con perfiles propios.

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
    │   ├── ⚙️ admin.py                   Configuración del CRUD administrativo
    │   ├── 🧱 models.py                  Modelos de sedes y responsables
    │   ├── 🔗 urls.py                    Rutas de organización
    │   ├── 👁️ views.py                   Vistas del módulo
    │   ├── 📁 migrations/                Migraciones de la aplicación
    │   └── 📁 management/                Comandos personalizados de Django
    │       └── 📁 commands/
    │           └── 📄 importar_datos.py
    │
    ├── 📁 actividades/                   Actividades y evidencias
    │   ├── ⚙️ admin.py                   Configuración del CRUD administrativo
    │   ├── 🧱 models.py                  Modelos de actividades y evidencias
    │   ├── 🔗 urls.py                    Rutas de actividades
    │   ├── 👁️ views.py                   Vistas del módulo
    │   └── 📁 migrations/                Migraciones de la aplicación
    │
    ├── 📁 agenda/                        Compromisos y prioridades
    │   ├── ⚙️ admin.py                   Configuración del CRUD administrativo
    │   ├── 🧱 models.py                  Modelo de compromisos
    │   ├── 🔗 urls.py                    Rutas de agenda
    │   ├── 👁️ views.py                   Vistas del módulo
    │   └── 📁 migrations/                Migraciones de la aplicación
    │
    ├── 📁 resultados/                    Metas, avances e informes
    │   ├── ⚙️ admin.py                   Configuración del CRUD administrativo
    │   ├── 🧱 models.py                  Modelos de períodos, metas y resultados
    │   ├── 🔗 urls.py                    Rutas de resultados
    │   ├── 👁️ views.py                   Vistas del módulo
    │   └── 📁 migrations/                Migraciones de la aplicación
    │
    ├── 📁 data/                          Datos iniciales del sistema en JSON
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
    ├── 📁 static/css/                    Estilos generales
        └── 🎨 style.css
```

Cada aplicación contiene sus modelos, migraciones, vistas, rutas y configuración de administración.
La carpeta `sgr/data/` contiene los datos iniciales y `templates/` y `static/` concentran la
presentación visual del sistema.

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

Para crear o actualizar las tablas de la base de datos:

```
python .\sgr\manage.py migrate
```

Para cargar todos los archivos JSON en la base de datos sin duplicar registros:

```
python .\sgr\manage.py importar_datos
```

El comando puede ejecutarse nuevamente cuando cambien los JSON; utiliza los identificadores
de los archivos para actualizar los registros existentes.

Tras ello, se puede iniciar el servidor con el siguente comando:

```
python .\sgr\manage.py runserver
```


De ahí, simplemente hay que abrir el navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Todos los datos para el uso de esta aplicación están en la carpeta [sgr/data/](sgr/data/).

El panel administrativo está disponible en [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
Para crear el usuario administrador:

```
python .\sgr\manage.py createsuperuser
```

Para detener el servidor, presiona `Ctrl + C`.

### 10. Herramientas de apoyo

Se utilizaron herramientas de inteligencia artificial como apoyo para generar datos,
comentar código, revisar avances y agilizar tareas repetitivas. La estructura, integración
y validación del proyecto se realizaron sobre el código de este repositorio.
#### Alcance actual

El proyecto implementa principalmente las **Unidades 1 y 2**: funciona como una aplicación
de consulta construida con Django, cuatro aplicaciones, plantillas, CSS, archivos JSON,
modelos, migraciones, persistencia y CRUD mediante el panel administrativo.

Para conservar los datos en AWS se recomienda utilizar Amazon RDS MySQL. En producción se
deben configurar las variables `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`
y `DB_PORT`, ejecutar `migrate` y luego `importar_datos`. El archivo `.env` no debe subirse
al repositorio.

