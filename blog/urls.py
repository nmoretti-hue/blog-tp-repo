from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("comentario/<int:pk>/eliminar/", views.eliminar_comentario, name="eliminar_comentario"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
]
