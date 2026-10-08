# Bitácora

## Tutorial de Django

Hice el tutorial de la documentación (partes 1 a 8) con la app de encuestas `polls`.

## Errores que tuve

- Al correr el servidor me salía `No module named 'debug_toolbar'`. Faltaba instalarlo. Lo arreglé con `python -m pip install -r requirements.txt`.
- No sabía cómo entrar al admin. Hay que crear un usuario con `python manage.py createsuperuser` y entrar a `/admin`.
- Al principio las entradas del blog se cargaban con un comando de Python. Lo saqué porque el TP pide que solo el admin cree entradas, así que ahora las cargo desde `/admin`.
- Los proyectos también estaban escritos en el código. Los pasé a la base de datos para poder editarlos desde el admin.

## Qué haría distinto / qué me quedó pendiente

- Subirlo a un hosting.
- Poner categorías en el blog.


## Tutorial de Django (partes 1 a 8)

- Hice la app `polls`: modelos `Question` y `Choice`, vistas genéricas, templates, admin, tests y archivos estáticos.
- En la parte 8 instalé `django-debug-toolbar`.

## Migración del portfolio

- **Dificultad:** las rutas relativas del HTML (`imagenes/...`, `styles.css`) dejaron de funcionar.
  **Solución:** moví todo a `portfolio/static/portfolio/` y usé `{% static %}`. Las fuentes de `styles.css` siguen con rutas relativas porque están en la misma carpeta.
- **Dificultad:** la navbar y el script del modo oscuro estaban repetidos en cada página.
  **Solución:** un `base.html` del que heredan todas las páginas.
- Las tres páginas de proyectos eran casi iguales, así que quedaron en un solo template y una vista que recibe el `slug`.

## Blog

- **Dificultad:** las imágenes y videos subidos desde el admin no se veían.
  **Solución:** configurar `MEDIA_URL` / `MEDIA_ROOT` y servirlos en desarrollo desde `urls.py`.

## Qué haría distinto / quedó en el tintero

- Editor de texto enriquecido para las entradas (por ejemplo, Markdown).
- Categorías o etiquetas y un buscador.
- Deploy en un hosting.

