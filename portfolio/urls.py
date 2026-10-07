from django.urls import path

from . import views

app_name = "portfolio"
urlpatterns = [
    path("", views.home, name="home"),
    path("description/", views.description, name="description"),
    path("cv/", views.cv, name="cv"),
    path("proyectos/<slug:slug>/", views.proyecto, name="proyecto"),
]
