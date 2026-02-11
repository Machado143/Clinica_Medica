from django.db.models import Sum, Count

from .models import Consulta


def relatorio_faturamento_por_medico():
    """Retorna um queryset com o faturamento agrupado por médico."""
    qs = (
        Consulta.objects.values("medico__nome", "medico__especialidade")
        .annotate(
            total=Sum("valor_consulta"),
            qtd=Count("id"),
        )
        .order_by("-total")
    )
    return qs