from django.test import TestCase
from django.urls import reverse


class PortfolioTests(TestCase):
    def test_paginas(self):
        for nombre in ["portfolio:home", "portfolio:description", "portfolio:cv"]:
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)

    def test_proyectos(self):
        from .proyectos import PROYECTOS
        for slug in PROYECTOS:
            self.assertEqual(self.client.get(reverse("portfolio:proyecto", args=[slug])).status_code, 200)

    def test_proyecto_inexistente(self):
        self.assertEqual(self.client.get("/proyectos/no-existe/").status_code, 404)

    def test_blog_y_cuentas_todavia_no_existen(self):
        self.assertEqual(self.client.get("/blog/").status_code, 404)
        self.assertEqual(self.client.get("/cuentas/registro/").status_code, 404)
        self.assertNotContains(self.client.get("/"), 'href="/blog/"')

    def test_panel_del_tutorial_disponible(self):
        from django.contrib.auth import get_user_model
        admin = get_user_model().objects.create_superuser("editor", "editor@example.com", "test-password-934")
        self.client.force_login(admin)
        self.assertEqual(self.client.get(reverse("admin:polls_question_changelist")).status_code, 200)
        self.assertEqual(self.client.get("/admin/portfolio/proyecto/").status_code, 404)
