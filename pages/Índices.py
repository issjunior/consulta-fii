from config import *
from modulos.scraping_ntnb import *
from modulos.selic import *
from modulos.ipca import *
import streamlit as st

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

tab1, tab2, tab3, tab4 = st.tabs(["📈 IPCA", "📈 SELIC", "📈 CDI", "📈 IFIX"])

with tab1:
    # Obtém os dados IPCA
    ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte = obter_ipca()

    # Obtém o último valor bruto do IPCA antes da formatação
    ultimo_ipca_bruto = ipca_5anos.iloc[-1].values[0]

    # Formata o último valor do IPCA
    ultimo_ipca_formatado = f"{ultimo_ipca_bruto:.2f} %"

    # Layout 1 em duas colunas
    col1, col2 = st.columns(2)
    # Coluna 1: Exibe os dados IPCA
    with col1:
        st.title("IPCA")
        st.caption("Índice Nacional de Preços ao Consumidor Amplo é o principal indicador de inflação do Brasil, medindo a variação de preços de bens e serviços para o consumidor final.")
        ipca_filtrado_formatado.columns = ["Código SGS IPCA - 13522"] # renomeia coluna
        st.dataframe(ipca_filtrado_formatado, height=245, use_container_width=True)
        st.caption(f"Fonte: Banco Central do Brasil <a href='https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries' target='_blank'>(SGS)</a>.</p>", unsafe_allow_html=True)

    # Coluna 2: Exibe o gráfico do IPCA
    with col2:
        if not ipca_5anos.empty:
            fig = criar_grafico(ipca_5anos, data_inicio_5anos, data_corte)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Dados do IPCA não disponíveis.")

st.divider()

with tab2:

    # Obtém os dados da SELIC no meio do mês
    selic_formatado, selic, data_inicio_5anos, data_corte = obter_selic()

    # Layout 3 em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.title("SELIC")
        st.caption("Sistema Especial de Liquidação e de Custódia é a taxa básica de juros da economia brasileira, usada como referência para outras taxas de juros e definida pelo Banco Central.")

        # Exibe o DataFrame da SELIC
        if selic_formatado is not None:
            selic_formatado.columns = ["Código SGS SELIC - 432"]  # Renomeia a coluna
            st.dataframe(selic_formatado, height=245, use_container_width=True)
            st.caption(f"Fonte: Banco Central do Brasil <a href='https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries' target='_blank'>(SGS)</a>.</p>", unsafe_allow_html=True)
        else:
            st.write("Dados da SELIC não disponíveis.")

    with col2:
        # Exibe o gráfico da SELIC no meio do mês
        if selic is not None and not selic.empty:
            # Passa todos os argumentos necessários para criar o gráfico
            fig_selic_meio_mes = criar_grafico_selic(selic, data_inicio_5anos, data_corte)
            st.plotly_chart(fig_selic_meio_mes, use_container_width=True)
        else:
            st.write("Dados da SELIC não disponíveis.")

with tab3:   
    col1, col2 = st.columns(2)
    with col1:
        st.title("CDI")
        st.caption("Conceito de CDI.")

    with col2:
        st.caption("Gráfico")

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.title("IFIX")
        st.caption("Conceito do IFIX.")

    with col2:
        st.caption("Gráfico")
    