from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import ComentarioForm, RegistroForm
from .models import Comentario, Post


class PostListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.publicados().select_related("autor")


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.publicados(), slug=slug)
    form = ComentarioForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(post.get_absolute_url())
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = request.user
            comentario.save()
            messages.success(request, "¡Comentario publicado!")
            return redirect(f"{post.get_absolute_url()}#comentarios")

    comentarios = post.comentarios.select_related("autor")
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comentarios": comentarios, "form": form},
    )


@staff_member_required
@require_POST
def eliminar_comentario(request, pk):
    """Solo el administrador (usuarios staff) puede borrar comentarios."""
    comentario = get_object_or_404(Comentario, pk=pk)
    post = comentario.post
    comentario.delete()
    messages.info(request, "Comentario eliminado.")
    return redirect(f"{post.get_absolute_url()}#comentarios")


def registro(request):
    if request.user.is_authenticated:
        return redirect("blog:post_list")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido, {usuario.username}! Ya podés comentar.")
            return redirect("blog:post_list")
    else:
        form = RegistroForm()
    return render(request, "registration/signup.html", {"form": form})
