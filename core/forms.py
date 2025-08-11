from django import forms
from .models import Tarefa
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "status", "prioridade", "prazo", "time"]
        widgets = {
            "prazo": forms.DateInput(attrs={"type": "date"}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]