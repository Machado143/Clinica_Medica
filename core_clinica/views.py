import json
from datetime import date, timedelta

from django.db.models import Sum, Count, Avg
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import render

from .models import Consulta, Medico, Paciente


def dashboard_data(request):
    """API JSON que alimenta os gráficos do dashboard admin."""

    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    # ── KPIs ──────────────────────────────────────────────
    total_consultas = Consulta.objects.count()
    total_pacientes = Paciente.objects.count()
    total_medicos = Medico.objects.count()
    faturamento_total = (
        Consulta.objects.aggregate(total=Sum("valor_consulta"))["total"] or 0
    )
    faturamento_mes = (
        Consulta.objects.filter(data__gte=inicio_mes).aggregate(
            total=Sum("valor_consulta")
        )["total"]
        or 0
    )
    ticket_medio = (
        Consulta.objects.aggregate(media=Avg("valor_consulta"))["media"] or 0
    )
    consultas_mes = Consulta.objects.filter(data__gte=inicio_mes).count()

    # ── Faturamento por Médico (bar chart) ────────────────
    fat_medico = (
        Consulta.objects.values("medico__nome")
        .annotate(total=Sum("valor_consulta"), qtd=Count("id"))
        .order_by("-total")
    )
    fat_medico_labels = [item["medico__nome"] for item in fat_medico]
    fat_medico_values = [float(item["total"]) for item in fat_medico]
    fat_medico_qtd = [item["qtd"] for item in fat_medico]

    # ── Consultas por Especialidade (doughnut) ────────────
    por_espec = (
        Consulta.objects.values("medico__especialidade")
        .annotate(qtd=Count("id"))
        .order_by("-qtd")
    )
    espec_labels = [item["medico__especialidade"] for item in por_espec]
    espec_values = [item["qtd"] for item in por_espec]

    # ── Faturamento nos últimos 30 dias (line chart) ──────
    trinta_dias = hoje - timedelta(days=30)
    por_dia = (
        Consulta.objects.filter(data__gte=trinta_dias)
        .values("data")
        .annotate(total=Sum("valor_consulta"), qtd=Count("id"))
        .order_by("data")
    )
    dias_labels = [item["data"].strftime("%d/%m") for item in por_dia]
    dias_fat = [float(item["total"]) for item in por_dia]
    dias_qtd = [item["qtd"] for item in por_dia]

    # ── Faturamento mensal (bar chart) ────────────────────
    por_mes = (
        Consulta.objects.annotate(
            _mes=ExtractMonth("data"),
            _ano=ExtractYear("data"),
        )
        .values("_ano", "_mes")
        .annotate(total=Sum("valor_consulta"), qtd=Count("id"))
        .order_by("_ano", "_mes")
    )
    meses_labels = [f'{item["_mes"]:02d}/{item["_ano"]}' for item in por_mes]
    meses_fat = [float(item["total"]) for item in por_mes]
    meses_qtd = [item["qtd"] for item in por_mes]

    # ── Top 5 pacientes por gasto ─────────────────────────
    top_pacientes = (
        Consulta.objects.values("paciente__nome")
        .annotate(total=Sum("valor_consulta"), qtd=Count("id"))
        .order_by("-total")[:5]
    )
    top_pac_labels = [item["paciente__nome"] for item in top_pacientes]
    top_pac_values = [float(item["total"]) for item in top_pacientes]

    return JsonResponse(
        {
            "kpis": {
                "total_consultas": total_consultas,
                "total_pacientes": total_pacientes,
                "total_medicos": total_medicos,
                "faturamento_total": float(faturamento_total),
                "faturamento_mes": float(faturamento_mes),
                "ticket_medio": round(float(ticket_medio), 2),
                "consultas_mes": consultas_mes,
            },
            "fat_medico": {
                "labels": fat_medico_labels,
                "values": fat_medico_values,
                "qtd": fat_medico_qtd,
            },
            "especialidades": {
                "labels": espec_labels,
                "values": espec_values,
            },
            "diario": {
                "labels": dias_labels,
                "faturamento": dias_fat,
                "qtd": dias_qtd,
            },
            "mensal": {
                "labels": meses_labels,
                "faturamento": meses_fat,
                "qtd": meses_qtd,
            },
            "top_pacientes": {
                "labels": top_pac_labels,
                "values": top_pac_values,
            },
        }
    )
