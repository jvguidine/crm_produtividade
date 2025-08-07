from django.db import models 

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