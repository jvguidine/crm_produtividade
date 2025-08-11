from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login
from .forms import TarefaForm, CustomUserCreationForm
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
from .models import Time
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TarefaForm
from .models import Tarefa, Usuario
import csv
from django.http import HttpResponse


from .models import Tarefa, Usuario, Time

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

    Time.objects.get_or_create(nome="Geral", defaults={"descricao": "Time padrão"})

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

@login_required
def tarefa_detalhe(request, pk):
    usuario = _get_or_create_usuario_from_user(request.user)
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=usuario)
    return render(request, "tarefa_detalhe.html", {"tarefa": tarefa})

@login_required
def tarefa_finalizar(request, pk):
    usuario = _get_or_create_usuario_from_user(request.user)
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=usuario)

    if request.method != "POST":
        messages.warning(request, "Ação inválida. Use o botão de finalizar.")
        return redirect("tarefa_detalhe", pk=pk)

    if tarefa.status == "concluida":
        messages.info(request, "Esta tarefa já está concluída.")
        return redirect("tarefa_detalhe", pk=pk)

    tarefa.status = "concluida"
    tarefa.data_conclusao = timezone.now()
    tarefa.save()

    messages.success(request, "Tarefa marcada como concluída!")
    return redirect("tarefa_detalhe", pk=pk)


@login_required
def pos_login_redirect(request):
    from django.shortcuts import redirect
    if request.user.is_staff:
        return redirect("listar_usuarios")
    return redirect("listar_tarefas")

def registrar(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            _ = _get_or_create_usuario_from_user(user)
            auth_login(request, user)
            try:
                return redirect("pos_login_redirect")
            except Exception:
                return redirect("listar_tarefas")
    else:
        form = CustomUserCreationForm()
    return render(request, "registrar.html", {"form": form})

@method_decorator(staff_member_required, name='dispatch')
class TimeListView(ListView):
    model = Time
    template_name = 'time_list.html'
    context_object_name = 'times'

@method_decorator(staff_member_required, name='dispatch')
class TimeCreateView(CreateView):
    model = Time
    fields = ['nome', 'descricao']
    template_name = 'time_form.html'
    success_url = reverse_lazy('time_list')

@method_decorator(staff_member_required, name='dispatch')
class TimeUpdateView(UpdateView):
    model = Time
    fields = ['nome', 'descricao']
    template_name = 'time_form.html'
    success_url = reverse_lazy('time_list')

@method_decorator(staff_member_required, name='dispatch')
class TimeDeleteView(DeleteView):
    model = Time
    template_name = 'time_confirm_delete.html'
    success_url = reverse_lazy('time_list')

class TarefaOwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        usuario = _get_or_create_usuario_from_user(self.request.user)
        return Tarefa.objects.filter(usuario=usuario)

class TarefaUpdateView(TarefaOwnerQuerysetMixin, UpdateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'tarefa_form.html'
    def get_success_url(self):
        return self.request.GET.get('next') or f"/tarefas/tarefa/{self.object.pk}/"

class TarefaDeleteView(TarefaOwnerQuerysetMixin, DeleteView):
    model = Tarefa
    template_name = 'tarefa_confirm_delete.html'
    success_url = '/tarefas/'

@method_decorator(staff_member_required, name='dispatch')
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuario_list.html'
    context_object_name = 'usuarios'

@method_decorator(staff_member_required, name='dispatch')
class UsuarioCreateView(CreateView):
    model = Usuario
    fields = ['nome', 'email', 'cargo']
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuario_list')

@method_decorator(staff_member_required, name='dispatch')
class UsuarioUpdateView(UpdateView):
    model = Usuario
    fields = ['nome', 'email', 'cargo']
    template_name = 'usuario_form.html'
    success_url = reverse_lazy('usuario_list')

@method_decorator(staff_member_required, name='dispatch')
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

@login_required
def exportar_tarefas_csv(request):
    usuario = _get_or_create_usuario_from_user(request.user)
    qs = Tarefa.objects.filter(usuario=usuario)

    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')
    if status: qs = qs.filter(status=status)
    if prioridade: qs = qs.filter(prioridade=prioridade)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=tarefas.csv'
    writer = csv.writer(response)
    writer.writerow(['Título', 'Status', 'Prioridade', 'Prazo', 'Time'])
    for t in qs:
        writer.writerow([t.titulo, t.status, t.prioridade, t.prazo, t.time.nome])
    return response

def home(request):

    contexto = {
        "mostrar_dashboard_publico": False,
        "total_pendentes": 0,
        "total_concluidas": 0,
    }

    if not request.user.is_authenticated:
        total_pendentes = Tarefa.objects.filter(status__in=["pendente", "em_andamento"]).count()
        total_concluidas = Tarefa.objects.filter(status="concluida").count()
        contexto.update({
            "mostrar_dashboard_publico": True,
            "total_pendentes": total_pendentes,
            "total_concluidas": total_concluidas,
        })

    return render(request, "home.html", contexto)
