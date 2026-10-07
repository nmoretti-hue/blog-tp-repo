from django.http import Http404
from django.shortcuts import render

from .proyectos import PROYECTOS


def home(request):
    return render(request, "portfolio/home.html")


def description(request):
    return render(request, "portfolio/description.html")


def cv(request):
    return render(request, "portfolio/cv.html")


def proyecto(request, slug):
    datos = PROYECTOS.get(slug)
    if datos is None:
        raise Http404("Proyecto no encontrado")
    return render(request, "portfolio/proyecto.html", {"proyecto": datos})
