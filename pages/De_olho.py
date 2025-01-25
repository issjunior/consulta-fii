import yfinance as yf
import streamlit as st
from config import *
from modulos.scraping_fear_greed_btc import *
from modulos.btc import *
import plotly.graph_objects as go

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

# Cotação dólar
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

    # Calculando as datas do período
    data_inicio = dados_dolar.index.min()
    data_corte = dados_dolar.index.max()

    # Formatando os valores no padrão de moeda brasileira
    def formatar_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    dados_filtrados_formatados = dados_filtrados.copy()
    for coluna in dados_filtrados_formatados.columns:
        dados_filtrados_formatados[coluna] = dados_filtrados_formatados[coluna].map(formatar_moeda)

    # Exibindo a tabela de dados formatados
    st.caption(f"Dados do período: {data_inicio.strftime('%d/%m/%Y')} até {data_corte.strftime('%d/%m/%Y')} (últimos 2 anos)")
    st.subheader("Dados Históricos do Dólar (USD/BRL)")
    #st.table(dados_filtrados_formatados)
    st.dataframe(dados_filtrados_formatados)

    # Plotando o gráfico da cotação com Plotly
    st.subheader("Histórico de cotação do Dólar")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dados_filtrados.index,
        y=dados_filtrados["Close"],
        mode="lines",
        name="Fechamento",
        hovertemplate="<b>Data:</b> %{x}<br><b>Valor Cota:</b> R$ %{y:.2f}<extra></extra>"
    ))
    fig.update_layout(
        title="Cotação do Dólar Americano nos Últimos 2 Anos",
        xaxis_title="Data",
        yaxis_title="Cotação (R$)",
        #template="plotly_white",
        xaxis_rangeslider_visible=True,  # Habilita o controle de zoom (range slider)
        xaxis_range=[data_corte - pd.DateOffset(years=1), data_corte]  # Limita a visualização para 1 ano
    )
    st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.title("Ativo 2")