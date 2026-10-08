from django.shortcuts import get_object_or_404, render
from blog.models import Post
from .models import Proyecto


def home(request):
    ultimos_posts = Post.objects.publicados()[:3]
    return render(request, "portfolio/home.html", {"ultimos_posts": ultimos_posts})


def description(request):
    return render(request, "portfolio/description.html")


def cv(request):
    return render(request, "portfolio/cv.html")


def proyecto(request, slug):
    datos = get_object_or_404(Proyecto.objects.prefetch_related("imagenes"), slug=slug, visible=True)
    return render(request, "portfolio/proyecto.html", {"proyecto": datos})
