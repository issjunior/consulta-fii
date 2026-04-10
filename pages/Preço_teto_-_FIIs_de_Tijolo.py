import streamlit as st
from config import *
from modulos.scraping_ntnb import *
from modulos.scraping_valorpatrimonial import *
from modulos.dividendos import *
from modulos.calculos import *
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from groq import Groq

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# ================================================================
# CONFIGURAÇÃO DO GROQ
# ================================================================
IA_DISPONIVEL = False
cliente_ia    = None
MODELO_GROQ   = "llama-3.3-70b-versatile"

try:
    cliente_ia    = Groq(api_key=st.secrets["GROQ_API_KEY"])
    IA_DISPONIVEL = True

except KeyError:
    st.error("❌ Chave `GROQ_API_KEY` não encontrada em `.streamlit/secrets.toml`.")
except Exception as e:
    st.error(f"❌ Erro ao configurar a IA: {e}")

# ================================================================
# HELPERS — IA
# ================================================================
def montar_contexto_fii(dados: dict) -> str:
    """Monta o prompt de sistema com os dados do FII para a IA."""
    return f"""
Você é um assistente especializado em fundos imobiliários (FIIs) brasileiros.
Responda sempre em português, de forma clara e objetiva.
Não forneça recomendações de compra ou venda — apenas análises e explicações educativas.

=== DADOS DO FII CONSULTADO ===
Ticker            : {dados.get('ticker', 'N/A')}
Nome              : {dados.get('nome', 'N/A')}
Preço Atual       : {dados.get('preco_atual', 'N/A')}
Preço Teto Gordon : {dados.get('preco_teto', 'N/A')}
Diferença %       : {dados.get('diferenca_pct', 'N/A')}
Diferença R$      : {dados.get('diferenca_abs', 'N/A')}
Média Dividendos  : {dados.get('media_dividendos', 'N/A')}
DY Anual          : {dados.get('media_div_pct', 'N/A')}
Dividendos 12m    : {dados.get('total_dividendos', 'N/A')}
Magic Number      : {dados.get('cotas_necessarias', 'N/A')} cotas
Valor Magic Number: {dados.get('valor_cotas_magicnumber', 'N/A')}
Cap Rate Ajustado : {dados.get('valor_cap_rate', 'N/A')}
P/VP              : {dados.get('valor_pvp', 'N/A')}
Spread utilizado  : {dados.get('spread', 'N/A')}
Vacância          : {dados.get('vacancia', 'N/A')}
Tx. Crescimento   : {dados.get('tx_crescimento_dy', 'N/A')}
================================

Com base nesses dados, responda à pergunta do usuário.
""".strip()


def gerar_sugestoes(dados: dict) -> list:
    """Gera 3 sugestões de perguntas contextualizadas com base nos dados do FII."""
    try:
        prompt = f"""
Com base nos dados abaixo de um FII brasileiro, gere exatamente 3 sugestões de perguntas 
relevantes e contextualizadas que um investidor faria sobre este fundo.

=== DADOS DO FII ===
Ticker      : {dados.get('ticker', 'N/A')}
Preço Atual : {dados.get('preco_atual', 'N/A')}
Preço Teto  : {dados.get('preco_teto', 'N/A')}
Diferença % : {dados.get('diferenca_pct', 'N/A')}
DY Anual    : {dados.get('media_div_pct', 'N/A')}
P/VP        : {dados.get('valor_pvp', 'N/A')}
Cap Rate    : {dados.get('valor_cap_rate', 'N/A')}
Magic Number: {dados.get('cotas_necessarias', 'N/A')} cotas
====================

Retorne APENAS as 3 perguntas, uma por linha, sem numeração, sem explicações, sem bullets.
""".strip()

        resposta = cliente_ia.chat.completions.create(
            model=MODELO_GROQ,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=256,
        )

        linhas    = resposta.choices[0].message.content.strip().split("\n")
        sugestoes = [l.strip() for l in linhas if l.strip()][:3]
        return sugestoes

    except Exception:
        # Fallback para sugestões fixas em caso de erro
        return [
            "Com base nos dados, este FII está barato ou caro?",
            "Como interpretar o Cap Rate Ajustado deste FII?",
            "O que significa o Magic Number e como utilizá-lo?",
        ]


