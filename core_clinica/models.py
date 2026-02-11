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
    
class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    descricao = models.TextField(blank=True, null=True, verbose_name="Observações Médicas")
    valor_consulta = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.paciente} - {self.medico} em {self.data}"

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"