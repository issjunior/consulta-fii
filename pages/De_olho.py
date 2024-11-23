import yfinance as yf
import pandas as pd
import streamlit as st
from config import *

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

def obter_dados_bitcoin():
    data_corte = pd.to_datetime("today").normalize()
    data_inicio = data_corte - pd.DateOffset(years=2)  # período de pesquisa
    
    dados_btc = yf.download("BTC-USD", start=data_inicio, end=data_corte)
    dados_btc.drop(columns=["Adj Close", "Open", "Volume"], inplace=True)  # exclui colunas desnecessárias
    dados_btc = dados_btc.sort_index(ascending=False)
    
    # Ajusta o índice para o formato de data brasileiro (dd/mm/aaaa)
    dados_btc.index = pd.to_datetime(dados_btc.index).strftime('%d/%m/%Y')
    
    return dados_btc, data_inicio, data_corte

# Obtém os dados do Bitcoin
dados_btc, data_inicio, data_corte = obter_dados_bitcoin()

# Adiciona algumas métricas interessantes
if not dados_btc.empty:
    st.subheader("Métricas do Bitcoin")
    col1, col2, col3, col4 = st.columns(4)
    
    # Obtém os valores e converte para float para as métricas
    ultimo_preco = dados_btc['Close'].iloc[0].item()
    penultimo_preco = dados_btc['Close'].iloc[1].item()
    primeiro_preco = dados_btc['Close'].iloc[-1].item()
    preco_maximo = dados_btc['High'].max().item()
    preco_minimo = dados_btc['Low'].min().item()
    
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
st.caption(f"Dados do período: {data_inicio.strftime('%d/%m/%Y')} até {data_corte.strftime('%d/%m/%Y')} (últimos 2 anos)")

if not dados_btc.empty:
    dados_btc.columns = ["Fechamento", "Máximo", "Mínimo"] # renomeia colunas
    st.dataframe(dados_btc, height=140, use_container_width=True)  # datagrama
else:
    st.error("Dados do Bitcoin não disponíveis para exibição.")

st.divider()