def perguntar_ia(dados: dict, historico: list, pergunta: str) -> str:
    """Envia a pergunta para o Groq mantendo o histórico da conversa."""
    try:
        contexto = montar_contexto_fii(dados)

        messages = [{"role": "system", "content": contexto}]

        for msg in historico:
            role    = "assistant" if msg["role"] == "model" else msg["role"]
            content = msg["parts"][0] if isinstance(msg["parts"], list) else msg["parts"]
            messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": pergunta})

        resposta = cliente_ia.chat.completions.create(
            model=MODELO_GROQ,
            messages=messages,
            temperature=0.4,
            max_tokens=1024,
        )

        return resposta.choices[0].message.content

    except Exception as e:
        return f"❌ Erro ao consultar a IA: {e}"

# ================================================================
# HEADER
# ================================================================
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
            "contra a inflação."
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
        placeholder="Ex: GARE11, HGLG11, LVBI11",
        label_visibility="collapsed"
    ).upper()

with col_button:
    buscar = st.button("Buscar", use_container_width=True)

col_spread, col_vacancia, col_crescimento = st.columns(3)

with col_spread:
    spread = st.number_input(
        "📌 Spread (prêmio) do FII:",
        value=2.5, min_value=0.0, step=0.1, format="%.2f"
    )

with col_vacancia:
    vacancia = st.number_input(
        "🏚️ Vacância (%):",
        value=0.0, min_value=0.0, step=0.1, format="%.2f"
    )

