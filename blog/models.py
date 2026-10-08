from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def publicados(self):
        """Entradas publicadas cuya fecha ya llego (igual que en polls)."""
        return self.filter(estado=Post.Estado.PUBLICADO, fecha_publicacion__lte=timezone.now())


class Post(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"

    titulo = models.CharField("título", max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    resumen = models.CharField(max_length=300, help_text="Se muestra en el listado del blog.")
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="blog/imagenes/", blank=True)
    video = models.FileField(
        upload_to="blog/videos/",
        blank=True,
        validators=[FileExtensionValidator(["mp4", "webm", "ogg"])],
        help_text="Opcional. Formatos: mp4, webm u ogg.",
    )
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.BORRADOR)
    fecha_publicacion = models.DateTimeField("fecha de publicación", default=timezone.now)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-fecha_publicacion"]
        verbose_name = "entrada"
        verbose_name_plural = "entradas"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios"
    )
    texto = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["creado"]

    def __str__(self):
        return f"Comentario de {self.autor} en {self.post}"
