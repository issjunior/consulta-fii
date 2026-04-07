import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from config import *
import time

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("📊 Resumo de FIIs")

st.divider()

# ================================================================
# CONFIGURAÇÕES
# ================================================================
tickers = [
    "GARE11.SA", "HFOF11.SA", "HGLG11.SA", "HGRU11.SA",
    "HSLG11.SA", "HSML11.SA", "JSRE11.SA", "KNCR11.SA",
    "KNSC11.SA", "PMLL11.SA", "RZAK11.SA", "RZTR11.SA",
    "TRXF11.SA", "TVRI11.SA", "XPML11.SA", "XPSF11.SA"
]

data_fim    = datetime.today()
data_inicio = data_fim - timedelta(days=365)  # 12 meses

# ================================================================
# FUNÇÕES
# ================================================================
@st.cache_data(ttl=10800)
def fetch_ticker_data(ticker):
    try:
        df = yf.download(ticker, start=data_inicio, end=data_fim, progress=False)
        df["Ticker"] = ticker
        df.reset_index(inplace=True)
        return df
    except Exception:
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

@st.cache_data(ttl=10800)
def fetch_ticker_info(ticker):
    """
    Busca history e info separadamente com fallback individual,
    evitando que um erro em .info derrube toda a página.
    """
    ticker_obj = yf.Ticker(ticker)

    # Buscar histórico recente
    try:
        history = ticker_obj.history(period="1d")
    except Exception:
        history = pd.DataFrame()

    # Buscar info — ponto mais propenso ao HTTP 500
    try:
        info = ticker_obj.info
    except Exception:
        info = {}  # Dicionário vazio como fallback seguro

    return history, info

def process_ticker_data(df):
    if df.empty:
        return None, None, None
    if "Adj Close" in df.columns:
        adj_close = df["Adj Close"]
    elif "Close" in df.columns:
        adj_close = df["Close"]
    else:
        return None, None, None
    menor_valor = float(adj_close.min().item())
    maior_valor = float(adj_close.max().item())
    return adj_close, menor_valor, maior_valor

def get_ultimo_valor(history):
    if history is None or history.empty:
        return None
    if 'Adj Close' in history.columns:
        return history['Adj Close'].iloc[-1]
    elif 'Close' in history.columns:
        return history['Close'].iloc[-1]
    return None

# ================================================================
# COLETA E PROCESSAMENTO COM LOADING
# ================================================================
dataframes  = []
dados_cards = []
erros       = []  # Acumula tickers que falharam para exibir ao final

loading_container = st.empty()
progress_bar      = st.progress(0, text="Iniciando busca...")

total = len(tickers)

for idx, ticker in enumerate(tickers):
    ticker_label = ticker.replace(".SA", "")

    progress_bar.progress(
        idx / total,
        text=f"⏳ Buscando dados de **{ticker_label}**... ({idx + 1}/{total})"
    )
    loading_container.info(f"📡 Consultando: **{ticker_label}**")

    try:
        data                                = fetch_ticker_data(ticker)
        adj_close, menor_valor, maior_valor = process_ticker_data(data)
        history, info                       = fetch_ticker_info(ticker)
        ultimo_valor                        = get_ultimo_valor(history)

        # Se não há dados de preço, pula o ticker
        if menor_valor is None or maior_valor is None:
            erros.append(f"⚠️ {ticker_label}: histórico de preços indisponível.")
            continue

        diferenca_valores    = maior_valor - menor_valor
        diferenca_percentual = ((maior_valor - menor_valor) / menor_valor * 100) if menor_valor != 0 else 0

        # Variação do dia — depende do info, usa fallback se vazio
        preco_anterior   = info.get("previousClose", None)
        variacao_dia_pct = None
        if ultimo_valor is not None and preco_anterior:
            variacao_dia_pct = ((float(ultimo_valor) - float(preco_anterior)) / float(preco_anterior)) * 100

        dados_cards.append({
            "ticker":            ticker,
            "nome":              info.get("longName", ticker_label),
            "ultimo_valor":      ultimo_valor,
            "maior_valor":       maior_valor,
            "menor_valor":       menor_valor,
            "diferenca_valores": diferenca_valores,
            "diferenca_pct":     diferenca_percentual,
            "variacao_dia_pct":  variacao_dia_pct,
        })

        resumo = pd.DataFrame({
            "Ticker":         [ticker_label],
            "Nome":           [info.get("longName", "N/A")],
            "Preço Atual":    [real(ultimo_valor) if ultimo_valor is not None else "N/A"],
            "- Preço (12m)":  [real(menor_valor)],
            "+ Preço (12m)":  [real(maior_valor)],
            "Amplitude (R$)": [real(diferenca_valores)],
            "Amplitude (%)":  [porcentagem(diferenca_percentual)],
        })
        dataframes.append(resumo)

    except Exception as e:
        # Qualquer erro inesperado não derruba a página inteira
        erros.append(f"⚠️ {ticker_label}: {str(e)}")
        continue

# Finaliza loading
progress_bar.progress(1.0, text="✅ Todos os dados carregados!")
loading_container.success("✅ Dados carregados com sucesso!")

time.sleep(1.5)
progress_bar.empty()
loading_container.empty()

# Exibe avisos de tickers que falharam (se houver)
if erros:
    with st.expander(f"⚠️ {len(erros)} ticker(s) com problema — clique para ver"):
        for erro in erros:
            st.warning(erro)

# ================================================================
# CARDS DE DESTAQUE POR TICKER
# ================================================================
st.subheader("📌 Visão Geral")
st.caption("Período de referência: últimos 12 meses")

colunas_por_linha = 4
for linha_idx in range(0, len(dados_cards), colunas_por_linha):
    grupo = dados_cards[linha_idx: linha_idx + colunas_por_linha]
    cols  = st.columns(colunas_por_linha)

    for i, d in enumerate(grupo):
        ticker_label = d["ticker"].replace(".SA", "")

        with cols[i]:
            with st.container(border=True):
                st.subheader(f"🏷️ {ticker_label}")
                st.caption(d["nome"])

                col_a, col_b = st.columns(2)
                with col_a:
                    with st.container(border=True):
                        st.caption("📈 Máxima (12m)")
                        st.write(f"**{real(d['maior_valor'])}**")
                with col_b:
                    with st.container(border=True):
                        st.caption("📉 Mínima (12m)")
                        st.write(f"**{real(d['menor_valor'])}**")

                with st.container(border=True):
                    if d["ultimo_valor"] is not None and d["variacao_dia_pct"] is not None:
                        st.metric(
                            label="💹 Preço Atual",
                            value=real(d["ultimo_valor"]),
                            delta=f"{d['variacao_dia_pct']:+.2f}% hoje",
                        )
                    else:
                        st.caption("💹 Preço Atual")
                        st.write(real(d["ultimo_valor"]) if d["ultimo_valor"] else "N/A")

                with st.container(border=True):
                    st.caption("↔️ Amplitude do período")
                    st.write(f"{real(d['diferenca_valores'])}  ({porcentagem(d['diferenca_pct'])})")

st.divider()

# ================================================================
# TABELA RESUMO COMPLETO
# ================================================================
if dataframes:
    st.subheader("📋 Tabela Resumo Completo")
    st.caption("Período de referência: últimos 12 meses")
    resultados = pd.concat(dataframes, ignore_index=True)
    st.dataframe(resultados, use_container_width=True, hide_index=True)
else:
    st.error("❌ Nenhum dado pôde ser carregado. Tente novamente mais tarde.")