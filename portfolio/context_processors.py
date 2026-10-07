from .proyectos import PROYECTOS


def proyectos_menu(request):
    return {"proyectos_menu": PROYECTOS.values()}
