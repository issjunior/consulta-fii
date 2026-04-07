import streamlit as st
from config import *
from modulos.scraping_ntnb import *
from modulos.scraping_valorpatrimonial import *
from modulos.dividendos import *
from modulos.calculos import *
import yfinance as yf
import pandas as pd
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
st.title("📊 Cálculo de Preço Teto - FIIs de Tijolo")

# ================================================================
# SEÇÃO EXPLICATIVA
# ================================================================
with st.expander("ℹ️ Entenda o Modelo de Gordon"):
    col_text, col_img = st.columns([1, 1])

    with col_text:
        st.subheader("Modelo de Gordon")
        st.write(
            "Fórmula utilizada para estimar o preço justo ou preço-teto de um ativo "
            "baseado em seus dividendos futuros. No contexto de fundos imobiliários, "
            "esse modelo assume que os dividendos crescem a uma taxa constante ao longo "
            "do tempo ou não sobem."
        )
        st.markdown("""
        ##### Explicando cada termo:
        - **D**: Dividend yield (DY). Consideramos os 12 últimos.
        - **R**: Média NTN-B + SPREAD (risco ou prêmio).
        - **G**: Taxa de crescimento dos dividendos.
        """)
        st.write(
            "Usamos os títulos NTN-B (Tesouro IPCA+) para precificar fundos imobiliários, "
            "porque eles oferecem uma taxa de retorno praticamente livre de risco e protegida "
            "contra a inflação. Essa taxa serve como base de comparação para o retorno esperado "
            "dos FIIs, já que, por terem maior risco, os fundos imobiliários precisam oferecer "
            "uma rentabilidade superior à média NTN-B."
        )

    with col_img:
        st.image("img/modelo_gordon.png")

st.divider()

# ================================================================
# SEÇÃO DE BUSCA E PARÂMETROS
# ================================================================
st.header("🔍 Buscar")

col_input, col_button = st.columns([4, 1])

with col_input:
    ticker_raw = st.text_input(
        "Ticker do FII",
        placeholder="Ex: MXRF11, HGLG11",
        label_visibility="collapsed"
    ).upper()

with col_button:
    buscar = st.button("Buscar", use_container_width=True)

# Parâmetros adicionais em linha
col_spread, col_vacancia, col_crescimento = st.columns(3)

with col_spread:
    spread = st.number_input(
        "📌 Spread (prêmio) do FII:",
        value=2.5,
        min_value=0.0,
        step=0.1,
        format="%.2f"
    )

with col_vacancia:
    vacancia = st.number_input(
        "🏚️ Vacância (%):",
        value=0.0,
        min_value=0.0,
        step=0.1,
        format="%.2f"
    )

with col_crescimento:
    tx_crescimento_dy = st.number_input(
        "📈 Taxa de crescimento esperado (próx. 12 meses %):",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.2f"
    )

