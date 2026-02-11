import pandas as pd
from .models import Consulta

def relatorio_faturamento_por_medico():
    # 1. Transformamos o banco de dados em um DataFrame do Pandas
    df = Consulta.pdobjects.all().to_dataframe(
        fieldnames=['medico__nome', 'valor_consulta', 'data']
    )
    
    if df.empty:
        return "Nenhum dado encontrado."

    # 2. Usamos o poder do Pandas para agrupar e somar
    faturamento = df.groupby('medico__nome')['valor_consulta'].sum().reset_index()
    
    return faturamento