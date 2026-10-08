# Portfolio de Nicolás Moretti

Mi página personal hecha con Django. Tiene mis proyectos, un blog con comentarios y la app de encuestas del tutorial.

## Cómo correrlo

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Inicio: http://127.0.0.1:8000/
- Blog: http://127.0.0.1:8000/blog/
- Admin: http://127.0.0.1:8000/admin/
- Encuestas: http://127.0.0.1:8000/polls/

## Blog

- Las entradas las crea solo el admin desde **/admin → Blog → Entradas**. Cada una tiene texto, imagen y video.
- Se muestran ordenadas por fecha, la más nueva primero.
- Para comentar hay que registrarse e ingresar.
- Los comentarios los borra solo el admin (botón "Eliminar" en la entrada o desde /admin).

## Proyectos

Se editan desde **/admin → Portfolio → Proyectos** y aparecen en el inicio y en el menú.

## Carpetas

- `mysite/`: configuración y rutas.
- `portfolio/`: páginas y proyectos.
- `blog/`: entradas y comentarios.
- `polls/`: encuestas del tutorial.
- `templates/base.html`: la parte común de todas las páginas.

`db.sqlite3` y `media/` no se suben al repo, así que en una instalación nueva el blog arranca vacío y las entradas se cargan desde el admin.

Tests: `python manage.py test`
