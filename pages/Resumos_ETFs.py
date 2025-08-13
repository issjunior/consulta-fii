import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import *

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
)

st.title("Resumo de ETFs")
st.caption("Considerando o período de 2 anos")

# Lista de tickers para análise
tickers = ["VOO"]  # Tickers

# Data de início e fim para buscar os dados
data_fim = datetime.today()
data_inicio = data_fim - timedelta(days=365 * 2)

# Função para buscar dados e processar
@st.cache_data
def fetch_ticker_data(ticker):
    # Note que auto_adjust=False para garantir que 'Adj Close' exista
    df = yf.download(ticker, start=data_inicio, end=data_fim, auto_adjust=False)
    df["Ticker"] = ticker
    df.reset_index(inplace=True)
    return df

def process_ticker_data(df):
    # Fechamento ajustado, maior e menor valores
    adj_close = df["Adj Close"]
    maior_valor = float(adj_close.max().item())
    menor_valor = float(adj_close.min().item())
    return adj_close, maior_valor, menor_valor

# Processar dados para cada ticker
dataframes = []
for ticker in tickers:
    data = fetch_ticker_data(ticker)
    adj_close, maior_valor, menor_valor = process_ticker_data(data)
    
    # Obter o valor corrente do ticker (último preço de mercado)
    ticker_info = yf.Ticker(ticker)
    ticker_history = ticker_info.history(period="1d", auto_adjust=False)  # Também aqui manter False
    
    # Verificar se 'Adj Close' está presente ou usar 'Close'
    if 'Adj Close' in ticker_history.columns:
        ultimo_valor_corrente = ticker_history['Adj Close'].iloc[-1]
    elif 'Close' in ticker_history.columns:
        ultimo_valor_corrente = ticker_history['Close'].iloc[-1]
    else:
        ultimo_valor_corrente = None  # Caso não haja nenhum valor disponível
    
    # Calcular a diferença entre o maior e menor valor
    diferenca_valores = maior_valor - menor_valor
    
    # Calcular a diferença percentual
    if menor_valor != 0:
        diferenca_percentual = ((maior_valor - menor_valor) / menor_valor) * 100
    else:
        diferenca_percentual = 0  # Evitar divisão por zero, caso o menor valor seja 0
    
    # Adicionar informações ao DataFrame
    resumo = pd.DataFrame({
        "Ticker": [ticker.replace(".SA", "")],
        "Preço atual": dolar(ultimo_valor_corrente) if ultimo_valor_corrente is not None else "N/A",
        "+ Preço": dolar(maior_valor),
        "- Preço": dolar(menor_valor),
        "Diferença (US$)": dolar(diferenca_valores),
        "Diferença (%)": porcentagem(diferenca_percentual)
    })
    dataframes.append(resumo)

# Concatenar todos os DataFrames
resultados = pd.concat(dataframes, ignore_index=True)

# Exibir DataFrame no Streamlit sem a coluna de índice
st.dataframe(resultados, use_container_width=True, hide_index=True)
