from config import *
from modulos.scraping_ntnb import *
from modulos.selic import *
from modulos.ipca import *
from modulos.cdi import *
import streamlit as st
import pandas as pd

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("📊 Índices Econômicos")
st.caption("Acompanhe os principais indicadores da economia brasileira.")

st.divider()

# ================================================================
# ABAS
# ================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📈 IPCA", "📈 SELIC", "📈 CDI", "📈 IFIX"])

# ================================================================
# HELPERS REUTILIZÁVEIS
# ================================================================
URL_SGS = (
    "https://www3.bcb.gov.br/sgspub/localizarseries/"
    "localizarSeries.do?method=prepararTelaLocalizarSeries"
)

def caption_fonte_bcb():
    st.caption(
        f"Fonte: Banco Central do Brasil "
        f"<a href='{URL_SGS}' target='_blank'>(SGS)</a>.",
        unsafe_allow_html=True,
    )

def card_ultimo_valor(label: str, serie: pd.DataFrame):
    """Exibe o último valor da série em um st.metric dentro de um container."""
    try:
        ultimo = float(serie.iloc[-1].values[0])
        with st.container(border=True):
            st.metric(label=label, value=f"{ultimo:.2f} %")
    except Exception:
        pass

# ================================================================
# TAB 1 — IPCA
# ================================================================
with tab1:
    loading = st.empty()
    loading.info("📡 Buscando dados do IPCA...")

    try:
        ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte = obter_ipca()
        loading.empty()
    except Exception as e:
        loading.empty()
        st.error(f"❌ Erro ao buscar dados do IPCA: {e}")
        ipca_filtrado_formatado = None
        ipca_5anos              = None

    st.subheader("📈 IPCA")
    st.caption(
        "Índice Nacional de Preços ao Consumidor Amplo — principal indicador de inflação "
        "do Brasil, medindo a variação de preços de bens e serviços para o consumidor final."
    )

    # Card com último valor
    if ipca_5anos is not None and not ipca_5anos.empty:
        card_ultimo_valor("Último IPCA registrado", ipca_5anos)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if ipca_filtrado_formatado is not None and not ipca_filtrado_formatado.empty:
            ipca_filtrado_formatado.columns = ["Código SGS IPCA - 13522"]
            st.dataframe(
                ipca_filtrado_formatado,
                height=350,
                use_container_width=True,
            )
            caption_fonte_bcb()
        else:
            st.warning("⚠️ Dados do IPCA não disponíveis.")

    with col2:
        if ipca_5anos is not None and not ipca_5anos.empty:
            try:
                fig = criar_grafico_ipca(ipca_5anos, data_inicio_5anos, data_corte)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao gerar gráfico do IPCA: {e}")
        else:
            st.warning("⚠️ Gráfico do IPCA não disponível.")

# ================================================================
# TAB 2 — SELIC
# ================================================================
with tab2:
    loading = st.empty()
    loading.info("📡 Buscando dados da SELIC...")

    try:
        selic_filtrado_formatado, selic_5anos, data_inicio_5anos, data_corte = obter_selic()
        loading.empty()
    except Exception as e:
        loading.empty()
        st.error(f"❌ Erro ao buscar dados da SELIC: {e}")
        selic_filtrado_formatado = None
        selic_5anos              = None

    st.subheader("📈 SELIC")
    st.caption(
        "Sistema Especial de Liquidação e de Custódia — taxa básica de juros da economia "
        "brasileira, usada como referência para outras taxas de juros e definida pelo Banco Central."
    )

    # Card com último valor
    if selic_filtrado_formatado is not None and not selic_filtrado_formatado.empty:
        card_ultimo_valor("Última SELIC registrada", selic_filtrado_formatado)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if selic_filtrado_formatado is not None and not selic_filtrado_formatado.empty:
            selic_filtrado_formatado.columns = ["Código SGS SELIC - 432"]
            st.dataframe(
                selic_filtrado_formatado,
                height=350,
                use_container_width=True,
            )
            caption_fonte_bcb()
        else:
            st.warning("⚠️ Dados da SELIC não disponíveis.")

    with col2:
        if selic_filtrado_formatado is not None and not selic_filtrado_formatado.empty:
            try:
                data_inicio_12meses = data_corte - pd.DateOffset(years=1)
                fig_selic = criar_grafico_selic(
                    selic_filtrado_formatado, data_inicio_12meses, data_corte
                )
                st.plotly_chart(fig_selic, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao gerar gráfico da SELIC: {e}")
        else:
            st.warning("⚠️ Gráfico da SELIC não disponível.")

# ================================================================
# TAB 3 — CDI
# ================================================================
with tab3:
    loading = st.empty()
    loading.info("📡 Buscando dados do CDI...")

    try:
        cdi_filtrado_formatado, cdi_5anos, data_inicio_5anos, data_corte = obter_cdi()
        loading.empty()
    except Exception as e:
        loading.empty()
        st.error(f"❌ Erro ao buscar dados do CDI: {e}")
        cdi_filtrado_formatado = None
        cdi_5anos              = None

    st.subheader("📈 CDI")
    st.caption(
        "Certificado de Depósito Interbancário — título de curto prazo emitido por bancos "
        "para regularizar o fluxo de caixa entre eles. Serve como referência para "
        "investimentos de renda fixa."
    )

    # Card com último valor
    if cdi_filtrado_formatado is not None and not cdi_filtrado_formatado.empty:
        card_ultimo_valor("Último CDI registrado", cdi_filtrado_formatado)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if cdi_filtrado_formatado is not None and not cdi_filtrado_formatado.empty:
            st.dataframe(
                cdi_filtrado_formatado,
                height=350,
                use_container_width=True,
            )
            caption_fonte_bcb()
        else:
            st.warning("⚠️ Dados do CDI não disponíveis.")

    with col2:
        if cdi_filtrado_formatado is not None and not cdi_filtrado_formatado.empty:
            try:
                data_inicio_12meses = data_corte - pd.DateOffset(years=1)
                fig_cdi = criar_grafico_cdi(
                    cdi_filtrado_formatado, data_inicio_12meses, data_corte
                )
                st.plotly_chart(fig_cdi, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao gerar gráfico do CDI: {e}")
        else:
            st.warning("⚠️ Gráfico do CDI não disponível.")

# ================================================================
# TAB 4 — IFIX
# ================================================================
with tab4:
    st.subheader("📈 IFIX")
    st.caption(
        "Indicador que mede a performance média dos fundos imobiliários (FIIs) "
        "listados na Bolsa de Valores brasileira (B3)."
    )

    st.divider()

    st.info("🚧 Dados do IFIX em desenvolvimento. Em breve disponível.")