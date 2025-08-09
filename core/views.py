from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import TarefaForm

from .models import Tarefa, Usuario

def _get_or_create_usuario_from_user(user):
    if not user.is_authenticated:
        return None
    email = user.email or f"{user.username}@local"
    nome = user.get_full_name() or user.username
    usuario, _ = Usuario.objects.get_or_create(
        email=email,
        defaults={"nome": nome, "cargo": "Colaborador"}
    )
    return usuario

@login_required
def listar_tarefas(request):
    usuario = _get_or_create_usuario_from_user(request.user)
    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')

    tarefas = Tarefa.objects.filter(usuario=usuario)
    if status:
        tarefas = tarefas.filter(status=status)
    if prioridade:
        tarefas = tarefas.filter(prioridade=prioridade)

    return render(request, 'listar_tarefas.html', {'tarefas': tarefas})

@login_required
def tarefas_por_usuario(request, usuario_id):
    usuario = _get_or_create_usuario_from_user(request.user)

    if not request.user.is_staff and (not usuario or usuario.id != usuario_id):
        return HttpResponseForbidden("Você não pode ver tarefas de outro usuário.")

    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')

    tarefas = Tarefa.objects.filter(usuario_id=usuario_id)
    if status:
        tarefas = tarefas.filter(status=status)
    if prioridade:
        tarefas = tarefas.filter(prioridade=prioridade)

    return render(request, 'tarefas_por_usuario.html', {'tarefas': tarefas})

@staff_member_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@login_required
def criar_tarefa(request):
    usuario = _get_or_create_usuario_from_user(request.user)

    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = usuario
            tarefa.save()
            messages.success(request, "Tarefa criada com sucesso!")
            return redirect("listar_tarefas")
    else:
        form = TarefaForm()

    return render(request, "tarefa_form.html", {"form": form})
