import streamlit as st
import yfinance as yf
from config import real, dolar
from modulos.btc import obter_dados_bitcoin
from modulos.ipca import obter_ipca
from modulos.scraping_ntnb import scrape_tesouro_ipca

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help":     None,
        "Report a bug": None,
        "About": (
            "**Sistema de Investimento** — Desenvolvido para análise de FIIs, "
            "Ações, Índices Econômicos e Criptomoedas.\n\n"
            "Versão 1.0"
        )
    }
)

# ── Coleta de dados ──────────────────────────────────────────────
loading = st.empty()
loading.info("📡 Buscando dados de mercado...")

btc_price    = None
usd_price    = None
ipca_value   = "N/A"
tesouro_2032 = "N/A"

try:
    dados_btc, _, _ = obter_dados_bitcoin()
    if dados_btc is not None and not dados_btc.empty:
        btc_price = dados_btc["Close"].iloc[0].item()
except Exception:
    pass

try:
    obj_dolar   = yf.Ticker("USDBRL=X")
    dados_dolar = obj_dolar.history(period="5d")
    if dados_dolar is not None and not dados_dolar.empty:
        usd_price = dados_dolar["Close"].iloc[-1]
except Exception:
    pass

try:
    _, ipca_5anos, _, _ = obter_ipca()
    if ipca_5anos is not None and not ipca_5anos.empty:
        ipca_value = f"{float(ipca_5anos.iloc[-1].values[0]):.2f} %"
except Exception:
    pass

try:
    titulos_info = scrape_tesouro_ipca()
    if titulos_info:
        titulo_2032 = next(
            (taxa for titulo, taxa in titulos_info if "2032" in titulo), None
        )
        tesouro_2032 = f"IPCA + {titulo_2032}%" if titulo_2032 else "N/D"
except Exception:
    tesouro_2032 = "N/D"

loading.empty()

# ── Cards de indicadores ─────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    with st.container(border=True):
        st.metric(
            label="🪙 Bitcoin — Preço Atual",
            value=dolar(btc_price) if btc_price is not None else "N/A",
        )

with col2:
    with st.container(border=True):
        st.metric(
            label="💵 Dólar (USD/BRL)",
            value=real(usd_price) if usd_price is not None else "N/A",
        )

with col3:
    with st.container(border=True):
        st.metric(
            label="📈 IPCA — Último Valor",
            value=ipca_value,
            help="Último valor mensal do IPCA disponível no Banco Central."
        )

with col4:
    with st.container(border=True):
        st.metric(
            label="💹 Tesouro IPCA+ 2032",
            value=tesouro_2032,
            help="Última taxa disponível para o título Tesouro IPCA+ com vencimento em 2032."
        )

# ================================================================
# LOGO CENTRALIZADA
# ================================================================
col_esq, col_centro, col_dir = st.columns([1, 1.5, 1])

with col_centro:
    st.image(
        "img/logo_real_state_JR_transparente.png",
        use_container_width=True
    )