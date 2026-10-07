# Portfolio de Nicolás Moretti

Primer avance en Django: las páginas del portfolio y las encuestas del tutorial.
Todavía no tiene blog, registro de lectores ni proyectos editables desde el admin.

## Para abrirlo

Desde la carpeta donde está `manage.py`:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Portfolio: http://127.0.0.1:8000/
- Encuestas: http://127.0.0.1:8000/polls/
- Admin del tutorial: http://127.0.0.1:8000/admin/

Para usar el admin, creá tu cuenta con `python manage.py createsuperuser`.
Esta copia no incluye una base de datos ni una cuenta preconfigurada.

## Archivos

- `portfolio/`: inicio, descripción, CV y proyectos.
- `portfolio/proyectos.py`: datos fijos de los proyectos.
- `portfolio/static/`: estilos, imágenes y video de fondo.
- `polls/`: aplicación de encuestas del tutorial.
- `templates/base.html`: estructura común de las páginas.
- `mysite/`: configuración y rutas.

Los proyectos se cambian editando `portfolio/proyectos.py`.
Usa Django 5.2 LTS y Python 3.12 o superior. Es para desarrollo local.

Tests: `python manage.py test`.

## Commit

Para guardar este avance en tu repositorio:

```bash
git add .
git commit -m "add portfolio and polls"
```

No borres la carpeta `.git` de tu repositorio. El ZIP contiene solo los archivos del proyecto.
Si ya copiaste la versión completa, esta carpeta intermedia no debe mezclarse con los archivos
viejos del blog: probala por separado antes de llevarla al repo.
