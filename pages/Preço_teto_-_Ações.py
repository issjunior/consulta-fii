import streamlit as st
from modulos.scraping_acoes import *
import plotly.graph_objects as go

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("📊 Cálculo de Preço Teto - Ações")

# Seção explicativa
with st.expander("ℹ️ Entenda o Método Graham"):
    col_text, col_img = st.columns([1, 1])

    with col_text:
        st.subheader("Método Graham")
        st.write(
            "Determina um valor justo para uma ação com base no lucro por ação (LPA) "
            "e na taxa de crescimento esperada da empresa."
        )

    with col_img:
        st.image("img/formula_graham.png")

st.divider()

# Seção de busca
st.header("🔍 Buscar")

col_input, col_button = st.columns([4, 1])

with col_input:
    ticker = st.text_input(
        "Ticker da Ação",
        placeholder="Ex: PETR4, VALE3",
        label_visibility="collapsed"
    ).upper()

with col_button:
    buscar = st.button("Buscar", use_container_width=True)

# Processamento da busca
if buscar:
    if not ticker:
        st.warning("⚠️ Digite um ticker válido")
    else:
        with st.spinner(f"Buscando dados de {ticker}..."):
            dados = obter_dados_acao(ticker)

        if dados is None:
            st.error(f"❌ Não foi possível obter dados para {ticker}")
        else:
            st.success(f"✅ Dados carregados com sucesso")
            st.caption(
                f"Fonte: [Investidor10](https://investidor10.com.br/acoes/{ticker})"
            )
            st.divider()

            # Segmento em destaque
            st.title(f"Ticker {dados['Ticker']}")
            st.subheader(f"📂 Segmento: {dados['Segmento'] or 'Informação não disponível'}")
            
            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                with st.container(border=True):
                    st.subheader("🏷️ Tag Along")
                    st.write(dados['Tag Along'] or "Informação não disponível")

            with col2:
                with st.container(border=True):
                    st.subheader("🔄 Free Float")
                    st.write(dados['Free Float'] or "Informação não disponível")

            with col3:
                with st.container(border=True):
                    st.subheader("📊 PAYOUT")
                    st.write(dados['PAYOUT'] or "Informação não disponível")

            col4, col5, col6 = st.columns(3)

            with col4:
                with st.container(border=True):
                    st.subheader("📊 ROE")
                    st.write(dados['ROE'] or "Informação não disponível")

            with col5:
                with st.container(border=True):
                    st.subheader("📊 DL / Ebitda")
                    st.write(dados['Dívida Líquida / Ebitda'] or "Informação não disponível")

            with col6:
                with st.container(border=True):
                    st.subheader("📊 ROIC")
                    st.write(dados['ROIC'] or "Informação não disponível")

            col7, col8 = st.columns(2)

            with col7:
                with st.container(border=True):
                    st.subheader("💰 LPA")
                    st.write(f"{dados['LPA']:.2f}" if dados['LPA'] else "Informação não disponível")

            with col8:
                with st.container(border=True):
                    st.subheader("📈 VPA")
                    st.write(f"{dados['VPA']:.2f}" if dados.get('VPA') else "Informação não disponível")

            # Cálculo do preço teto pelo método Graham
            Graham_const = 22.5
            lpa = dados.get('LPA')
            vpa = dados.get('VPA')
            preco_teto = None
            if lpa and vpa and lpa > 0 and vpa > 0:
                preco_teto = (Graham_const * lpa * vpa) ** 0.5

            preco_atual = dados.get('PrecoAtual')

            # cálculo de diferença percentual e absoluta (Atual x Teto)
            diferenca_pct = None
            diferenca_abs = None
            if preco_atual and preco_teto and preco_teto > 0:
                diferenca_pct = ((preco_atual - preco_teto) / preco_teto) * 100
                diferenca_abs = preco_atual - preco_teto

            # Exibir lado a lado: Preço Teto, Preço Atual e Diferença
            col9, col10, col11 = st.columns(3)

            with col9:
                with st.container(border=True):
                    st.subheader("💹 Preço Atual")
                    if preco_atual:
                        st.write(f"R$ {preco_atual:.2f}")
                    else:
                        st.write("Informação não disponível")

            with col10:
                with st.container(border=True):
                    st.subheader("🏁 Preço Teto (Graham)")
                    if preco_teto:
                        st.write(f"R$ {preco_teto:.2f}")
                    else:
                        st.write("Informação não disponível")

            with col11:
                with st.container(border=True):
                    if diferenca_pct is not None and diferenca_abs is not None:
                        st.metric(
                            "Diferença (Preço Atual vs Preço Teto)",
                            f"{diferenca_pct:+.2f}%",
                            delta=f"R$ {diferenca_abs:+.2f}"
                        )
                    elif diferenca_pct is not None:
                        st.metric(
                            "Diferença %",
                            f"{diferenca_pct:+.2f}%",
                            delta="R$ 0.00"
                        )
                    else:
                        st.write("Diferença não disponível")