with col_crescimento:
    tx_crescimento_dy = st.number_input(
        "📈 Taxa de crescimento esperado (próx. 12 meses %):",
        min_value=0.0, value=0.0, step=0.1, format="%.2f"
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
                media_dividendos               = obter_media_dividendos(ticker)

                if media_dividendos is None:
                    st.error(f"❌ Código {ticker_raw} não encontrado.")
                else:
                    total_dividendos        = calcular_total_dividendos(media_dividendos)
                    acao                    = yf.Ticker(ticker)
                    preco_atual             = acao.info.get("currentPrice", None)
                    media_div_pct           = calcular_media_dividendos_porcentagem(total_dividendos, preco_atual)
                    preco_teto              = calcular_preco_teto(total_dividendos, media_ntnb_local, spread, tx_crescimento_dy)
                    cotas_necessarias       = calcular_cotas_necessarias(preco_atual, media_dividendos)
                    valor_cotas_magicnumber = calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual)
                    valor_cap_rate          = calcular_cap_rate_ajustado(media_dividendos, vacancia, preco_atual)
                    valor_pvp               = obter_pvp(ticker)

                    diferenca_abs = None
                    diferenca_pct = None
                    if preco_atual and preco_teto and preco_teto > 0:
                        diferenca_abs = preco_atual - preco_teto
                        diferenca_pct = ((preco_atual - preco_teto) / preco_teto) * 100

                    nome_fii = acao.info.get('longName', ticker_raw)

                    # ── Salva dados na session_state para o chat ─────────
                    st.session_state["dados_fii"] = {
                        "ticker":                  ticker_raw,
                        "nome":                    nome_fii,
                        "preco_atual":             real(preco_atual) if preco_atual else "N/A",
                        "preco_teto":              real(preco_teto) if preco_teto else "N/A",
                        "diferenca_pct":           f"{diferenca_pct:+.2f}%" if diferenca_pct is not None else "N/A",
                        "diferenca_abs":           f"R$ {diferenca_abs:+.2f}" if diferenca_abs is not None else "N/A",
                        "media_dividendos":        real(media_dividendos) if media_dividendos else "N/A",
                        "media_div_pct":           porcentagem(media_div_pct) if media_div_pct else "N/A",
                        "total_dividendos":        real(total_dividendos) if total_dividendos else "N/A",
                        "cotas_necessarias":       cotas_necessarias,
                        "valor_cotas_magicnumber": real(valor_cotas_magicnumber) if valor_cotas_magicnumber else "N/A",
                        "valor_cap_rate":          porcentagem(valor_cap_rate) if valor_cap_rate else "N/A",
                        "valor_pvp":               porcentagem(valor_pvp) if valor_pvp else "N/A",
                        "spread":                  porcentagem(spread),
                        "vacancia":                porcentagem(vacancia),
                        "tx_crescimento_dy":       porcentagem(tx_crescimento_dy),
                    }

                    # ── Limpa histórico ao buscar novo ticker ────────────
                    st.session_state["chat_historico"]  = []
                    st.session_state["chat_mensagens"]  = []
                    st.session_state["sugestoes_ia"]    = []
                    st.session_state["sugestoes_ticker"] = None

                    st.success("✅ Dados carregados com sucesso")
                    st.divider()

                    # ── Identificação ────────────────────────────────────
                    st.title(f"Ticker: {ticker_raw}")
                    st.subheader(f"🏢 {nome_fii}")
                    st.divider()

                    # ── Cards linha 1 ────────────────────────────────────
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        with st.container(border=True):
                            st.subheader("📊 P/VP")
                            st.write(porcentagem(valor_pvp) if valor_pvp else "Não disponível")
                    with col2:
                        with st.container(border=True):
                            st.subheader("📈 Cap Rate Ajustado")
                            st.write(porcentagem(valor_cap_rate) if valor_cap_rate else "Não disponível")
                    with col3:
                        with st.container(border=True):
                            st.subheader("🔢 Magic Number")
                            st.write(f"{cotas_necessarias} cotas" if cotas_necessarias else "Não disponível")

                    # ── Cards linha 2 ────────────────────────────────────
                    col4, col5, col6 = st.columns(3)
                    with col4:
                        with st.container(border=True):
                            st.subheader("💰 Média de Dividendos")
                            if media_dividendos:
                                st.write(f"{real(media_dividendos)} (DY anual de {porcentagem(media_div_pct)})")
                            else:
                                st.write("Não disponível")
                    with col5:
                        with st.container(border=True):
                            st.subheader("📥 Dividendos (12 meses)")
                            st.write(real(total_dividendos) if total_dividendos else "Não disponível")
                    with col6:
                        with st.container(border=True):
                            st.subheader("💼 Valor p/ Magic Number")
                            st.write(real(valor_cotas_magicnumber) if valor_cotas_magicnumber else "Não disponível")

                    # ── Cards linha 3 ────────────────────────────────────
                    col7, col8, col9 = st.columns(3)
                    with col7:
                        with st.container(border=True):
                            st.subheader("💹 Preço Atual")
                            st.write(real(preco_atual) if preco_atual else "Não disponível")
                    with col8:
                        with st.container(border=True):
                            st.subheader("🏁 Preço Teto (Gordon)")
                            if preco_teto:
                                st.write(f"{real(preco_teto)} (spread de {porcentagem(spread)})")
                            else:
                                st.write("Não disponível")
                    with col9:
                        with st.container(border=True):
                            if diferenca_pct is not None and diferenca_abs is not None:
                                st.metric(
                                    "Diferença (Preço Atual vs Preço Teto)",
                                    f"{diferenca_pct:+.2f}%",
                                    delta=f"R$ {diferenca_abs:+.2f}",
                                )
                            else:
                                st.write("Diferença não disponível")

                    st.divider()

                    # ── Gráficos ─────────────────────────────────────────
                    st.subheader("📈 Histórico de Cotas e Dividendos (5 anos)")
                    col_g1, col_g2 = st.columns(2)
                    historico_acao = acao.history(period="5y")
                    data_corte     = pd.to_datetime('today').normalize()

                    with col_g1:
                        if not historico_acao.empty:
                            historico_clean = historico_acao[['Close']].dropna()
                            preco_min = float(historico_clean['Close'].min())
                            preco_max = float(historico_clean['Close'].max())
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
                                hovertemplate="<b>Data:</b> %{x}<br><b>Valor Cota:</b> R$ %{y:.2f}<extra></extra>"
                            ))
                            if preco_teto:
                                fig_cota.add_hline(
                                    y=preco_teto, line_dash="dash", line_color="#00FF41",
                                    annotation_text=f"Preço Teto: R$ {preco_teto:.2f}",
                                    annotation_position="right",
                                    annotation_font=dict(size=11, color="#00FF41")
                                )
                            if preco_atual:
                                fig_cota.add_hline(
                                    y=preco_atual, line_dash="dash", line_color="#FF6B6B",
                                    annotation_text=f"Preço Atual: R$ {preco_atual:.2f}",
                                    annotation_position="right",
                                    annotation_font=dict(size=11, color="#FF6B6B")
                                )
                            fig_cota.update_layout(
                                xaxis_title="Data", yaxis_title="Preço (R$)",
                                hovermode='x unified', template='plotly_dark',
                                height=500, margin=dict(b=80),
                                plot_bgcolor='rgba(17, 17, 17, 0.5)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                                xaxis=dict(
                                    rangeslider=dict(visible=True), type='date',
                                    range=[data_corte - pd.DateOffset(years=1), data_corte],
                                    gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True
                                ),
                                yaxis=dict(
                                    gridcolor='rgba(255, 255, 255, 0.1)',
                                    range=[y_min, y_max], automargin=True, showgrid=True
                                ),
                                font=dict(size=12, color='#FFFFFF'),
                                legend=dict(
                                    orientation="h", yanchor="bottom", y=-0.25,
                                    xanchor="center", x=0.5,
                                    bgcolor="rgba(30, 30, 30, 0.9)",
                                    bordercolor="rgba(255, 255, 255, 0.2)",
                                    borderwidth=1, font=dict(color='#FFFFFF')
                                )
                            )
                            st.plotly_chart(fig_cota, use_container_width=True)
                        else:
                            st.warning("⚠️ Histórico da cota não disponível.")

                    with col_g2:
                        dividendos = acao.dividends
                        if not dividendos.empty:
                            dividendos.index = dividendos.index.tz_localize(None)
                            dividendos_10a   = dividendos[
                                dividendos.index >= data_corte - pd.DateOffset(years=10)
                            ]
                            fig_div = go.Figure()
                            fig_div.add_trace(go.Scatter(
                                x=dividendos_10a.index, y=dividendos_10a,
                                mode='markers+lines', name='Dividendos',
                                line=dict(color='#FFD700', width=2),
                                marker=dict(size=6, color='#FFD700'),
                                fill='tozeroy', fillcolor='rgba(255, 215, 0, 0.10)',
                                hovertemplate="<b>Data:</b> %{x}<br><b>Dividendo:</b> R$ %{y:.2f}<extra></extra>"
                            ))
                            fig_div.update_layout(
                                xaxis_title="Data", yaxis_title="Dividendos (R$)",
                                hovermode='x unified', template='plotly_dark',
                                height=500, margin=dict(b=80),
                                plot_bgcolor='rgba(17, 17, 17, 0.5)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                                xaxis=dict(
                                    rangeslider=dict(visible=True), type='date',
                                    range=[data_corte - pd.DateOffset(years=1), data_corte],
                                    gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True
                                ),
                                yaxis=dict(
                                    gridcolor='rgba(255, 255, 255, 0.1)',
                                    automargin=True, showgrid=True
                                ),
                                font=dict(size=12, color='#FFFFFF'),
                                legend=dict(
                                    orientation="h", yanchor="bottom", y=-0.25,
                                    xanchor="center", x=0.5,
                                    bgcolor="rgba(30, 30, 30, 0.9)",
                                    bordercolor="rgba(255, 255, 255, 0.2)",
                                    borderwidth=1, font=dict(color='#FFFFFF')
                                )
                            )
                            st.plotly_chart(fig_div, use_container_width=True)
                        else:
                            st.warning("⚠️ Nenhum dividendo pago para este ticker.")

                    # ── Tabela Resumo ────────────────────────────────────
                    st.divider()
                    st.subheader("📋 Resumo Completo")
                    df_resumo = {
                        "Métrica": [
                            "Gestora", "Ticker", "Cotação Atual",
                            "Variação da Cota (52 sem.)", "Média de Dividendos",
                            "Dividendos Recebidos (últ. 12 meses)", "Preço Teto (Gordon)",
                            "Diferença % (Atual vs Teto)", "Diferença R$ (Atual - Teto)",
                            "Magic Number", "Valor para Magic Number",
                            "Cap Rate Ajustado (c/ vacância)", "P/VP"
                        ],
                        "Valor": [
                            acao.info.get('longName', 'N/A'),
                            ticker_raw,
                            real(preco_atual) if preco_atual else "N/A",
                            f"{real(acao.info.get('fiftyTwoWeekLow', 'N/A'))} - {real(acao.info.get('fiftyTwoWeekHigh', 'N/A'))}",
                            f"{real(media_dividendos)} (DY anual de {porcentagem(media_div_pct)})" if media_dividendos else "N/A",
                            real(total_dividendos) if total_dividendos else "N/A",
                            f"{real(preco_teto)} (spread de {porcentagem(spread)})" if preco_teto else "N/A",
                            f"{diferenca_pct:+.2f}%" if diferenca_pct is not None else "N/A",
                            f"R$ {diferenca_abs:+.2f}" if diferenca_abs is not None else "N/A",
                            f"{cotas_necessarias} cotas" if cotas_necessarias else "N/A",
                            real(valor_cotas_magicnumber) if valor_cotas_magicnumber else "N/A",
                            porcentagem(valor_cap_rate) if valor_cap_rate else "N/A",
                            porcentagem(valor_pvp) if valor_pvp else "N/A",
                        ]
                    }
                    st.dataframe(df_resumo, use_container_width=True, hide_index=True)

            except KeyError:
                st.error(f"❌ Ticker '{ticker_raw}' não encontrado. Verifique se está correto.")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {e}")

