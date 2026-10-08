from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from blog.models import Post

EJEMPLOS = Path(__file__).resolve().parent.parent.parent / "ejemplos"

POSTS = [
    {
        'titulo': 'Mi primera vez programando con bloques',
        'slug': 'mis-primeros-bloques',
        'resumen': 'Así empecé con la programación, antes de escribir código.',
        "contenido": (
            'No arranqué escribiendo código. Mi primera vez programando fue con bloques: '
            'juntaba las instrucciones para armar el programa.\n\n'
            'Los bloques se ejecutan en un orden, así que hay que acomodarlos según lo que '
            'querés hacer.\n\n'
            'Después pasé a hacer proyectos con código. El primero fue el Juego del Calamar.'
        ),
        'dias_atras': 2,
    },
    {
        'titulo': 'Mi primer proyecto: el Juego del Calamar',
        'slug': 'mi-primer-proyecto-juego-del-calamar',
        'resumen': 'Lo hice con dos compañeros. Yo me encargué de los sprites y el menú.',
        "contenido": (
            'Mi primer proyecto fue un juego del Calamar que hice con dos compañeros. Era un '
            'trabajo para clase y tenía nota.\n\n'
            'Yo me encargué de los sprites y del menú. Nos llevó varias clases terminarlo. En '
            'la página del proyecto dejé imágenes del menú y de algunas partes del juego.\n\n'
            'Después lo llevamos a la ExpoHuergo, pero nadie lo jugó. Igual, quedó como uno de '
            'los primeros proyectos que subí a mi portfolio.'
        ),
        'imagen': 'menu.png',
        'dias_atras': 1,
    },
]


class Command(BaseCommand):
    help = "Carga entradas de ejemplo en el blog (requiere un superusuario creado)."

    def handle(self, *args, **options):
        admin = get_user_model().objects.filter(is_superuser=True).first()
        if admin is None:
            raise CommandError("Primero creá un superusuario: python manage.py createsuperuser")

        for datos in POSTS:
            if Post.objects.filter(slug=datos["slug"]).exists():
                self.stdout.write(f"Ya existe: {datos['titulo']}")
                continue
            post = Post(
                titulo=datos["titulo"],
                slug=datos["slug"],
                resumen=datos["resumen"],
                contenido=datos["contenido"],
                autor=admin,
                estado=Post.Estado.PUBLICADO,
                fecha_publicacion=timezone.now() - timedelta(days=datos["dias_atras"]),
            )
            if datos.get("imagen"):
                with open(EJEMPLOS / datos["imagen"], "rb") as f:
                    post.imagen.save(datos["imagen"], File(f), save=False)
            if datos.get("video"):
                with open(EJEMPLOS / datos["video"], "rb") as f:
                    post.video.save(datos["video"], File(f), save=False)
            post.save()
            self.stdout.write(self.style.SUCCESS(f"Creada: {post.titulo}"))
