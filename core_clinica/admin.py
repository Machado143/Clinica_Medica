from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html

from .models import Medico, Paciente, Consulta


# ──────────────────────────────────────────────
# Médico
# ──────────────────────────────────────────────
@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especialidade', 'crm', 'total_consultas')
    search_fields = ('nome', 'crm', 'especialidade')
    list_filter = ('especialidade',)
    ordering = ('nome',)

    @admin.display(description='Consultas', ordering='total_consultas')
    def total_consultas(self, obj):
        return obj.consulta_set.count()


# ──────────────────────────────────────────────
# Paciente
# ──────────────────────────────────────────────
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'data_nascimento')
    search_fields = ('nome', 'cpf', 'email')
    list_filter = ('data_nascimento',)
    ordering = ('nome',)


# ──────────────────────────────────────────────
# Consulta  (com dashboard de gráficos)
# ──────────────────────────────────────────────
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'paciente',
        'medico',
        'data',
        'horario',
        'valor_formatado',
        'resumo_diagnostico',
    )
    list_filter = ('data', 'medico', 'medico__especialidade')
    search_fields = ('paciente__nome', 'medico__nome', 'diagnostico')
    date_hierarchy = 'data'
    ordering = ('-data', '-horario')
    list_per_page = 25
    autocomplete_fields = ('paciente', 'medico')
    readonly_fields = ('created_display',)

    fieldsets = (
        ('Informações da Consulta', {
            'fields': ('paciente', 'medico', 'data', 'horario', 'valor_consulta'),
        }),
        ('Dados Clínicos', {
            'classes': ('collapse',),
            'fields': ('descricao', 'diagnostico', 'prescricao'),
        }),
    )

    # ── colunas customizadas ──
    @admin.display(description='Valor', ordering='valor_consulta')
    def valor_formatado(self, obj):
        return format_html(
            '<span style="color:#28a745;font-weight:600">R$&nbsp;{}</span>',
            f'{obj.valor_consulta:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        )

    @admin.display(description='Diagnóstico')
    def resumo_diagnostico(self, obj):
        if obj.diagnostico:
            resumo = obj.diagnostico[:50] + ('…' if len(obj.diagnostico) > 50 else '')
            return resumo
        return '—'

    @admin.display(description='Criado em')
    def created_display(self, obj):
        return f'{obj.data} às {obj.horario}'

    # ── actions ──
    actions = ['marcar_valor_padrao']

    @admin.action(description='✏️ Definir valor padrão (R$ 250,00)')
    def marcar_valor_padrao(self, request, queryset):
        updated = queryset.update(valor_consulta=250.00)
        self.message_user(request, f'{updated} consulta(s) atualizada(s) para R$ 250,00.')