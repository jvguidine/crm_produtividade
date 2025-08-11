from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import TimeListView, TimeCreateView, TimeUpdateView, TimeDeleteView, TarefaUpdateView, TarefaDeleteView, UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView

urlpatterns = [
    path('tarefas/<int:usuario_id>/', views.tarefas_por_usuario, name='tarefas_por_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tarefas/', views.listar_tarefas, name='listar_tarefas'),
    path('tarefas/nova/', views.criar_tarefa, name='criar_tarefa'),
    path('tarefa/<int:pk>/', views.tarefa_detalhe, name='tarefa_detalhe'),
    path('tarefa/<int:pk>/finalizar/', views.tarefa_finalizar, name='tarefa_finalizar'),
    path('registrar/', views.registrar, name='registrar'),
    path('pos-login/', views.pos_login_redirect, name='pos_login_redirect'),
]

urlpatterns += [
    path('times/', TimeListView.as_view(), name='time_list'),
    path('times/novo/', TimeCreateView.as_view(), name='time_create'),
    path('times/<int:pk>/editar/', TimeUpdateView.as_view(), name='time_update'),
    path('times/<int:pk>/excluir/', TimeDeleteView.as_view(), name='time_delete'),
    path('tarefa/<int:pk>/editar/', TarefaUpdateView.as_view(), name='tarefa_editar'),
    path('tarefa/<int:pk>/excluir/', TarefaDeleteView.as_view(), name='tarefa_excluir'),
    path('usuarios/lista/', UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/novo/', UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/excluir/', UsuarioDeleteView.as_view(), name='usuario_delete'),
    path('tarefas/exportar/', views.exportar_tarefas_csv, name='exportar_tarefas_csv'),
]