# ================================================================
# PROCESSAMENTO DA BUSCA
# ================================================================
if buscar:
    ticker = ticker_raw + ".SA" if ticker_raw else ""

    if not ticker_raw:
        st.warning("⚠️ Digite um ticker válido")
    else:
        with st.spinner(f"Buscando dados de {ticker_raw}..."):
            try:
                media_ntnb_local, titulos_info = exibir_resultados()
                media_dividendos = obter_media_dividendos(ticker)

                if media_dividendos is None:
                    st.error(f"❌ Código {ticker_raw} não encontrado.")
                else:
                    # ── Cálculos principais ──────────────────────────────
                    total_dividendos          = calcular_total_dividendos(media_dividendos)
                    acao                      = yf.Ticker(ticker)
                    preco_atual               = acao.info.get("currentPrice", None)
                    media_div_pct             = calcular_media_dividendos_porcentagem(total_dividendos, preco_atual)
                    preco_teto                = calcular_preco_teto(total_dividendos, media_ntnb_local, spread, tx_crescimento_dy)
                    cotas_necessarias         = calcular_cotas_necessarias(preco_atual, media_dividendos)
                    valor_cotas_magicnumber   = calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual)
                    valor_cap_rate            = calcular_cap_rate_ajustado(media_dividendos, vacancia, preco_atual)
                    valor_pvp                 = obter_pvp(ticker)

                    # ── Diferença Preço Atual x Preço Teto ──────────────
                    diferenca_abs = None
                    diferenca_pct = None
                    if preco_atual and preco_teto and preco_teto > 0:
                        diferenca_abs = preco_atual - preco_teto
                        diferenca_pct = ((preco_atual - preco_teto) / preco_teto) * 100

                    st.success(f"✅ Dados carregados com sucesso")
                    st.divider()

                    # ── Identificação do FII ─────────────────────────────
                    nome_fii = acao.info.get('longName', ticker_raw)
                    st.title(f"Ticker: {ticker_raw}")
                    st.subheader(f"🏢 {nome_fii}")

                    st.divider()

                    # ── Métricas em cards (linha 1) ──────────────────────
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        with st.container(border=True):
                            st.subheader("📊 P/VP")
                            st.write(f"{porcentagem(valor_pvp)}" if valor_pvp else "Informação não disponível")

                    with col2:
                        with st.container(border=True):
                            st.subheader("📈 Cap Rate Ajustado")
                            st.write(f"{porcentagem(valor_cap_rate)}" if valor_cap_rate else "Informação não disponível")

                    with col3:
                        with st.container(border=True):
                            st.subheader("🔢 Magic Number")
                            st.write(f"{cotas_necessarias} cotas" if cotas_necessarias else "Informação não disponível")

                    # ── Métricas em cards (linha 2) ──────────────────────
                    col4, col5, col6 = st.columns(3)

                    with col4:
                        with st.container(border=True):
                            st.subheader("💰 Média de Dividendos")
                            if media_dividendos:
                                st.write(f"{real(media_dividendos)} (DY anual de {porcentagem(media_div_pct)})")
                            else:
                                st.write("Informação não disponível")

                    with col5:
                        with st.container(border=True):
                            st.subheader("📥 Dividendos (12 meses)")
                            st.write(real(total_dividendos) if total_dividendos else "Informação não disponível")

                    with col6:
                        with st.container(border=True):
                            st.subheader("💼 Valor p/ Magic Number")
                            st.write(real(valor_cotas_magicnumber) if valor_cotas_magicnumber else "Informação não disponível")

                    # ── Preço Atual | Preço Teto | Diferença ────────────
                    col7, col8, col9 = st.columns(3)

                    with col7:
                        with st.container(border=True):
                            st.subheader("💹 Preço Atual")
                            st.write(real(preco_atual) if preco_atual else "Informação não disponível")

                    with col8:
                        with st.container(border=True):
                            st.subheader("🏁 Preço Teto (Gordon)")
                            if preco_teto:
                                st.write(f"{real(preco_teto)} (spread de {porcentagem(spread)})")
                            else:
                                st.write("Informação não disponível")

                    with col9:
                        with st.container(border=True):
                            if diferenca_pct is not None and diferenca_abs is not None:
                                st.metric(
                                    "Diferença (Preço Atual vs Preço Teto)",
                                    f"{diferenca_pct:+.2f}%",
                                    delta=f"R$ {diferenca_abs:+.2f}",
                                    delta_color="inverse"  # ✅ Inverte a lógica de cores
                                )
                            else:
                                st.write("Diferença não disponível")

                    st.divider()

                    # ================================================================
                    # GRÁFICOS LADO A LADO: HISTÓRICO DE COTAS E DIVIDENDOS
                    # ================================================================
                    st.subheader("📈 Histórico de Cotas e Dividendos (5 anos)")

                    col_g1, col_g2 = st.columns(2)

                    historico = acao.history(period="5y")
                    data_corte = pd.to_datetime('today').normalize()

                    # ── Gráfico 1: Histórico de Preço ────────────────────
                    with col_g1:
                        if not historico.empty:
                            historico_clean = historico[['Close']].dropna()

                            preco_min = historico_clean['Close'].min()
                            preco_max = historico_clean['Close'].max()
                            amplitude = preco_max - preco_min
                            margem    = amplitude * 0.15
                            y_min     = preco_min - margem
                            y_max     = preco_max + margem

                            if preco_teto and preco_teto > y_max:
                                y_max = preco_teto + (amplitude * 0.1)

                            fig_cota = go.Figure()

                            fig_cota.add_trace(go.Scatter(
                                x=historico_clean.index,
                                y=historico_clean['Close'],
                                mode='lines',
                                name='Preço da Cota',
                                line=dict(color='#00D9FF', width=2.5),
                                fill='tozeroy',
                                fillcolor='rgba(0, 217, 255, 0.15)',
                                hovertemplate=(
                                    "<b>Data:</b> %{x}<br>"
                                    "<b>Valor Cota:</b> R$ %{y:.2f}<extra></extra>"
                                )
                            ))

                            # Linha de preço teto
                            if preco_teto:
                                fig_cota.add_hline(
                                    y=preco_teto,
                                    line_dash="dash",
                                    line_color="#00FF41",
                                    annotation_text=f"Preço Teto (Gordon): R$ {preco_teto:.2f}",
                                    annotation_position="right",
                                    annotation_font=dict(size=11, color="#00FF41")
                                )

                            # Linha de preço atual
                            if preco_atual:
                                fig_cota.add_hline(
                                    y=preco_atual,
                                    line_dash="dash",
                                    line_color="#FF6B6B",
                                    annotation_text=f"Preço Atual: R$ {preco_atual:.2f}",
                                    annotation_position="right",
                                    annotation_font=dict(size=11, color="#FF6B6B")
                                )

                            fig_cota.update_layout(
                                xaxis_title="Data",
                                yaxis_title="Preço (R$)",
                                hovermode='x unified',
                                template='plotly_dark',
                                height=500,
                                margin=dict(b=80),
                                plot_bgcolor='rgba(17, 17, 17, 0.5)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                                xaxis=dict(
                                    rangeslider=dict(visible=True),
                                    type='date',
                                    range=[
                                        data_corte - pd.DateOffset(years=1),
                                        data_corte
                                    ],
                                    gridcolor='rgba(255, 255, 255, 0.1)',
                                    showgrid=True
                                ),
                                yaxis=dict(
                                    gridcolor='rgba(255, 255, 255, 0.1)',
                                    range=[y_min, y_max],
                                    automargin=True,
                                    showgrid=True
                                ),
                                font=dict(size=12, color='#FFFFFF'),
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.25,
                                    xanchor="center",
                                    x=0.5,
                                    bgcolor="rgba(30, 30, 30, 0.9)",
                                    bordercolor="rgba(255, 255, 255, 0.2)",
                                    borderwidth=1,
                                    font=dict(color='#FFFFFF')
                                )
                            )

                            st.plotly_chart(fig_cota, use_container_width=True)
                        else:
                            st.warning("⚠️ Histórico da cota não disponível para este ticker.")

                    # ── Gráfico 2: Histórico de Dividendos ───────────────
                    with col_g2:
                        dividendos = acao.dividends

                        if not dividendos.empty:
                            dividendos.index = dividendos.index.tz_localize(None)
                            dividendos_10a = dividendos[
                                dividendos.index >= data_corte - pd.DateOffset(years=10)
                            ]

                            fig_div = go.Figure()

                            fig_div.add_trace(go.Scatter(
                                x=dividendos_10a.index,
                                y=dividendos_10a,
                                mode='markers+lines',
                                name='Dividendos',
                                line=dict(color='#FFD700', width=2),
                                marker=dict(size=6, color='#FFD700'),
                                fill='tozeroy',
                                fillcolor='rgba(255, 215, 0, 0.10)',
                                hovertemplate=(
                                    "<b>Data:</b> %{x}<br>"
                                    "<b>Dividendo:</b> R$ %{y:.2f}<extra></extra>"
                                )
                            ))

                            fig_div.update_layout(
                                xaxis_title="Data",
                                yaxis_title="Dividendos (R$)",
                                hovermode='x unified',
                                template='plotly_dark',
                                height=500,
                                margin=dict(b=80),
                                plot_bgcolor='rgba(17, 17, 17, 0.5)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                                xaxis=dict(
                                    rangeslider=dict(visible=True),
                                    type='date',
                                    range=[
                                        data_corte - pd.DateOffset(years=1),
                                        data_corte
                                    ],
                                    gridcolor='rgba(255, 255, 255, 0.1)',
                                    showgrid=True
                                ),
                                yaxis=dict(
                                    gridcolor='rgba(255, 255, 255, 0.1)',
                                    automargin=True,
                                    showgrid=True
                                ),
                                font=dict(size=12, color='#FFFFFF'),
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.25,
                                    xanchor="center",
                                    x=0.5,
                                    bgcolor="rgba(30, 30, 30, 0.9)",
                                    bordercolor="rgba(255, 255, 255, 0.2)",
                                    borderwidth=1,
                                    font=dict(color='#FFFFFF')
                                )
                            )

                            st.plotly_chart(fig_div, use_container_width=True)
                        else:
                            st.warning("⚠️ Nenhum dividendo pago para este ticker.")

                    # ================================================================
                    # TABELA RESUMO COMPLETO
                    # ================================================================
                    st.divider()
                    st.subheader("📋 Resumo Completo")

                    df_resumo = {
                        "Métrica": [
                            "Gestora",
                            "Ticker",
                            "Cotação Atual",
                            "Variação da Cota (52 sem.)",
                            "Média de Dividendos",
                            "Dividendos Recebidos (últ. 12 meses)",
                            "Preço Teto (Gordon)",
                            "Diferença % (Atual vs Teto)",
                            "Diferença R$ (Atual - Teto)",
                            "Magic Number",
                            "Valor para Magic Number",
                            "Cap Rate Ajustado (c/ vacância)",
                            "P/VP"
                        ],
                        "Valor": [
                            acao.info.get('longName', 'N/A'),
                            ticker_raw,
                            real(preco_atual) if preco_atual else "N/A",
                            (
                                f"{real(acao.info.get('fiftyTwoWeekLow', 'N/A'))} - "
                                f"{real(acao.info.get('fiftyTwoWeekHigh', 'N/A'))}"
                            ),
                            (
                                f"{real(media_dividendos)} (DY anual de {porcentagem(media_div_pct)})"
                                if media_dividendos else "N/A"
                            ),
                            real(total_dividendos) if total_dividendos else "N/A",
                            (
                                f"{real(preco_teto)} (spread de {porcentagem(spread)})"
                                if preco_teto else "N/A"
                            ),
                            f"{diferenca_pct:+.2f}%" if diferenca_pct is not None else "N/A",
                            f"R$ {diferenca_abs:+.2f}" if diferenca_abs is not None else "N/A",
                            f"{cotas_necessarias} cotas" if cotas_necessarias else "N/A",
                            real(valor_cotas_magicnumber) if valor_cotas_magicnumber else "N/A",
                            porcentagem(valor_cap_rate) if valor_cap_rate else "N/A",
                            porcentagem(valor_pvp) if valor_pvp else "N/A"
                        ]
                    }

                    st.dataframe(df_resumo, use_container_width=True, hide_index=True)

            except KeyError:
                st.error(
                    f"❌ Não foi possível encontrar dados para '{ticker_raw}'. "
                    "Verifique se o ticker está correto."
                )
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")