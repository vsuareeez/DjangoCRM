# DjangoCRM

> CRM en Django para gestión de clientes, con módulo de calendario.

Aplicación web desarrollada con Django que permite administrar una cartera de clientes (registro, consulta, edición y eliminación) con autenticación de usuarios, e incluye un módulo de calendario para organizar actividades.

## Características

- **Gestión de clientes (CRUD):** registrar, listar, editar y eliminar clientes.
- **Autenticación de usuarios:** login y control de acceso a las vistas.
- **Módulo de calendario:** organización de eventos/actividades.
<!-- [Confirma esta lista según lo que realmente tenga la app y agrega/quita lo que corresponda] -->

## Stack

- **Backend:** Python · Django
- **Base de datos:** <!-- [Confirma: SQLite / MySQL / PostgreSQL] -->
- **Frontend:** HTML, plantillas de Django

## Cómo ejecutarlo localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/vsuareeez/DjangoCRM.git
cd DjangoCRM

# 2. Crear y activar un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt   # [Si no existe, créalo con: pip freeze > requirements.txt]

# 4. Aplicar migraciones
python manage.py migrate

# 5. (Opcional) Crear un superusuario
python manage.py createsuperuser

# 6. Levantar el servidor
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000/` en el navegador.

## Estructura del proyecto

```
dcrm/          # Configuración del proyecto Django
website/       # App principal (gestión de clientes)
calendar_app/  # Módulo de calendario
manage.py      # Punto de entrada de Django
```

## Capturas

<!-- [Agrega 1-2 capturas de pantalla aquí: arrástralas al editor de GitHub o súbelas a una carpeta /docs] -->

---

> ⚠️ **Nota de seguridad:** revisa que `mydb.py` y `settings.py` no tengan credenciales reales commiteadas (contraseñas de base de datos, `SECRET_KEY`). Si las tienen, muévelas a variables de entorno y agrégalas a `.gitignore`.
