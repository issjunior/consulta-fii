import streamlit as st
from modulos.scraping_valorpatrimonial import *
from config import *

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
)

with st.expander("Entenda o cálculo"):
    st.write("Para fundos imobiliários de papel basta o valor sobre o valor patrimonial (P/VP) para precificar o fundo.")

st.divider()

st.header("Cálculo de preço teto para FIIs de Papel")
ticker = st.text_input("Ticker do FII:", "").upper() + ".SA"

if st.button("Consultar"):
    valor_obter_pvp = obter_pvp(ticker)

    st.subheader(f"O P/VP do {ticker.replace('.SA', '')} é de {valor_obter_pvp}")
