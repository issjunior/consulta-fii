import streamlit as st
from bcb import sgs
import pandas as pd
import plotly.graph_objects as go

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def obter_cdi():
    try:
        # Obtém os dados da SELIC acumulada nos últimos 5 anos
        cdi_5anos = sgs.get(4389)  # Código '4389' para a SELIC no SGS do Banco Central
        if cdi_5anos is None or cdi_5anos.empty:  # Verifica se a resposta é inválida
            raise ValueError("Nenhum dado foi retornado para o CDI.")
    except Exception as erro_busca_cdi:
        st.warning("Não foi possível obter os dados do CDI (5 anos). Verifique sua conexão ou tente novamente mais tarde.")
        st.error(f"Código do erro: {erro_busca_cdi}")
        return None  # Retorna apenas None em caso de erro
    
    # Define a data de corte como a última data disponível
    data_corte = pd.to_datetime("today").normalize()

    # Define o período padrão para 5 anos
    data_inicio_5anos = data_corte - pd.DateOffset(years=5)

    # Filtra os dados para os últimos 5 anos
    cdi_filtrado = cdi_5anos.loc[data_inicio_5anos:data_corte]

    # Garante que o índice seja datetime
    cdi_filtrado.index = pd.to_datetime(cdi_filtrado.index)

    # Remove valores consecutivos iguais e NaN
    cdi_filtrado = cdi_filtrado[cdi_filtrado.diff().fillna(1) != 0].dropna()

    # Inverte a ordem do DataFrame para que as datas mais recentes fiquem em cima
    cdi_filtrado = cdi_filtrado.iloc[::-1]

    # Formata os valores da coluna 4389 diretamente com o símbolo de porcentagem
    cdi_filtrado["4389"] = cdi_filtrado["4389"].apply(lambda x: f"{x:.2f}%")

    # Renomeia a coluna "4389" para "Código SGS CDI 4389"
    cdi_filtrado.rename(columns={"4389": "Código SGS CDI - 4389"}, inplace=True)

    return cdi_filtrado, cdi_5anos, data_inicio_5anos, data_corte

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def criar_grafico_cdi(cdi_filtrado_formatado, data_inicio_12meses, data_corte):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=cdi_filtrado_formatado.index,
            y=cdi_filtrado_formatado.values.flatten(),  # Transforma em vetor simples
            mode='markers+lines',
            name="CDI",
            hovertemplate="<b>Data:</b> %{x}<br><b>CDI:</b> %{y:.2f} %<extra></extra>",
        )
    )
    
    # Ajustes no layout do gráfico
    fig.update_layout(
        title="Histórico de CDI (últimos 5 anos)",
        xaxis_title="Período",
        yaxis_title="CDI (%)",
        xaxis_rangeslider_visible=True,  # Controle de zoom (range slider)
        xaxis_range=[data_inicio_12meses, data_corte],  # Mostra os últimos 12 meses inicialmente
    )
    
    return fig