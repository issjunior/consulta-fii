import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import *

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("📊 Resumo de ETFs")

st.divider()

# ================================================================
# CONFIGURAÇÕES
# ================================================================
tickers = ["VOO", "DIVD11.SA", "NDIV11.SA"]

# Tickers brasileiros (.SA) são exibidos em R$, demais em US$
TICKERS_BRL = {"DIVD11.SA", "NDIV11.SA"}

data_fim    = datetime.today()
data_inicio = data_fim - timedelta(days=365 * 2)

# ================================================================
# FUNÇÕES
# ================================================================
def formatar_moeda(ticker: str, valor) -> str:
    """Retorna o valor formatado em R$ ou US$ conforme o ticker."""
    if valor is None:
        return "N/A"
    if ticker in TICKERS_BRL:
        return real(valor)
    return dolar(valor)

def simbolo_moeda(ticker: str) -> str:
    return "R$" if ticker in TICKERS_BRL else "US$"

@st.cache_data
def fetch_ticker_data(ticker):
    df = yf.download(ticker, start=data_inicio, end=data_fim, auto_adjust=False)
    df["Ticker"] = ticker
    df.reset_index(inplace=True)
    return df

@st.cache_data
def fetch_ticker_info(ticker):
    ticker_info = yf.Ticker(ticker)
    history     = ticker_info.history(period="1d", auto_adjust=False)
    info        = ticker_info.info
    return history, info

def process_ticker_data(df):
    adj_close   = df["Adj Close"]
    maior_valor = float(adj_close.max().item())
    menor_valor = float(adj_close.min().item())
    return adj_close, maior_valor, menor_valor

def get_ultimo_valor(history):
    if 'Adj Close' in history.columns:
        return history['Adj Close'].iloc[-1]
    elif 'Close' in history.columns:
        return history['Close'].iloc[-1]
    return None

# ================================================================
# COLETA E PROCESSAMENTO DOS DADOS
# ================================================================
with st.spinner("Buscando dados dos ETFs..."):
    dataframes  = []
    dados_cards = []

    for ticker in tickers:
        data                                = fetch_ticker_data(ticker)
        adj_close, maior_valor, menor_valor = process_ticker_data(data)
        history, info                       = fetch_ticker_info(ticker)
        ultimo_valor                        = get_ultimo_valor(history)

        diferenca_valores    = maior_valor - menor_valor
        diferenca_percentual = ((maior_valor - menor_valor) / menor_valor * 100) if menor_valor != 0 else 0

        # Variação do dia
        preco_anterior   = info.get("previousClose", None)
        variacao_dia_pct = None
        if ultimo_valor is not None and preco_anterior:
            variacao_dia_pct = ((float(ultimo_valor) - float(preco_anterior)) / float(preco_anterior)) * 100

        fmt = lambda v, t=ticker: formatar_moeda(t, v)

        dados_cards.append({
            "ticker":            ticker,
            "nome":              info.get("longName", ticker.replace(".SA", "")),
            "ultimo_valor":      ultimo_valor,
            "maior_valor":       maior_valor,
            "menor_valor":       menor_valor,
            "diferenca_valores": diferenca_valores,
            "diferenca_pct":     diferenca_percentual,
            "variacao_dia_pct":  variacao_dia_pct,
            "fmt":               fmt,
            "simbolo":           simbolo_moeda(ticker),
        })

        resumo = pd.DataFrame({
            "Ticker":        [ticker.replace(".SA", "")],
            "Nome":          [info.get("longName", "N/A")],
            "Preço Atual":   [fmt(ultimo_valor) if ultimo_valor is not None else "N/A"],
            "+ Preço (2a)":  [fmt(maior_valor)],
            "- Preço (2a)":  [fmt(menor_valor)],
            "Amplitude":     [fmt(diferenca_valores)],
            "Amplitude (%)": [porcentagem(diferenca_percentual)],
        })
        dataframes.append(resumo)

# ================================================================
# CARDS DE DESTAQUE POR TICKER
# ================================================================
st.subheader("📌 Visão Geral")
st.caption("Período de referência: últimos 2 anos")

cols = st.columns(len(dados_cards))

for i, d in enumerate(dados_cards):
    fmt          = d["fmt"]
    ticker_label = d["ticker"].replace(".SA", "")

    with cols[i]:
        with st.container(border=True):
            st.subheader(f"🏷️ {ticker_label}")
            st.caption(f"{d['nome']}  •  moeda: {d['simbolo']}")

            col_a, col_b = st.columns(2)
            with col_a:
                with st.container(border=True):
                    st.caption("📈 Máxima (2 anos)")
                    st.write(f"**{fmt(d['maior_valor'])}**")
            with col_b:
                with st.container(border=True):
                    st.caption("📉 Mínima (2 anos)")
                    st.write(f"**{fmt(d['menor_valor'])}**")

            with st.container(border=True):
                if d["ultimo_valor"] is not None and d["variacao_dia_pct"] is not None:
                    st.metric(
                        label="💹 Preço Atual",
                        value=fmt(d["ultimo_valor"]),
                        delta=f"{d['variacao_dia_pct']:+.2f}% hoje",
                    )
                else:
                    st.caption("💹 Preço Atual")
                    st.write(fmt(d["ultimo_valor"]))

            with st.container(border=True):
                st.caption("↔️ Amplitude do período")
                st.write(f"{fmt(d['diferenca_valores'])}  ({porcentagem(d['diferenca_pct'])})")

st.divider()

# ================================================================
# TABELA RESUMO COMPLETO
# ================================================================
st.subheader("📋 Tabela Resumo Completo")
st.caption("Período de referência: últimos 2 anos")

resultados = pd.concat(dataframes, ignore_index=True)
st.dataframe(resultados, use_container_width=True, hide_index=True)