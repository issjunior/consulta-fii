from config import *
from modulos.scraping_ntnb import *
from modulos.selic import *
from modulos.ipca import *
from modulos.cdi import *
import streamlit as st
import pandas as pd

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

tab1, tab2, tab3, tab4 = st.tabs(["📈 IPCA", "📈 SELIC", "📈 CDI", "📈 IFIX"])

# -------------------- TAB IPCA --------------------
with tab1:
    ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte = obter_ipca()

    col1, col2 = st.columns(2)
    with col1:
        st.title("IPCA")
        st.caption(
            "Índice Nacional de Preços ao Consumidor Amplo é o principal indicador de inflação do Brasil, medindo a variação de preços de bens e serviços para o consumidor final."
        )

        if ipca_filtrado_formatado is not None and not ipca_filtrado_formatado.empty:
            ipca_filtrado_formatado.columns = ["Código SGS IPCA - 13522"]
            st.dataframe(ipca_filtrado_formatado, height=245, use_container_width=True)
            st.caption(
                f"Fonte: Banco Central do Brasil <a href='https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries' target='_blank'>(SGS)</a>.",
                unsafe_allow_html=True
            )
        else:
            st.write("Dados do IPCA não disponíveis.")

    with col2:
        if ipca_5anos is not None and not ipca_5anos.empty:
            fig = criar_grafico_ipca(ipca_5anos, data_inicio_5anos, data_corte)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Gráfico do IPCA não disponível.")

st.divider()

# -------------------- TAB SELIC --------------------
with tab2:
    selic_filtrado_formatado, selic_5anos, data_inicio_5anos, data_corte = obter_selic()

    col1, col2 = st.columns(2)
    with col1:
        st.title("SELIC")
        st.caption(
            "Sistema Especial de Liquidação e de Custódia é a taxa básica de juros da economia brasileira, usada como referência para outras taxas de juros e definida pelo Banco Central."
        )

        if selic_filtrado_formatado is not None and not selic_filtrado_formatado.empty:
            selic_filtrado_formatado.columns = ["Código SGS SELIC - 432"]
            st.dataframe(selic_filtrado_formatado, height=245, use_container_width=True)
            st.caption(
                f"Fonte: Banco Central do Brasil <a href='https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries' target='_blank'>(SGS)</a>.",
                unsafe_allow_html=True
            )
        else:
            st.write("Dados da SELIC não disponíveis.")

    with col2:
        if selic_filtrado_formatado is not None and not selic_filtrado_formatado.empty:
            data_inicio_12meses = data_corte - pd.DateOffset(years=1)
            fig_selic = criar_grafico_selic(selic_filtrado_formatado, data_inicio_12meses, data_corte)
            st.plotly_chart(fig_selic, use_container_width=True)
        else:
            st.write("Gráfico da SELIC não disponível.")

# -------------------- TAB CDI --------------------
with tab3:
    cdi_filtrado_formatado, cdi_5anos, data_inicio_5anos, data_corte = obter_cdi()

    col1, col2 = st.columns(2)
    with col1:
        st.title("CDI")
        st.caption(
            "Certificado de Depósito Interbancário, um título de curto prazo emitido por bancos para regularizar o fluxo de caixa entre eles."
        )

        if cdi_filtrado_formatado is not None and not cdi_filtrado_formatado.empty:
            st.dataframe(cdi_filtrado_formatado, height=245, use_container_width=True)
            st.caption(
                f"Fonte: Banco Central do Brasil <a href='https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries' target='_blank'>(SGS)</a>.",
                unsafe_allow_html=True
            )
        else:
            st.write("Dados do CDI não disponíveis.")

    with col2:
        if cdi_filtrado_formatado is not None and not cdi_filtrado_formatado.empty:
            data_inicio_12meses = data_corte - pd.DateOffset(years=1)
            fig_cdi = criar_grafico_cdi(cdi_filtrado_formatado, data_inicio_12meses, data_corte)
            st.plotly_chart(fig_cdi, use_container_width=True)
        else:
            st.write("Gráfico do CDI não disponível.")

# -------------------- TAB IFIX --------------------
with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.title("IFIX")
        st.caption(
            "Indicador que mede a performance média dos fundos imobiliários (FIIs) listados na Bolsa de Valores brasileira (B3)."
        )

    with col2:
        st.caption("Gráfico")
