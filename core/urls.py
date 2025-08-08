from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tarefas/<int:usuario_id>/', views.tarefas_por_usuario, name='tarefas_por_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tarefas/', views.listar_tarefas, name='listar_tarefas'),
]