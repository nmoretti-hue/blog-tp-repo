from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Proyecto(models.Model):
    class Estado(models.TextChoices):
        TERMINADO = "terminado", "Terminado"
        EN_DESARROLLO = "en_desarrollo", "En desarrollo"

    titulo = models.CharField("título", max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    descripcion = models.TextField("descripción")
    enlace = models.URLField("enlace al proyecto")
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.TERMINADO)
    colaboradores = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True, help_text="Mostrar en el inicio y el menú de proyectos.")

    class Meta:
        ordering = ["orden", "titulo"]
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("portfolio:proyecto", args=[self.slug])


class ImagenProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="proyectos/", blank=True)
    archivo_estatico = models.CharField("archivo estático", max_length=200, blank=True,
        help_text="Para imágenes existentes en portfolio/imagenes/. Si subís una imagen, dejá este campo vacío.")
    alt = models.CharField("descripción de la imagen", max_length=200)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "pk"]
        verbose_name = "imagen del proyecto"
        verbose_name_plural = "imágenes del proyecto"

    def clean(self):
        super().clean()
        if bool(self.imagen) == bool(self.archivo_estatico):
            raise ValidationError("Elegí una imagen subida o un archivo estático, no ambos.")

    def __str__(self):
        return self.alt
