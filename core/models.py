from django.db import models 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class Time(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome
    
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    prazo = models.DateField()
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
@receiver(post_save, sender=Tarefa)
def enviar_email_tarefa(sender, instance, created, **Kwargs):
    if created:
        assunto = f"Nova tarefa atribuída: {instance.titulo}"
        mensagem = (
            f"Olá {instance.usuario.nome},\n\n"
            f"Uma nova tarefa foi atrubuída a você no sistema:\n\n"
            f"Título: {instance.titulo}\n"
            f"Descrição: {instance.descricao}\n"
            f"Prazo: {instance.prazo}\n"
            f"Prioridade: {instance.prioridade}\n"
            f"Status: {instance.status}"
            f"Time: {instance.time.nome}"
        )

        send_mail(
            assunto,
            mensagem,
            'admin@crm,com',
            [instance.usuario.email],
            fail_silently=False,
        )