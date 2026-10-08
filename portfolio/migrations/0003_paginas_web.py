from django.db import migrations

PROYECTOS = [{'titulo': 'Nuevo Siglo Propiedades', 'slug': 'nuevo-siglo-propiedades', 'descripcion': 'Desarrollé una página web para Nuevo Siglo Propiedades, una inmobiliaria de Barracas y San Telmo.\nEl sitio presenta la inmobiliaria, información sobre propiedades y tasaciones, y opciones de contacto por WhatsApp.', 'enlace': 'https://nvspp.pages.dev/', 'estado': 'terminado', 'colaboradores': '', 'orden': 4, 'visible': True}, {'titulo': 'Instituto Zaccaria', 'slug': 'instituto-zaccaria', 'descripcion': 'Estoy desarrollando esta página web junto con Davirro para el Instituto Zaccaria.\nEl sitio reúne información de jardín, primaria y secundaria, actividades, historia del colegio y datos de contacto.\nEl proyecto sigue en desarrollo.', 'enlace': 'https://zaccaria.pages.dev/', 'estado': 'en_desarrollo', 'colaboradores': 'Davirro', 'orden': 5, 'visible': True}]


def cargar_paginas(apps, schema_editor):
    Proyecto = apps.get_model('portfolio', 'Proyecto')
    for record in PROYECTOS:
        datos = dict(record)
        slug = datos.pop('slug')
        Proyecto.objects.using(schema_editor.connection.alias).get_or_create(slug=slug, defaults=datos)


class Migration(migrations.Migration):
    dependencies = [('portfolio', '0002_proyectos_originales')]
    operations = [migrations.RunPython(cargar_paginas, migrations.RunPython.noop)]
