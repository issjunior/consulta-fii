import yfinance as yf
import pandas as pd
import streamlit as st
from config import *
from modulos.scraping_fear_greed_btc import *
from modulos.btc import *

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

tab1, tab2, tab3 = st.tabs(["📈 BTC", "📈 Dólar", "📈 FII 1"])

with tab1:

    # Obtém os dados do Bitcoin
    dados_btc, data_inicio, data_corte = obter_dados_bitcoin()

    # Primeira linha
    # Métricas BTC
    if not dados_btc.empty:
        st.subheader("Métricas do Bitcoin")
        col1, col2, col3, col4 = st.columns(4)
        
        # Obtém os valores e converte para float para as métricas
        ultimo_preco = dados_btc['Close'].iloc[0].item()
        penultimo_preco = dados_btc['Close'].iloc[1].item()
        delta_preco = ultimo_preco - penultimo_preco
        primeiro_preco = dados_btc['Close'].iloc[-1].item()
        preco_maximo = dados_btc['High'].max().item()
        preco_minimo = dados_btc['Low'].min().item()
        
        with col1:
            st.metric(label="Preço Atual", value=dolar(ultimo_preco), delta=dolar(delta_preco))
        with col2:
            variacao = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100
            st.metric(label="Variação no Período", value=porcentagem(variacao))
        with col3:
            st.metric(label="Máxima no Período", value=dolar(preco_maximo))
        with col4:
            st.metric(label="Mínima no Período", value=dolar(preco_minimo))

    # Adiciona informações sobre o período dos dados
    st.caption(f"Dados do período: {data_inicio.strftime('%d/%m/%Y')} até {data_corte.strftime('%d/%m/%Y')} (últimos 2 anos)")

    # Segunda linha
    if not dados_btc.empty:
            dados_btc.columns = ["Fechamento", "Máximo", "Mínimo"] # renomeia colunas
            st.dataframe(dados_btc, use_container_width=True)  # datagrama
    else:
            st.error("Dados do Bitcoin não disponíveis para exibição.")

# Terceira linha
    col1, col2 = st.columns(2)

    with col1:
    # Exibir o gráfico índice Fear & Greed no Streamlit
        st.markdown('<img src="https://alternative.me/crypto/fear-and-greed-index.png" alt="Gráfico de medo & ganância do Bitcoin" />', unsafe_allow_html=True)

    with col2:
        st.subheader("Índice Fear & Greed Cripto")
        # Chama a função que retorna os valores
        btc_fear_greed_now, btc_fear_greed_yesterday, btc_fear_greed_last_week, btc_fear_greed_last_month = alternative()

        st.metric(label="Hoje", value=btc_fear_greed_now)
        st.metric(label="Ontem", value=btc_fear_greed_yesterday)
        st.metric(label="Última semana", value=btc_fear_greed_last_week)
        st.metric(label="Último mês", value=btc_fear_greed_last_month)
        st.caption("Fonte: <a href='https://alternative.me/crypto/' target='_blank'>alternative.me</a>.", unsafe_allow_html=True)


st.divider()

with tab2:
    
    # Ticker do dólar em relação ao real
    ticker = "USDBRL=X"

    # Obtendo os dados históricos do dólar
    dolar = yf.Ticker(ticker)
    dados_dolar = dolar.history(period="2y")  # Período de 2 anos

    # Ocultando as colunas desnecessárias
    colunas_para_exibir = ["Open", "High", "Low", "Close"]
    dados_filtrados = dados_dolar[colunas_para_exibir]

    # Ordenando as datas em ordem decrescente (mais recentes primeiro)
    dados_filtrados = dados_filtrados.sort_index(ascending=False)

    # Formatando os valores no padrão de moeda brasileira
    dados_filtrados_formatados = dados_filtrados.copy()
    for coluna in dados_filtrados_formatados.columns:
        dados_filtrados_formatados[coluna] = dados_filtrados_formatados[coluna].map(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

    # Exibindo a tabela de dados
    st.write("### Dados Históricos do Dólar (USD/BRL)")
    st.dataframe(dados_filtrados_formatados)

    # Plotando o gráfico da cotação
    st.write("### Gráfico da Cotação do Dólar nos Últimos 2 Anos")
    st.line_chart(dados_filtrados["Close"])

    st.caption("Cotação do Dólar Americano nos Últimos 2 Anos")

with tab3:
    st.title("Ativo 2")