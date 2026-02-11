from django.contrib import admin
from django.db.models import Sum, Count
from .models import Medico, Paciente, Consulta

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade', 'crm')
    search_fields = ('nome',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone')
    search_fields = ('nome', 'cpf')

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'data', 'valor_consulta')
    list_filter = ('data', 'medico')
    
    # Esta função injeta dados no Dashboard do Admin
    def changelist_view(self, request, extra_context=None):
        # 1. Total de Faturamento
        total_faturamento = Consulta.objects.aggregate(Sum('valor_consulta'))['valor_consulta__sum'] or 0
        
        # 2. Consultas por Médico (o que o Pandas faria, o Django faz aqui)
        faturamento_por_medico = Consulta.objects.values('medico__nome').annotate(
            total=Sum('valor_consulta'),
            qtd=Count('id')
        ).order_by('-total')

        extra_context = extra_context or {}
        extra_context['total_faturamento'] = total_faturamento
        extra_context['faturamento_medicos'] = faturamento_por_medico
        
        return super().changelist_view(request, extra_context=extra_context)