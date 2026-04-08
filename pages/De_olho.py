import yfinance as yf
import streamlit as st
from config import *
from modulos.scraping_fear_greed_btc import *
from modulos.btc import *
import plotly.graph_objects as go

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("🪙 Mercado — BTC, Dólar e FIIs")
st.caption("Acompanhe as cotações e indicadores de mercado em tempo real.")

st.divider()

# ================================================================
# ABAS
# ================================================================
tab1, tab2, tab3 = st.tabs(["₿ Bitcoin", "💵 Dólar", "🏢 FII"])

# ================================================================
# TAB 1 — BITCOIN
# ================================================================
with tab1:

    st.subheader("₿ Bitcoin (BTC)")
    st.caption("Dados históricos e indicadores de sentimento do mercado cripto.")

    st.divider()

    # ── Coleta de dados ──────────────────────────────────────────
    loading = st.empty()
    loading.info("📡 Buscando dados do Bitcoin...")

    try:
        dados_btc, data_inicio, data_corte = obter_dados_bitcoin()
        loading.empty()
    except Exception as e:
        loading.empty()
        st.error(f"❌ Erro ao buscar dados do Bitcoin: {e}")
        dados_btc   = None
        data_inicio = None
        data_corte  = None

    # ── Métricas ─────────────────────────────────────────────────
    if dados_btc is not None and not dados_btc.empty:
        try:
            ultimo_preco    = dados_btc['Close'].iloc[0].item()
            penultimo_preco = dados_btc['Close'].iloc[1].item()
            delta_preco     = ultimo_preco - penultimo_preco
            primeiro_preco  = dados_btc['Close'].iloc[-1].item()
            preco_maximo    = dados_btc['High'].max().item()
            preco_minimo    = dados_btc['Low'].min().item()
            variacao        = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                with st.container(border=True):
                    st.metric(
                        label="💰 Preço Atual",
                        value=dolar(ultimo_preco),
                        delta=dolar(delta_preco)
                    )
            with col2:
                with st.container(border=True):
                    st.metric(
                        label="📊 Variação no Período",
                        value=porcentagem(variacao)
                    )
            with col3:
                with st.container(border=True):
                    st.metric(
                        label="📈 Máxima no Período",
                        value=dolar(preco_maximo)
                    )
            with col4:
                with st.container(border=True):
                    st.metric(
                        label="📉 Mínima no Período",
                        value=dolar(preco_minimo)
                    )

        except Exception as e:
            st.error(f"❌ Erro ao calcular métricas do Bitcoin: {e}")

        if data_inicio and data_corte:
            st.caption(
                f"Dados do período: {data_inicio.strftime('%d/%m/%Y')} "
                f"até {data_corte.strftime('%d/%m/%Y')} (últimos 2 anos)"
            )

        st.divider()

        # ── Tabela histórica ──────────────────────────────────────
        try:
            dados_exibir = dados_btc.copy()
            dados_exibir.columns = ["Fechamento", "Máximo", "Mínimo"]
            st.subheader("📋 Histórico de Preços")
            st.dataframe(dados_exibir, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erro ao exibir tabela do Bitcoin: {e}")

    else:
        st.warning("⚠️ Dados do Bitcoin não disponíveis.")

    st.divider()

    # ── Fear & Greed + Imagem ─────────────────────────────────────
    col_img, col_fg = st.columns(2)

    with col_img:
        with st.container(border=True):
            st.subheader("📊 Índice Fear & Greed — Gráfico")
            st.markdown(
                '<img src="https://alternative.me/crypto/fear-and-greed-index.png" '
                'alt="Gráfico de medo & ganância do Bitcoin" style="width:100%;" />',
                unsafe_allow_html=True
            )

    with col_fg:
        with st.container(border=True):
            st.subheader("📊 Índice Fear & Greed — Valores")

            loading_fg = st.empty()
            loading_fg.info("📡 Buscando índice Fear & Greed...")

            try:
                (
                    btc_fear_greed_now,
                    btc_fear_greed_yesterday,
                    btc_fear_greed_last_week,
                    btc_fear_greed_last_month
                ) = alternative()
                loading_fg.empty()

                c1, c2 = st.columns(2)
                with c1:
                    st.metric(label="🕐 Hoje",          value=btc_fear_greed_now)
                    st.metric(label="📅 Última semana", value=btc_fear_greed_last_week)
                with c2:
                    st.metric(label="⏮️ Ontem",         value=btc_fear_greed_yesterday)
                    st.metric(label="🗓️ Último mês",    value=btc_fear_greed_last_month)

                st.caption(
                    "Fonte: <a href='https://alternative.me/crypto/' target='_blank'>alternative.me</a>.",
                    unsafe_allow_html=True
                )

            except Exception as e:
                loading_fg.empty()
                st.error(f"❌ Erro ao buscar Fear & Greed: {e}")

# ================================================================
# TAB 2 — DÓLAR
# ================================================================
with tab2:

    st.subheader("💵 Dólar (USD/BRL)")
    st.caption("Cotação histórica do Dólar Americano frente ao Real Brasileiro.")

    st.divider()

    loading_dolar = st.empty()
    loading_dolar.info("📡 Buscando dados do Dólar...")

    try:
        ticker_dolar = "USDBRL=X"
        obj_dolar    = yf.Ticker(ticker_dolar)
        dados_dolar  = obj_dolar.history(period="2y")

        loading_dolar.empty()

        if dados_dolar.empty:
            st.warning("⚠️ Dados do Dólar não disponíveis no momento.")
        else:
            # Filtra e ordena
            colunas_exibir  = ["Open", "High", "Low", "Close"]
            dados_filtrados = dados_dolar[colunas_exibir].sort_index(ascending=False)

            data_inicio_dolar = dados_dolar.index.min()
            data_corte_dolar  = dados_dolar.index.max()

            # ── Métricas ──────────────────────────────────────────
            try:
                ultimo_close    = dados_filtrados["Close"].iloc[0]
                penultimo_close = dados_filtrados["Close"].iloc[1]
                delta_close     = ultimo_close - penultimo_close
                maximo_periodo  = dados_filtrados["High"].max()
                minimo_periodo  = dados_filtrados["Low"].min()

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    with st.container(border=True):
                        st.metric(
                            label="💰 Cotação Atual",
                            value=f"R$ {ultimo_close:,.2f}",
                            delta=f"R$ {delta_close:+,.2f}"
                        )
                with col2:
                    with st.container(border=True):
                        variacao_dolar = ((ultimo_close - dados_filtrados["Close"].iloc[-1]) /
                                          dados_filtrados["Close"].iloc[-1]) * 100
                        st.metric(
                            label="📊 Variação no Período",
                            value=f"{variacao_dolar:+.2f}%"
                        )
                with col3:
                    with st.container(border=True):
                        st.metric(label="📈 Máxima no Período", value=f"R$ {maximo_periodo:,.2f}")
                with col4:
                    with st.container(border=True):
                        st.metric(label="📉 Mínima no Período", value=f"R$ {minimo_periodo:,.2f}")

            except Exception as e:
                st.error(f"❌ Erro ao calcular métricas do Dólar: {e}")

            st.caption(
                f"Dados do período: {data_inicio_dolar.strftime('%d/%m/%Y')} "
                f"até {data_corte_dolar.strftime('%d/%m/%Y')} (últimos 2 anos)"
            )

            st.divider()

            # ── Tabela formatada ──────────────────────────────────
            try:
                def formatar_moeda_brl(valor):
                    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                dados_fmt = dados_filtrados.copy()
                for col in dados_fmt.columns:
                    dados_fmt[col] = dados_fmt[col].map(formatar_moeda_brl)
                dados_fmt.index = dados_fmt.index.strftime('%d/%m/%Y')
                dados_fmt.columns = ["Abertura", "Máximo", "Mínimo", "Fechamento"]

                st.subheader("📋 Histórico de Cotações")
                st.dataframe(dados_fmt, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao formatar tabela do Dólar: {e}")

            st.divider()

            # ── Gráfico ───────────────────────────────────────────
            try:
                st.subheader("📈 Histórico de Cotação")

                fig_dolar = go.Figure()
                fig_dolar.add_trace(go.Scatter(
                    x=dados_filtrados.index,
                    y=dados_filtrados["Close"],
                    mode="lines",
                    name="Fechamento",
                    line=dict(color='#00D9FF', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(0, 217, 255, 0.10)',
                    hovertemplate=(
                        "<b>Data:</b> %{x}<br>"
                        "<b>Cotação:</b> R$ %{y:.2f}<extra></extra>"
                    )
                ))
                fig_dolar.update_layout(
                    xaxis_title="Data",
                    yaxis_title="Cotação (R$)",
                    hovermode='x unified',
                    template='plotly_dark',
                    height=500,
                    plot_bgcolor='rgba(17, 17, 17, 0.5)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    xaxis=dict(
                        rangeslider=dict(visible=True),
                        type='date',
                        range=[
                            data_corte_dolar - pd.DateOffset(years=1),
                            data_corte_dolar
                        ],
                        gridcolor='rgba(255, 255, 255, 0.1)',
                        showgrid=True
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255, 255, 255, 0.1)',
                        showgrid=True,
                        automargin=True
                    ),
                    font=dict(size=12, color='#FFFFFF'),
                )
                st.plotly_chart(fig_dolar, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao gerar gráfico do Dólar: {e}")

    except Exception as e:
        loading_dolar.empty()
        st.error(f"❌ Erro ao buscar dados do Dólar: {e}")

# ================================================================
# TAB 3 — FII (em desenvolvimento)
# ================================================================
with tab3:
    st.subheader("🏢 FII")
    st.caption("Indicadores e histórico de fundos imobiliários.")

    st.divider()

    st.info("🚧 Seção em desenvolvimento. Em breve disponível.")