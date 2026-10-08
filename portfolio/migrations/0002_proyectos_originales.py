from django.db import migrations

# Copia de los datos originales para que la migración no dependa de las vistas.
PROYECTOS = [{'slug': 'juego-del-calamar', 'titulo': 'EL JUEGO DEL CALAMAR', 'descripcion': 'Este juego fue desarrollado por mi y mis dos compañeros\nEn este juego fue un trabajo con nota en el que me encargue de los sprites y el menu El proyecto en ser terminado tardo varias clases\nLo expusimos en la ExpoHuergo y nadie lo jugo', 'enlace': 'https://github.com/idavirro/squidgamepy.git', 'orden': 1, 'imagenes': [{'archivo': 'menu.png', 'alt': 'menu'}, {'archivo': 'rope.png', 'alt': 'rope'}, {'archivo': 'cristales.png', 'alt': 'cristales'}]}, {'slug': 'pokemon', 'titulo': 'POKEMON', 'descripcion': 'Este juego fue desarrollado por mi\nEn este juego fue un trabajo con nota que realice El proyecto en ser terminado tardo varias clases\nMe saque un 8 en este proyecto', 'enlace': 'https://github.com/nmoretti-hue/pokemoncitos.git', 'orden': 2, 'imagenes': [{'archivo': 'pokemonardo.jfif', 'alt': 'portada pokemon'}, {'archivo': 'Capturapokemon.png', 'alt': 'captura pokemon'}, {'archivo': 'segundaCapturapokemon.png', 'alt': 'segunda captura pokemon'}]}, {'slug': 'reproductor-de-musica', 'titulo': 'REPRODUCTOR DE MÚSICA', 'descripcion': 'Este Reproductor de Música fue desarrollado por mi\nEn este proyecto fue un trabajo con nota que realice El proyecto en ser terminado tardo pocas clases\nLo hice con la IA y el profe fue bueno y me aprobo', 'enlace': 'https://github.com/nmoretti-hue/Trabajo-Practico-1.git', 'orden': 3, 'imagenes': [{'archivo': 'reproductorMusica.png', 'alt': 'reproductor'}, {'archivo': 'barradebusqueda.png', 'alt': 'barra de busqueda'}, {'archivo': 'ReproductorCodigo.png', 'alt': 'codigo del reproductor'}]}]


def cargar_originales(apps, schema_editor):
    Proyecto = apps.get_model('portfolio', 'Proyecto')
    Imagen = apps.get_model('portfolio', 'ImagenProyecto')
    alias = schema_editor.connection.alias
    for record in PROYECTOS:
        datos = dict(record)
        imagenes = datos.pop('imagenes')
        slug = datos.pop('slug')
        proyecto, creado = Proyecto.objects.using(alias).get_or_create(slug=slug, defaults=datos)
        if creado:
            for orden, imagen in enumerate(imagenes):
                Imagen.objects.using(alias).create(proyecto=proyecto,
                    archivo_estatico=imagen['archivo'], alt=imagen['alt'], orden=orden)


class Migration(migrations.Migration):
    dependencies = [('portfolio', '0001_initial')]
    operations = [migrations.RunPython(cargar_originales, migrations.RunPython.noop)]
