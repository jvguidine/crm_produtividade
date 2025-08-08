from django.shortcuts import render
from .models import Tarefa
from .models import Usuario

def tarefas_por_usuario(request, usuario_id):
    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')

    tarefas = Tarefa.objects.filter(usuario_id=usuario_id)

    if status:
        tarefas = tarefas.filter(status=status)
    if prioridade:
        tarefas = tarefas.filter(prioridade=prioridade)
    return render(request, 'tarefas_por_usuario.html', {'tarefas': tarefas})

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})