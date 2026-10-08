from django.contrib import admin
from .models import ImagenProyecto, Proyecto


class ImagenProyectoInline(admin.TabularInline):
    model = ImagenProyecto
    extra = 0
    fields = ["imagen", "archivo_estatico", "alt", "orden"]


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "estado", "colaboradores", "visible", "orden"]
    list_filter = ["estado", "visible"]
    search_fields = ["titulo", "descripcion", "colaboradores"]
    prepopulated_fields = {"slug": ["titulo"]}
    inlines = [ImagenProyectoInline]
    fieldsets = [
        (None, {"fields": ["titulo", "slug", "descripcion", "enlace"]}),
        ("Estado y presentación", {"fields": ["estado", "colaboradores", "orden", "visible"]}),
    ]
