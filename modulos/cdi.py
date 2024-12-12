import streamlit as st
from bcb import sgs
import pandas as pd

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def obter_cdi():
    try:
        # Obtém os dados da SELIC acumulada nos últimos 5 anos
        cdi_5anos = sgs.get(4389)  # Código '4389' para a SELIC no SGS do Banco Central
        if cdi_5anos is None or cdi_5anos.empty:  # Verifica se a resposta é inválida
            raise ValueError("Nenhum dado foi retornado para a CDI.")
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

    return cdi_filtrado, cdi_5anos, data_inicio_5anos, data_corte