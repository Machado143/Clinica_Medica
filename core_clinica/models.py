from django.db import models

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)
    especialidade = models.CharField(max_length=50)

    def __str__(self):
        return f"Dr(a). {self.nome} - {self.especialidade}"

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return self.nome