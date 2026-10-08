"""
URL configuration for mysite project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

from blog import views as blog_views

urlpatterns = [
    path("", include("portfolio.urls")),
    path("blog/", include("blog.urls")),
    path("polls/", include("polls.urls")),
    path("cuentas/registro/", blog_views.registro, name="signup"),
    path("cuentas/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()

if settings.DEBUG:
    # En desarrollo django sirve los archivos que se suben desde el admin
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
