from config import *
from scraping_ntnb import *
from dividendos import *
from calculos import *
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
)

# Criando duas colunas
col1, col2, col3 = st.columns(3)

# Adicionando a explicação na primeira coluna (col1)
with col1:
    st.markdown("""
    <div style="text-align: justify;">
        <h2>Modelo de Gordon</h2>
        Fórmula utilizada para estimar o preço justo ou preço-teto de um ativo baseado em seus dividendos futuros. No contexto de fundos imobiliários, esse modelo assume que os dividendos crescem a uma taxa constante ao longo do tempo ou não subir.
    </div>
    """, unsafe_allow_html=True)

# Adicionando a imagem e fórmula na segunda coluna (col2)
with col2:
    st.markdown("""
    <div style="text-align: justify;">
        Usamos os títulos NTN-B (Tesouro IPCA+) para precificar fundos imobiliários, porque eles oferecem uma taxa de retorno praticamente livre de risco e protegida contra a inflação. Essa taxa serve como base de comparação para o retorno esperado dos FIIs, já que, por terem maior risco, os fundos imobiliários precisam oferecer uma rentabilidade superior a média NTN-B. Além disso, essa comparação ajuda os investidores a avaliar se os FIIs estão caros ou baratos.
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.latex(r"PrecoTeto = \frac{D}{R - G}")
    st.markdown(""" 
    ##### Explicando cada termo:
    - **D**: Dividend yield (DY). Consideramos os 12 últimos.
    - **R**: Média NTN-B + SPREAD (risco ou prêmio).
    - **G**: Taxa de crescimento dos dividendos.
    """)

st.divider()

# classe para reduzir o espaçamento no st.markdown
st.markdown(
    """
    <style>
    .reduced-space { margin-bottom: -10px; }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.header("Cálculo de preço teto para FIIs")
    ticker = st.text_input("Digite o ticker do FII:", "").upper() + ".SA"
    spread = st.number_input("Qual o spread (risco) do FII:", value=2.5, step=0.5, format="%.2f")
    vacancia = st.number_input("Qual a vacância (%):", value=0.0, step=0.01, format="%.2f")
    tx_crescimento_dy = st.number_input("Taxa de crescimento esperado para os próximos 12 meses (%):", value=0.0, step=0.01, format="%.2f")

    if st.button("Consultar"):
        if ticker:
            try:
                media_ntnb_local, titulos_info = exibir_resultados()
                media_dividendos = obter_media_dividendos(ticker)
                if media_dividendos is None:
                    st.warning(f"Código {ticker} não encontrado.")
                    return
                total_dividendos = calcular_total_dividendos(media_dividendos)
                acao = yf.Ticker(ticker)
                preco_atual = acao.info.get("currentPrice", None)
                media_dividendos_porcentagem = calcular_media_dividendos_porcentagem(total_dividendos, preco_atual)
                preco_teto = calcular_preco_teto(total_dividendos, media_ntnb_local, spread, tx_crescimento_dy)
                cotas_necessarias = calcular_cotas_necessarias(preco_atual, media_dividendos)
                valor_cotas_magicnumber = calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual)
                valor_cap_rate = calcular_cap_rate_ajustado(media_dividendos, vacancia, preco_atual)

                resultados = {
                    "Indicador": [
                        "Fundo",
                        "Ticker",
                        "Cotação Atual",
                        "Variação da Cota",
                        "Média de Dividendos",
                        "Dividendos Recebidos",
                        "Preço Teto",
                        "Magic Number",
                        "Valor para Magic Number",
                        "Cap Rate Ajustado (considerando vacância)"
                    ],
                    "Valor": [
                        acao.info.get('longName', 'N/A'),
                        ticker.replace(".SA", ""),
                        real(preco_atual),
                        f"R$ {acao.info.get('fiftyTwoWeekLow', 'N/A')} - R$ {acao.info.get('fiftyTwoWeekHigh', 'N/A')}",
                        f"{real(media_dividendos)} (DY anual de {media_dividendos_porcentagem:.2f}%)",
                        real(total_dividendos),
                        f"{real(preco_teto)} (com spread de {spread:.2f}%)",
                        f"{cotas_necessarias} cotas",
                        real(valor_cotas_magicnumber),
                        f"{valor_cap_rate:.2f}%"
                    ]
                }
                df_resultados = pd.DataFrame(resultados)

                def colorir_linhas(row):
                    return ['background-color: #0E1117' if row.name % 2 == 0 else 'background-color: #262730'] * len(row)

                st.subheader(f"Resultados para {ticker.replace('.SA', '')}")
                st.dataframe(df_resultados.style.apply(colorir_linhas, axis=1), use_container_width=True)

                st.divider()

                # Gráficos
                # Criar colunas lado a lado para os gráficos
                col1, col2 = st.columns(2)

                # Fixar o período em 5 anos
                historico = acao.history(period="5y")

                # Verificar se o histórico contém dados antes de gerar o gráfico
                if not historico.empty:
                    historico = historico[['Close']].dropna()
                    data_corte = pd.to_datetime('today').normalize()

                    # Criando o gráfico de preços com Plotly
                    fig = go.Figure()

                    # Adicionando a linha de preços ao gráfico
                    fig.add_trace(go.Scatter(x=historico.index, y=historico['Close'], mode='lines', name='Preço da Cota'))

                    # Ajustes para o gráfico
                    fig.update_layout(
                        title=f"Histórico de preço.",
                        xaxis_title="Escolha o período",
                        yaxis_title="Preço (R$)",
                        xaxis_rangeslider_visible=True,  # Habilita o controle de zoom (range slider)
                        xaxis_range=[data_corte - pd.DateOffset(years=1), data_corte]  # Limita a visualização para 1 ano
                    )

                    # Exibe o gráfico interativo no Streamlit
                    col1.plotly_chart(fig, use_container_width=True)
                else:
                    col1.write("Histórico da cota não disponível para este ticker.")

                # Construção do gráfico de dividendos
                dividendos = acao.dividends

                # Verificar se há dividendos disponíveis
                if not dividendos.empty:
                    dividendos.index = dividendos.index.tz_localize(None)
                    data_corte = pd.to_datetime('today').normalize()
                    dividendos_5anos = dividendos[dividendos.index >= data_corte - pd.DateOffset(years=5)]

                    # Criando o gráfico de dividendos com Plotly
                    fig_dividendos = go.Figure()

                    # Adicionando a linha de dividendos ao gráfico
                    fig_dividendos.add_trace(go.Scatter(x=dividendos_5anos.index, y=dividendos_5anos, mode='markers+lines', name='Dividendos'))

                    # Ajustes para o gráfico de dividendos
                    fig_dividendos.update_layout(
                        title=f"Histórico de dividendos.",
                        xaxis_title="Escolha o período",
                        yaxis_title="Dividendos (R$)",
                        xaxis_rangeslider_visible=True,  # Habilita o controle de zoom (range slider)
                        xaxis_range=[data_corte - pd.DateOffset(years=1), data_corte]  # Limita a visualização para 1 ano
                    )

                    # Exibe o gráfico interativo no Streamlit
                    col2.plotly_chart(fig_dividendos, use_container_width=True)
                else:
                    col2.write("Nenhum dividendo pago para este ticker.")

            except KeyError:
                st.error(f"Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.")
        else:
            st.warning("Por favor, insira um ticker válido.")

if __name__ == "__main__":
    main()
