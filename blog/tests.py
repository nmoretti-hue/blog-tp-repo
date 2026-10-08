import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Comentario, Post

User = get_user_model()


def crear_post(autor, titulo="Entrada", dias=0, estado=Post.Estado.PUBLICADO):
    return Post.objects.create(
        titulo=titulo,
        slug=titulo.lower().replace(" ", "-"),
        autor=autor,
        resumen="Resumen",
        contenido="Contenido de prueba",
        estado=estado,
        fecha_publicacion=timezone.now() + datetime.timedelta(days=dias),
    )


class BlogTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@test.com", "clave-admin-123")
        self.usuario = User.objects.create_user("lector", password="clave-lector-123")

    def test_lista_ordenada_cronologicamente(self):
        vieja = crear_post(self.admin, "Vieja", dias=-10)
        nueva = crear_post(self.admin, "Nueva", dias=-1)
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(list(response.context["posts"]), [nueva, vieja])

    def test_no_muestra_borradores_ni_futuras(self):
        crear_post(self.admin, "Borrador", estado=Post.Estado.BORRADOR)
        futura = crear_post(self.admin, "Futura", dias=5)
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, "Todavía no hay entradas publicadas.")
        detalle = self.client.get(futura.get_absolute_url())
        self.assertEqual(detalle.status_code, 404)

    def test_anonimo_no_puede_comentar(self):
        post = crear_post(self.admin, "Post", dias=-1)
        response = self.client.post(post.get_absolute_url(), {"texto": "hola"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(Comentario.objects.count(), 0)

    def test_usuario_logueado_comenta(self):
        post = crear_post(self.admin, "Post", dias=-1)
        self.client.login(username="lector", password="clave-lector-123")
        self.client.post(post.get_absolute_url(), {"texto": "Buen post!"})
        comentario = Comentario.objects.get()
        self.assertEqual(comentario.autor, self.usuario)
        self.assertEqual(comentario.post, post)

    def test_solo_admin_elimina_comentarios(self):
        post = crear_post(self.admin, "Post", dias=-1)
        comentario = Comentario.objects.create(post=post, autor=self.usuario, texto="hola")
        url = reverse("blog:eliminar_comentario", args=[comentario.pk])

        self.client.login(username="lector", password="clave-lector-123")
        self.client.post(url)
        self.assertTrue(Comentario.objects.filter(pk=comentario.pk).exists())

        self.client.login(username="admin", password="clave-admin-123")
        self.client.post(url)
        self.assertFalse(Comentario.objects.filter(pk=comentario.pk).exists())

    def test_solo_admin_crea_entradas(self):
        self.client.login(username="lector", password="clave-lector-123")
        response = self.client.get(reverse("admin:blog_post_add"))
        self.assertEqual(response.status_code, 302)

        self.client.login(username="admin", password="clave-admin-123")
        response = self.client.get(reverse("admin:blog_post_add"))
        self.assertEqual(response.status_code, 200)

    def test_registro_de_usuario(self):
        response = self.client.post(
            reverse("signup"),
            {"username": "nuevo", "password1": "UnaClaveLarga#2026", "password2": "UnaClaveLarga#2026"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="nuevo").exists())

class AdminCreaEntradaTests(TestCase):
    """Las entradas se cargan desde /admin, no desde el codigo."""

    def setUp(self):
        from tempfile import TemporaryDirectory
        from django.test import override_settings
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        override = override_settings(MEDIA_ROOT=self.media.name)
        override.enable()
        self.addCleanup(override.disable)
        self.admin = User.objects.create_superuser("nico", "nico@example.com", "clave-admin-123")
        self.client.login(username="nico", password="clave-admin-123")

    def test_entrada_con_imagen_desde_el_admin(self):
        import base64
        from django.core.files.uploadedfile import SimpleUploadedFile
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )
        ahora = timezone.localtime()
        response = self.client.post(
            reverse("admin:blog_post_add"),
            {
                "titulo": "Mi primera vez programando con bloques",
                "slug": "mis-primeros-bloques",
                "resumen": "Resumen",
                "contenido": "Contenido",
                "imagen": SimpleUploadedFile("menu.png", png, content_type="image/png"),
                "estado": Post.Estado.PUBLICADO,
                "fecha_publicacion_0": ahora.strftime("%Y-%m-%d"),
                "fecha_publicacion_1": (ahora - datetime.timedelta(minutes=1)).strftime("%H:%M:%S"),
                "comentarios-TOTAL_FORMS": "0",
                "comentarios-INITIAL_FORMS": "0",
                "comentarios-MIN_NUM_FORMS": "0",
                "comentarios-MAX_NUM_FORMS": "1000",
            },
        )
        self.assertEqual(response.status_code, 302, getattr(response, "context", None) and response.context["adminform"].form.errors)
        post = Post.objects.get()
        self.assertEqual(post.autor, self.admin)
        self.assertTrue(post.imagen)
        self.client.logout()
        self.assertContains(self.client.get(reverse("blog:post_list")), post.titulo)

class EntradasPersonalesTests(TestCase):
    def setUp(self):
        from io import StringIO
        from tempfile import TemporaryDirectory
        from django.core.management import call_command
        from django.test import override_settings
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        User.objects.create_superuser('nico', 'nico@example.com', 'test-password-934')
        call_command('cargar_ejemplos', stdout=StringIO())

    def test_ejemplos_personales_sin_duplicados(self):
        from io import StringIO
        from django.core.management import call_command
        call_command('cargar_ejemplos', stdout=StringIO())
        self.assertEqual(Post.objects.count(), 2)
        self.assertTrue(Post.objects.filter(slug='mis-primeros-bloques').exists())
        juego = Post.objects.get(slug='mi-primer-proyecto-juego-del-calamar')
        self.assertIn('dos compañeros', juego.contenido)
        self.assertIn('sprites', juego.contenido)
        self.assertTrue(juego.imagen)

    def test_nuevas_entradas_se_pueden_leer(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, 'Mis primeros pasos programando')
        for post in Post.objects.all():
            response = self.client.get(post.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, post.titulo)
>>>>>>> e67b288071008cb1d29441a89272e27c16e9c648
