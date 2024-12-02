import streamlit as st
from bcb import sgs
import pandas as pd
import plotly.graph_objects as go

import numpy as np

import streamlit as st
from bcb import sgs
import pandas as pd

@st.cache_data(ttl=10800)  # TTL em segundos (3 horas)
def obter_selic():
    try:
        # Obtém os dados da SELIC acumulada nos últimos 5 anos
        selic_5anos = sgs.get(432)  # Código '432' para a SELIC no SGS do Banco Central
        if selic_5anos is None or selic_5anos.empty:  # Verifica se a resposta é inválida
            raise ValueError("Nenhum dado foi retornado para a SELIC.")
    except Exception as erro_busca_selic:
        st.warning("Não foi possível obter os dados da SELIC (5 anos). Verifique sua conexão ou tente novamente mais tarde.")
        st.error(f"Código do erro: {erro_busca_selic}")
        return None, None, None, None  # Retorna valores default em caso de erro

    # Define a data de corte como a última data disponível
    data_corte = pd.to_datetime("today").normalize()

    # Define o período padrão para 5 anos
    data_inicio_5anos = data_corte - pd.DateOffset(years=5)

    # Filtra os dados para os últimos 5 anos
    selic_filtrado = selic_5anos.loc[data_inicio_5anos:data_corte]

    # Garante que o índice seja datetime
    selic_filtrado.index = pd.to_datetime(selic_filtrado.index)

    # Inverte a ordem do DataFrame para que as datas mais recentes fiquem em cima
    selic_filtrado = selic_filtrado.iloc[::-1]

    # Remove a hora da coluna 'date' para formatar as datas
    selic_filtrado.index = selic_filtrado.index.strftime('%d/%m/%Y')

    # Converte os valores para formato numérico e adiciona o símbolo de '%'
    selic_filtrado_formatado = selic_filtrado.apply(pd.to_numeric, errors='coerce')
    selic_filtrado_formatado = selic_filtrado_formatado.map(lambda x: f"{x:.2f} %" if isinstance(x, (int, float)) else x)

    return selic_filtrado_formatado, selic_5anos, data_inicio_5anos, data_corte

# Função para criar o gráfico da SELIC
@st.cache_data(ttl=10800)
def criar_grafico_selic(selic_filtrado_formatado):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=selic_filtrado_formatado.index,
            y=selic_filtrado_formatado.values.flatten(),
            mode='lines+markers',
            name="Taxa SELIC"
        )
    )

    # Ajustes no layout do gráfico
    fig.update_layout(
        title="Histórico da SELIC (Últimos 5 anos)",
        xaxis_title="Período",
        yaxis_title="SELIC (%)",
        xaxis_rangeslider_visible=True,
    )

    return fig
