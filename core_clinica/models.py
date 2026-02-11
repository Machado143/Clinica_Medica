from django.db import models


class Medico(models.Model):
    nome = models.CharField("Nome", max_length=100)
    crm = models.CharField("CRM", max_length=20, unique=True)
    especialidade = models.CharField("Especialidade", max_length=50)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ["nome"]

    def __str__(self):
        return f"Dr(a). {self.nome} — {self.especialidade}"


class Paciente(models.Model):
    nome = models.CharField("Nome", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    telefone = models.CharField("Telefone", max_length=20)
    data_nascimento = models.DateField("Data de Nascimento")
    email = models.EmailField("E-mail")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name="Médico")
    data = models.DateField("Data")
    horario = models.TimeField("Horário")
    valor_consulta = models.DecimalField("Valor", max_digits=8, decimal_places=2, default=0.0)
    descricao = models.TextField(blank=True, null=True, verbose_name="Observações Médicas")
    diagnostico = models.TextField(blank=True, null=True, verbose_name="Diagnóstico/Sintomas")
    prescricao = models.TextField(blank=True, null=True, verbose_name="Prescrição Médica")

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ["-data", "-horario"]

    def __str__(self):
        return f"{self.paciente} — {self.medico} em {self.data}"
