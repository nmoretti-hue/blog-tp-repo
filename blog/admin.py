from django.contrib import admin

from .models import Comentario, Post


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ["autor", "texto", "creado"]
    readonly_fields = ["autor", "texto", "creado"]
    # Desde la entrada el admin puede tildar "Eliminar" en cada comentario
    can_delete = True

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["titulo", "estado", "fecha_publicacion", "autor", "cantidad_comentarios"]
    list_filter = ["estado", "fecha_publicacion"]
    search_fields = ["titulo", "contenido"]
    prepopulated_fields = {"slug": ["titulo"]}
    date_hierarchy = "fecha_publicacion"
    inlines = [ComentarioInline]
    fieldsets = [
        (None, {"fields": ["titulo", "slug", "resumen", "contenido"]}),
        ("Multimedia", {"fields": ["imagen", "video"]}),
        ("Publicación", {"fields": ["estado", "fecha_publicacion"]}),
    ]

    @admin.display(description="Comentarios")
    def cantidad_comentarios(self, obj):
        return obj.comentarios.count()

    def save_model(self, request, obj, form, change):
        # El autor siempre es el admin que crea la entrada
        if not change:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ["autor", "post", "texto", "creado"]
    list_filter = ["creado", "post"]
    search_fields = ["texto", "autor__username"]
    readonly_fields = ["post", "autor", "texto", "creado"]

    def has_add_permission(self, request):
        return False