# ================================================================
# SEÇÃO DE CHAT COM IA
# ================================================================
if "dados_fii" in st.session_state and st.session_state["dados_fii"]:

    st.divider()
    st.subheader("🤖 Assistente IA — Análise do FII")

    dados_fii = st.session_state["dados_fii"]

    if not IA_DISPONIVEL:
        st.error(
            "❌ Chave da API Groq não configurada. "
            "Adicione `GROQ_API_KEY` em `.streamlit/secrets.toml`."
        )
    else:
        st.caption(
            f"💬 Converse com a IA sobre o **{dados_fii['ticker']}** — "
            "ela já conhece todos os dados calculados acima."
        )

        if "chat_mensagens" not in st.session_state:
            st.session_state["chat_mensagens"] = []
        if "chat_historico" not in st.session_state:
            st.session_state["chat_historico"] = []

        # ── Sugestões dinâmicas geradas pela IA ─────────────────────
        st.markdown("**💡 Sugestões de perguntas:**")

        # Gera sugestões apenas uma vez por ticker consultado
        if "sugestoes_ia" not in st.session_state or \
           st.session_state.get("sugestoes_ticker") != dados_fii["ticker"]:
            with st.spinner("💡 Gerando sugestões personalizadas..."):
                st.session_state["sugestoes_ia"]     = gerar_sugestoes(dados_fii)
                st.session_state["sugestoes_ticker"] = dados_fii["ticker"]

        sugestoes          = st.session_state["sugestoes_ia"]
        sugestao_escolhida = None

        col_s1, col_s2, col_s3 = st.columns(3)

        with col_s1:
            if st.button(sugestoes[0], use_container_width=True):
                sugestao_escolhida = sugestoes[0]
        with col_s2:
            if st.button(sugestoes[1], use_container_width=True):
                sugestao_escolhida = sugestoes[1]
        with col_s3:
            if st.button(sugestoes[2], use_container_width=True):
                sugestao_escolhida = sugestoes[2]

        # ── Exibir histórico de mensagens ────────────────────────────
        for msg in st.session_state["chat_mensagens"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # ── Input do usuário ou sugestão clicada ─────────────────────
        pergunta_usuario = st.chat_input("Digite sua pergunta sobre este FII...")
        pergunta_final   = sugestao_escolhida or pergunta_usuario

        if pergunta_final:
            st.session_state["chat_mensagens"].append({
                "role": "user",
                "content": pergunta_final
            })
            with st.chat_message("user"):
                st.markdown(pergunta_final)

            with st.chat_message("assistant"):
                with st.spinner("🤖 Consultando IA..."):
                    resposta = perguntar_ia(
                        dados_fii,
                        st.session_state["chat_historico"],
                        pergunta_final
                    )
                st.markdown(resposta)

            st.session_state["chat_mensagens"].append({
                "role": "assistant",
                "content": resposta
            })
            st.session_state["chat_historico"].append(
                {"role": "user",  "parts": [pergunta_final]}
            )
            st.session_state["chat_historico"].append(
                {"role": "model", "parts": [resposta]}
            )

        # ── Botão limpar conversa ────────────────────────────────────
        if st.session_state.get("chat_mensagens"):
            if st.button("🗑️ Limpar conversa", use_container_width=False):
                st.session_state["chat_historico"] = []
                st.session_state["chat_mensagens"] = []
                st.rerun()