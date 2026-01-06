import streamlit as st
import yfinance as yf

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
)

st.title("Cálculo de Ações")
st.caption("Método de análise de desempenho de ações")