from django.contrib import admin
from .models import Medico, Paciente, Consulta

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone') # Colunas que aparecem na lista
    search_fields = ('nome', 'cpf') # Barra de busca rápida

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm', 'especialidade')
    list_filter = ('especialidade',) # Filtro lateral por especialidade

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data', 'horario')
    list_filter = ('data', 'medico') # Filtro por dia e por médico
    date_hierarchy = 'data' # Cria um navegador de datas no topo