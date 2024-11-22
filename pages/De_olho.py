import yfinance as yf
import pandas as pd
import streamlit as st
from modulos.config import *

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

def obter_dados_bitcoin():
    data_corte = pd.to_datetime("today").normalize()
    data_inicio = data_corte - pd.DateOffset(years=2)  # periodo de pesquisa
    
    dados_btc = yf.download("BTC-USD", start=data_inicio, end=data_corte)
    dados_btc = yf.download("BTC-USD", start=data_inicio, end=data_corte)
    dados_btc.drop(columns=["Adj Close", "Open", "Volume"], inplace=True)  # exclui a coluna 'Adj Close' e 'Open'
    dados_btc = dados_btc.sort_index(ascending=False)
    return dados_btc, data_inicio, data_corte

# Obtém os dados do Bitcoin
dados_btc, data_inicio, data_corte = obter_dados_bitcoin()

# Adiciona algumas métricas interessantes
if not dados_btc.empty:
    st.subheader("Métricas do Bitcoin")
    col1, col2, col3, col4 = st.columns(4)
    
    # Obtém os valores e converte para float
    ultimo_preco = float(dados_btc['Close'].iloc[0])
    penultimo_preco = float(dados_btc['Close'].iloc[1])
    primeiro_preco = float(dados_btc['Close'].iloc[-1])

    preco_maximo = float(dados_btc['High'].max())
    
    preco_minimo = float(dados_btc['Low'].min())
    
    with col1:
        st.metric(label="Preço Atual", value=dolar(ultimo_preco), delta=dolar(penultimo_preco))
    with col2:
        variacao = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100
        st.metric(label="Variação no Período", value=porcentagem(variacao))
    with col3:
        st.metric(label="Máxima no Período", value=dolar(preco_maximo))
    with col4:
        st.metric(label="Mínima no Período", value=dolar(preco_minimo))

# Adiciona informações sobre o período dos dados
st.caption(f"Dados do período: {data_inicio.strftime('%d/%m/%Y')} até {data_corte.strftime('%d/%m/%Y')}")

# Divisão do layout em duas colunas
col1, col2 = st.columns(2)

# Exibição na coluna 1 (dados do Bitcoin)
with col1:
    if not dados_btc.empty:
        st.title("Dados do Bitcoin")
        st.dataframe(dados_btc, use_container_width=True)  # limita a visualização em 7 linhas, mas permite visualizar o restante do dt
    else:
        st.error("Dados do Bitcoin não disponíveis para exibição.")

with col2:
    st.write("Coluna 2")