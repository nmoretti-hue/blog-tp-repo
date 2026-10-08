# Bitácora

## Tutorial de Django

Hice el tutorial de la documentación (partes 1 a 8) con la app de encuestas `polls`.

## Pasar mi página a Django

- No entendía por qué el `index.html` tenía tan pocas líneas. Después vi que las plantillas usan `{% extends %}` y `{% block %}`, y que lo que se repite (navbar, modo oscuro) está en `base.html`.
- Las imágenes y el CSS dejaron de cargar con las rutas de antes. Los moví a `static` y usé `{% static %}`.

## Errores que tuve

- Al correr el servidor me salía `No module named 'debug_toolbar'`. Faltaba instalarlo. Lo arreglé con `python -m pip install -r requirements.txt`.
- No sabía cómo entrar al admin. Hay que crear un usuario con `python manage.py createsuperuser` y entrar a `/admin`.
- Al principio las entradas del blog se cargaban con un comando de Python. Lo saqué porque el TP pide que solo el admin cree entradas, así que ahora las cargo desde `/admin`.
- Los proyectos también estaban escritos en el código. Los pasé a la base de datos para poder editarlos desde el admin.

## Qué haría distinto / qué me quedó pendiente

- Subirlo a un hosting.
- Poner categorías en el blog.
