from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["texto"]
        labels = {"texto": "Tu comentario"}
        widgets = {"texto": forms.Textarea(attrs={"rows": 4, "placeholder": "Escribí algo..."})}


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email (opcional)")

    class Meta(UserCreationForm.Meta):
        fields = ["username", "email"]
