# Bitácora

> Borrador: completalo con tus palabras y con lo que te pasó a vos.

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
- **Dificultad:** el botón de logout con un link (GET) no funciona en Django 5+.
  **Solución:** un formulario POST con `{% csrf_token %}`.
- Para que solo el admin borre comentarios usé `@staff_member_required`, y para crear entradas el admin de Django.

## Qué haría distinto / quedó en el tintero

- Editor de texto enriquecido para las entradas (por ejemplo, Markdown).
- Categorías o etiquetas y un buscador.
- Deploy en un hosting.
