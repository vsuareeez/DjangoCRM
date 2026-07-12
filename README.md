# DjangoCRM

> CRM en Django para gestión de clientes, con módulo de calendario.

Aplicación web desarrollada con Django que permite administrar una cartera de clientes (registro, consulta, edición y eliminación) con autenticación de usuarios, e incluye un módulo de calendario para organizar actividades.

## Características

- **Gestión de clientes (CRUD):** registrar, listar, editar y eliminar clientes.
- **Autenticación de usuarios:** login, registro y control de acceso a las vistas.
- **Roles y permisos:** grupos `Admin` (control total sobre clientes) y `Viewer` (solo lectura), creados automáticamente al migrar.
- **Notas por cliente:** cada cliente puede tener notas con autor y fecha.
- **Historial de cambios:** auditoría de modificaciones de clientes con `django-simple-history`.
- **Dashboard:** gráficos de clientes por ciudad y por mes.
- **Módulo de calendario:** organización de eventos/actividades.

## Stack

- **Backend:** Python · Django
- **Base de datos:** MySQL (o SQLite para desarrollo rápido)
- **Frontend:** HTML, plantillas de Django, Bootstrap

## Cómo ejecutarlo localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/vsuareeez/DjangoCRM.git
cd DjangoCRM

# 2. Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Opción A: SQLite (lo más rápido, sin instalar nada más)

```bash
export DB_ENGINE=sqlite3      # En Windows: set DB_ENGINE=sqlite3
python manage.py migrate
python manage.py runserver
```

### Opción B: MySQL

Crea la base de datos (`CREATE DATABASE dcrm;`) y configura las credenciales
como variables de entorno — **nunca las escribas en el código**:

```bash
export DB_NAME=dcrm
export DB_USER=root
export DB_PASSWORD=tu_contraseña
export DB_HOST=localhost
export DB_PORT=3306

python manage.py migrate
python manage.py runserver
```

### Crear un superusuario (opcional)

```bash
python manage.py createsuperuser
```

Luego abre `http://127.0.0.1:8000/` en el navegador.

### Variables de entorno para producción

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django (obligatoria en producción) |
| `DJANGO_DEBUG` | `False` en producción |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por coma |
| `DB_*` | Credenciales de la base de datos (ver arriba) |

## Estructura del proyecto

```
dcrm/          # Configuración del proyecto Django
website/       # App principal (gestión de clientes, notas, dashboard)
calendar_app/  # Módulo de calendario
manage.py      # Punto de entrada de Django
```

## Tests

```bash
DB_ENGINE=sqlite3 python manage.py test
```
