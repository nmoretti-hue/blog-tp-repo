from django.test import TestCase
from django.urls import reverse


class PortfolioViewsTests(TestCase):
    def test_paginas_principales(self):
        for nombre in ["portfolio:home", "portfolio:description", "portfolio:cv"]:
            response = self.client.get(reverse(nombre))
            self.assertEqual(response.status_code, 200, nombre)

    def test_proyectos(self):
        for slug in ["juego-del-calamar", "pokemon", "reproductor-de-musica"]:
            response = self.client.get(reverse("portfolio:proyecto", args=[slug]))
            self.assertEqual(response.status_code, 200, slug)

    def test_proyecto_inexistente(self):
        response = self.client.get(reverse("portfolio:proyecto", args=["no-existe"]))
        self.assertEqual(response.status_code, 404)


class ProyectosAdminTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.admin = get_user_model().objects.create_superuser(
            'editor', 'editor@example.com', 'test-password-934')

    def test_nuevas_paginas_cargadas(self):
        from .models import Proyecto
        self.assertEqual(Proyecto.objects.count(), 5)
        for slug, enlace in [
            ('nuevo-siglo-propiedades', 'https://nvspp.pages.dev/'),
            ('instituto-zaccaria', 'https://zaccaria.pages.dev/'),
        ]:
            response = self.client.get(reverse('portfolio:proyecto', args=[slug]))
            self.assertContains(response, enlace)
        zaccaria = Proyecto.objects.get(slug='instituto-zaccaria')
        self.assertEqual(zaccaria.colaboradores, 'Davirro')
        self.assertEqual(zaccaria.estado, Proyecto.Estado.EN_DESARROLLO)

    def test_originales_conservan_imagenes(self):
        from .models import Proyecto
        for slug in ['juego-del-calamar', 'pokemon', 'reproductor-de-musica']:
            self.assertEqual(Proyecto.objects.get(slug=slug).imagenes.count(), 3)

    def test_admin_puede_agregar_y_aparece_en_inicio_y_menu(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('admin:portfolio_proyecto_add'), {
            'titulo': 'Un proyecto nuevo', 'slug': 'un-proyecto-nuevo',
            'descripcion': 'Texto', 'enlace': 'https://example.com/',
            'estado': 'en_desarrollo', 'colaboradores': 'Un compañero',
            'orden': 6, 'visible': 'on', '_save': 'Guardar',
            'imagenes-TOTAL_FORMS': 0, 'imagenes-INITIAL_FORMS': 0,
            'imagenes-MIN_NUM_FORMS': 0, 'imagenes-MAX_NUM_FORMS': 1000,
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('portfolio:home'))
        self.assertContains(response, '<strong>Un proyecto nuevo</strong>', html=True)
        self.assertContains(response, '<a class="dropdown-item" href="/proyectos/un-proyecto-nuevo/">Un proyecto nuevo</a>', html=True)
        response = self.client.get(reverse('portfolio:proyecto', args=['un-proyecto-nuevo']))
        self.assertContains(response, 'Un compañero')

    def test_proyecto_oculto_no_aparece(self):
        from .models import Proyecto
        Proyecto.objects.filter(slug='instituto-zaccaria').update(visible=False)
        response = self.client.get(reverse('portfolio:home'))
        self.assertNotContains(response, 'Instituto Zaccaria')
        response = self.client.get(reverse('portfolio:proyecto', args=['instituto-zaccaria']))
        self.assertEqual(response.status_code, 404)

    def test_descripcion_escapa_html(self):
        from .models import Proyecto
        Proyecto.objects.filter(slug='instituto-zaccaria').update(descripcion='<script>alert(1)</script>')
        response = self.client.get(reverse('portfolio:proyecto', args=['instituto-zaccaria']))
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;')

    def test_visitante_no_puede_agregar_proyectos(self):
        response = self.client.get(reverse('admin:portfolio_proyecto_add'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_navbar_sin_boton_admin_y_panel_disponible(self):
        self.client.force_login(self.admin)
        for name in ['portfolio:home', 'blog:post_list']:
            response = self.client.get(reverse(name))
            self.assertNotContains(response, 'href="/admin/"')
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 200)
