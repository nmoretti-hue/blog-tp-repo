from .models import Proyecto


def proyectos_menu(request):
    return {"proyectos_menu": Proyecto.objects.filter(visible=True)}
