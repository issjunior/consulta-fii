import streamlit as st
import yfinance as yf

from modulos.scraping_acoes import *

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
#   layout="centered",  # ou "wide"
)

st.title("Cálculo de preço teto Ações")

with st.expander("Entenda o cálculo"):
    st.title("Método Graham")
    st.write("Busca determinar um valor justo para uma ação com base no lucro por ação (LPA) e na taxa de crescimento esperada da empresa")

    moldura = st.container(border=True)
    moldura.image("img/formula_graham.png")

st.divider()

st.header("Parâmetros de Fundamentalistas")

ticker = st.text_input("Ticker da Ação:", "").upper()

if st.button("Buscar Dados"):
    dados = obter_dados_acao(ticker)
    if dados:
        st.write("Dados obtidos:")
        st.json(dados)
    else:
        st.error("Não foi possível obter os dados para o ticker informado.")
