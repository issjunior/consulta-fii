from config import *
from modulos.scraping_ntnb import *
from modulos.selic import *
from bcb import sgs
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Função para obter dados do IPCA
@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def obter_ipca():
    try:
        # Obtém os dados do IPCA (5 anos)
        ipca_5anos = sgs.get(13522)  # busco o código '13522' no https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
        if ipca_5anos is None or ipca_5anos.empty:  # Verifica se a resposta é inválida
            raise ValueError("Nenhum dado foi retornado para o IPCA.")
    except Exception as erro_busca_ipca:
        st.warning("Não foi possível obter os dados do IPCA (5 anos). Verifique sua conexão ou tente novamente mais tarde.")
        st.error(f"Código do erro: {erro_busca_ipca}")
        return None, None, None, None  # Retorna valores default em caso de erro

    # Define a data de corte como a última data disponível
    data_corte = pd.to_datetime("today").normalize()

    # Define o período padrão para 5 anos e os últimos 12 meses
    data_inicio_5anos = data_corte - pd.DateOffset(years=5)  # 5 anos de histórico

    # Filtra os dados para os últimos 5 anos
    ipca_filtrado = ipca_5anos.loc[data_inicio_5anos:data_corte]

    # Inverte a ordem do DataFrame para que as datas mais recentes fiquem em cima
    ipca_filtrado = ipca_filtrado.iloc[::-1]

    # Remove a hora da coluna 'date' apenas no DataFrame para formatar as datas
    ipca_filtrado.index = pd.to_datetime(ipca_filtrado.index).strftime('%d/%m/%Y')

    # Converte a coluna IPCA para float (caso necessário) e formata com o símbolo de '%'
    ipca_filtrado = ipca_filtrado.apply(pd.to_numeric, errors='coerce')  # Garante que os valores sejam numéricos
    ipca_filtrado_formatado = ipca_filtrado.map(lambda x: f"{x:.2f} %" if isinstance(x, (int, float)) else x)

    return ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte

# Função para criar o gráfico
@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def criar_grafico(ipca_5anos, data_inicio_5anos, data_corte):
    # Define o início do intervalo como 12 meses atrás
    data_inicio_12meses = data_corte - pd.DateOffset(years=1)

    # Filtra os dados para os últimos 5 anos
    ipca_filtrado_5anos = ipca_5anos.loc[data_inicio_5anos:data_corte]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ipca_filtrado_5anos.index,
            y=ipca_filtrado_5anos.values.flatten(),  # Transforma em vetor simples
            mode='markers+lines',
            name="IPCA (5 anos)",
        )
    )
    
    # Ajustes no layout do gráfico
    fig.update_layout(
        title="Histórico de IPCA (Últimos 5 anos)",
        xaxis_title="Período",
        yaxis_title="IPCA (%)",
        xaxis_rangeslider_visible=True,  # Controle de zoom (range slider)
        xaxis_range=[data_inicio_12meses, data_corte],  # Mostra os últimos 12 meses inicialmente
    )
    
    return fig

# Função para processar os títulos e adicionar a soma
@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def processar_titulos(titulos_info, ultimo_ipca_formatado):
    # Converte os resultados para um DataFrame
    df_titulos = pd.DataFrame(titulos_info, columns=['Título', 'Porcentagem'])

    # Substitui a vírgula por ponto e converte a coluna 'Porcentagem' para float
    df_titulos['Porcentagem'] = df_titulos['Porcentagem'].str.replace(',', '.').astype(float)

    # Calcula a média da coluna 'Porcentagem'
    media_porcentagem = df_titulos['Porcentagem'].mean()

    # Adiciona a média como última linha do DataFrame
    df_titulos.loc[len(df_titulos)] = ['Média de títulos NTN-B', media_porcentagem]

    # Aplica o símbolo de porcentagem a todos os valores da coluna 'Porcentagem'
    df_titulos['Porcentagem'] = df_titulos['Porcentagem'].map(lambda x: f"{x:.2f} %")

    # Converte o valor do último IPCA para um número, removendo o '%'
    ultimo_ipca_num = float(ultimo_ipca_formatado.replace(' %', ''))

    # Cria a nova coluna 'Último IPCA' com o valor formatado
    df_titulos['Último IPCA'] = ultimo_ipca_formatado

    # Soma da coluna 'Porcentagem' (convertida para número) e 'Último IPCA' (convertido para número)
    df_titulos['Soma'] = df_titulos['Porcentagem'].str.replace(' %', '').astype(float) + ultimo_ipca_num

    # Formata a nova coluna 'Soma' para exibir como porcentagem
    df_titulos['Soma'] = df_titulos['Soma'].map(lambda x: f"{x:.2f} %")

    return df_titulos

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

# Layout 2 em duas colunas
col1, col2 = st.columns(2)

with col1:
    # Exibe os títulos encontrados no investidor10 e suas porcentagens
    media_ntnb_local, titulos_info = exibir_resultados()

    if titulos_info:
        st.title("Títulos IPCA+")
        st.caption("Título de renda fixa emitido pelo governo brasileiro, com rendimento atrelado à inflação medida pelo IPCA (Índice de Preços ao Consumidor Amplo), que é o principal indicador da inflação no Brasil.")

        # Processa os títulos encontrados
        df_titulos = processar_titulos(titulos_info, ultimo_ipca_formatado)

        # Exibe o DataFrame com os títulos, agora incluindo a coluna 'Soma'
        st.dataframe(df_titulos, hide_index=True, use_container_width=True)
        st.caption(f"Fonte: <a href='{url_investidor10}' target='_blank'>Investidor10</a>.</p>", unsafe_allow_html=True)
    else:
        st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

with col2:
    st.markdown("##### coluna 2")

st.divider()

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
    else:
        st.write("Dados da SELIC não disponíveis.")

    with col2:
        # Exibe o gráfico da SELIC no meio do mês
        if selic is not None and not selic.empty:
            fig_selic_meio_mes = criar_grafico_selic(selic)
            st.plotly_chart(fig_selic_meio_mes, use_container_width=True)
        else:
            st.write("Dados da SELIC não disponíveis.")

col1, col2 = st.columns(2)

with col1:
    st.title("CDI")
    st.caption("Conceito de CDI.")

with col2:
    st.markdown("##### Coluna 2")
    