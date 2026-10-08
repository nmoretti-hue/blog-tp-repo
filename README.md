# Portfolio de Nicolás Moretti

Página personal hecha con Django. Tiene mis proyectos, un blog y la app de encuestas del tutorial.

## Para abrirla

Extraé el ZIP en una carpeta nueva. La base incluida conserva mi cuenta y las entradas del blog.
Abrí una terminal donde está `manage.py` y ejecutá:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Inicio: http://127.0.0.1:8000/
- Blog: http://127.0.0.1:8000/blog/
- Admin: http://127.0.0.1:8000/admin/
- Encuestas: http://127.0.0.1:8000/polls/

Si empezás con una base vacía, creá tu cuenta con:

```bash
python manage.py createsuperuser
python manage.py cargar_ejemplos
```

`cargar_ejemplos` carga las dos entradas del blog y no las duplica si ya existen.

## Qué puedo editar

En el admin puedo agregar entradas, subir imágenes y videos, y borrar comentarios.
Los lectores se pueden registrar para comentar.

En **Portfolio → Proyectos** puedo cambiar los textos, enlaces, imágenes, estado y orden.
Los proyectos aparecen en el inicio y en el menú. Zaccaria está en desarrollo con Davirro.

El blog tiene dos entradas:
- Mi primera vez programando con bloques.
- Mi primer proyecto: el Juego del Calamar.

## Archivos

- `mysite/`: configuración y rutas.
- `portfolio/`: páginas y proyectos.
- `blog/`: entradas y comentarios.
- `polls/`: encuestas del tutorial.
- `templates/base.html`: estructura común de las páginas.
- `db.sqlite3`: cuentas, entradas y otros datos.
- `media/`: imágenes y videos subidos desde el admin.

Usa Django 5.2 LTS y funciona con Python 3.12. Para probarlo:

```bash
python manage.py test
```

La configuración es para usar en la computadora, no para producción.
No publiques `db.sqlite3`, y cambiá la contraseña del admin antes de subir el sitio a internet.