# ================================================================
# GRÁFICO DE HISTÓRICO DE PREÇO (12 MESES)
# ================================================================

        st.divider()
        st.subheader("📈 Histórico de Preço (12 meses)")

        try:
            historico = obter_historico_preco(ticker)

            if historico is not None and not historico.empty:
                # Criar figura com Plotly Graph Objects
                fig = go.Figure()

                # Adicionar linha de preço de fechamento
                fig.add_trace(go.Scatter(
                    x=historico.index,
                    y=historico['Close'],
                    mode='lines',
                    name='Preço de Fechamento',
                    line=dict(color='#00D9FF', width=2.5),
                    fill='tozeroy',
                    fillcolor='rgba(0, 217, 255, 0.15)'
                ))

                # Calcular limites do eixo Y com margem dinâmica
                preco_min = historico['Close'].min()
                preco_max = historico['Close'].max()
                amplitude = preco_max - preco_min

                # Margem de 15% acima e abaixo
                margem = amplitude * 0.15
                y_min = preco_min - margem
                y_max = preco_max + margem

                # Adicionar linha de preço teto (Graham) se disponível
                if preco_teto:
                    fig.add_hline(
                        y=preco_teto,
                        line_dash="dash",
                        line_color="#00FF41",
                        annotation_text=f"Preço Teto (Graham): R$ {preco_teto:.2f}",
                        annotation_position="right",
                        annotation_font=dict(size=11, color="#00FF41")
                    )
                    # Ajustar limite superior se preço teto for maior
                    if preco_teto > y_max:
                        y_max = preco_teto + (amplitude * 0.1)

                # Adicionar linha de preço atual
                if preco_atual:
                    fig.add_hline(
                        y=preco_atual,
                        line_dash="dash",
                        line_color="#FF6B6B",
                        annotation_text=f"Preço Atual: R$ {preco_atual:.2f}",
                        annotation_position="right",
                        annotation_font=dict(size=11, color="#FF6B6B")
                    )

                # Configurar layout com limites ajustados
                fig.update_layout(
#                   title=f'Histórico de Preço - {ticker} (Últimos 12 meses)',
                    xaxis_title='Data',
                    yaxis_title='Preço (R$)',
                    hovermode='x unified',
                    template='plotly_dark',
                    height=700,
                    margin=dict(b=150),
                    plot_bgcolor='rgba(17, 17, 17, 0.5)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    xaxis=dict(
                        rangeslider=dict(visible=False),
                        type='date',
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

                # Adicionar anotação explicativa abaixo do gráfico
                fig.add_annotation(
                    text="<b>Linhas de Referência:</b> " +
                         "<span style='color:#00FF41'>━━ Verde (tracejada):</span> Preço Teto (Método Graham) | " +
                         "<span style='color:#FF6B6B'>━━ Vermelho (tracejada):</span> Preço Atual do Mercado",
                    xref="paper", yref="paper",
                    x=0.5, y=-0.20,
                    showarrow=False,
                    bgcolor="rgba(30, 30, 30, 0.95)",
                    bordercolor="rgba(255, 255, 255, 0.2)",
                    borderwidth=1,
                    font=dict(size=10, color='#FFFFFF'),
                    align="center",
                    xanchor="center"
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Não foi possível obter histórico de preços para este ticker")

        except Exception as e:
            st.error(f"❌ Erro ao carregar gráfico: {e}")
        except Exception as e:
            st.error(f"❌ Erro ao carregar gráfico: {e}")
        # Tabela resumida
        st.subheader("📋 Resumo Completo")

        df_resumo = {
            "Métrica": ["Ticker", "Segmento", "Tag Along", "Free Float", "PAYOUT", "ROE", "Dívida Líquida / Ebitda", "ROIC", "LPA", "VPA", "Preço Atual", "Preço Teto (Graham)", "Diferença % (Atual vs Teto)", "Diferença R$ (Atual - Teto)"],
            "Valor": [
                dados['Ticker'] or "N/A",
                dados['Segmento'] or "N/A",
                dados['Tag Along'] or "N/A",
                dados['Free Float'] or "N/A",
                dados['PAYOUT'] or "N/A",
                dados['ROE'] or "N/A",
                dados['Dívida Líquida / Ebitda'] or "N/A",
                dados['ROIC'] or "N/A",
                f"{dados['LPA']:.2f}" if dados['LPA'] else "N/A",
                f"{dados['VPA']:.2f}" if dados.get('VPA') else "N/A",
                f"R$ {preco_atual:.2f}" if preco_atual else "N/A",
                f"R$ {preco_teto:.2f}" if preco_teto else "N/A",
                f"{diferenca_pct:+.2f}%" if diferenca_pct is not None else "N/A",
                f"R$ {diferenca_abs:+.2f}" if diferenca_abs is not None else "N/A"
            ]
        }

        st.dataframe(df_resumo, use_container_width=True, hide_index=True)