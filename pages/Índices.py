from config import *
from modulos.scraping_ntnb import *
from modulos.selic import *
from modulos.ipca import *
from modulos.cdi import *
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
            fig = criar_grafico_ipca(ipca_5anos, data_inicio_5anos, data_corte)
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

        #selic_filtrado_formatado, selic, data_inicio_5anos, data_corte = obter_selic()
        selic_filtrado_formatado, selic_5anos, data_inicio_5anos, data_corte = obter_selic()

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
        # Gráfico
        if not selic_filtrado_formatado.empty:
            # Define o início do intervalo como 12 meses atrás
            data_inicio_12meses = data_corte - pd.DateOffset(years=1)

            # Cria o gráfico com os dados filtrados
            fig_selic = criar_grafico_selic(selic_filtrado_formatado, data_inicio_12meses, data_corte)
            st.plotly_chart(fig_selic, use_container_width=True)
        else:
            st.write("Dados da taxa SELIC não disponíveis.")

with tab3:   
    
    col1, col2 = st.columns(2)
    
    with col1:

        # Obtém os dados da SELIC
        cdi_filtrado_formatado, cdi_5anos, data_inicio_5anos, data_corte = obter_cdi()

        st.title("CDI")
        st.caption("Certificado de Depósito Interbancário, um título de curto prazo emitido por bancos para regularizar o fluxo de caixa entre eles.")
        # Função para exibir os dados do CDI
        def exibir_cdi():
            # Chama a função para obter os dados do CDI
            cdi_5anos = obter_cdi()
            
            if cdi_5anos is not None:
                # Exibe o DataFrame usando Streamlit de forma interativa
                st.dataframe(cdi_5anos)
            else:
                st.warning("Não foi possível obter os dados do CDI.")

        # Chama a função para exibir os dados do CDI
        st.dataframe(cdi_filtrado_formatado, height=245, use_container_width=True)
        st.caption(f"Fonte: Banco Central do Brasil <a href='https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries' target='_blank'>(SGS)</a>.</p>", unsafe_allow_html=True)

    with col2:

        # Gráfico
        if not cdi_filtrado_formatado.empty:
            # Define o início do intervalo como 12 meses atrás
            data_inicio_12meses = data_corte - pd.DateOffset(years=1)

            # Cria o gráfico com os dados filtrados
            fig_cdi = criar_grafico_cdi(cdi_filtrado_formatado, data_inicio_12meses, data_corte)
            st.plotly_chart(fig_cdi, use_container_width=True)
        else:
            st.write("Dados do CDI não disponíveis.")

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.title("IFIX")
        st.caption("Indicador que mede a performance média dos fundos imobiliários (FIIs) listados na Bolsa de Valores brasileira (B3). Ele é composto por uma carteira teórica de fundos imobiliários selecionados com base em critérios como liquidez e representatividade no mercado.")

    with col2:
        st.caption("Gráfico")
    