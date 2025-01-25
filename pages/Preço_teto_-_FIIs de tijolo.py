from config import *
from modulos.scraping_ntnb import *
from modulos.scraping_valorpatrimonial import *
from modulos.dividendos import *
from modulos.calculos import *
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

with st.expander("Entenda o cálculo"):
    st.title("Modelo de Gordon")
    st.write("Fórmula utilizada para estimar o preço justo ou preço-teto de um ativo baseado em seus dividendos futuros. No contexto de fundos imobiliários, esse modelo assume que os dividendos crescem a uma taxa constante ao longo do tempo ou não subir.")

    moldura = st.container(border=True)
    moldura.image("img/modelo_gordon.png")

    st.markdown(""" 
    ##### Explicando cada termo:
    - **D**: Dividend yield (DY). Consideramos os 12 últimos.
    - **R**: Média NTN-B + SPREAD (risco ou prêmio).
    - **G**: Taxa de crescimento dos dividendos.
    """)

    st.write("Usamos os títulos NTN-B (Tesouro IPCA+) para precificar fundos imobiliários, porque eles oferecem uma taxa de retorno praticamente livre de risco e protegida contra a inflação. Essa taxa serve como base de comparação para o retorno esperado dos FIIs, já que, por terem maior risco, os fundos imobiliários precisam oferecer uma rentabilidade superior a média NTN-B. Além disso, essa comparação ajuda os investidores a avaliar se os FIIs estão caros ou baratos.")

st.divider()

def main():
    st.header("Cálculo de preço teto para FIIs de Tijolo")
    ticker = st.text_input("Ticker do FII:", "").upper() + ".SA"
    spread = st.number_input("Spread (prêmio) do FII:", value=2.5, min_value=0.0, step=0.1, format="%.2f")
    vacancia = st.number_input("Vacância (%):", value=0.0, min_value=0.0, step=0.1, format="%.2f")
    tx_crescimento_dy = st.number_input("Taxa de crescimento esperado para os próximos 12 meses (%):",min_value=0.0, value=0.0, step=0.1, format="%.2f")

    if st.button("Consultar"):
        if ticker:
            try:
                media_ntnb_local, titulos_info = exibir_resultados() # média dos titulos NTN-B do modulo "scraping.ntnb.py"
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
                valor_obter_pvp = obter_pvp(ticker)

                resultados = {
                    "Indicador": [
                        "Gestora",
                        "Ticker",
                        "Cotação Atual",
                        "Variação da Cota",
                        "Média de Dividendos",
                        "Dividendos Recebidos (últimos 12 meses)",
                        "Preço Teto",
                        "Magic Number",
                        "Valor para Magic Number",
                        "Cap Rate Ajustado (considerando vacância)",
                        "P/VP"
                    ],
                    "Valor": [
                        acao.info.get('longName', 'N/A'),
                        ticker.replace(".SA", ""),
                        real(preco_atual),
                        f"{real(acao.info.get('fiftyTwoWeekLow', 'N/A'))} - {real(acao.info.get('fiftyTwoWeekHigh', 'N/A'))}",
                        f"{real(media_dividendos)} (DY anual de {porcentagem(media_dividendos_porcentagem)})",
                        real(total_dividendos),
                        f"{real(preco_teto)} (com spread de {porcentagem(spread)})",
                        f"{cotas_necessarias} cotas",
                        real(valor_cotas_magicnumber),
                        f"{porcentagem(valor_cap_rate)}",
                        f"{porcentagem(valor_obter_pvp)}"
                    ]
                }
                df_resultados = pd.DataFrame(resultados)

                def colorir_linhas(row):
                    return ['background-color: #0E1117' if row.name % 2 == 0 else 'background-color: #262730'] * len(row)

                st.subheader(f"Resultados para {ticker.replace('.SA', '')}")

                # Informações de destaque FII
                col1, col2 = st.columns(2)               
                delta_preco = preco_teto - preco_atual

                with col1:
                    st.metric(label="Preço Atual", value=real(preco_atual), delta=real(delta_preco), delta_color="normal")

                with col2:
                    st.metric(label="Preço Teto", value=real(preco_teto))

                st.dataframe(df_resultados.style.apply(colorir_linhas, axis=1), hide_index=True, use_container_width=True)

                st.caption("Últimos 12 meses")

                st.divider()

                # Gráficos do histórico de cotas
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
                    fig.add_trace(go.Scatter(
                        x=historico.index,
                        y=historico['Close'],
                        mode='lines',
                        name='Preço da Cota',
                        hovertemplate="<b>Data:</b> %{x}<br><b>Valor Cota:</b> %{y:.2f}<extra></extra>"
                        )
                    )

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
                    dividendos_5anos = dividendos[dividendos.index >= data_corte - pd.DateOffset(years=10)]  # Periodo de 10 anos de dividendos

                    # Criando o gráfico de dividendos com Plotly
                    fig_dividendos = go.Figure()

                    # Adicionando a linha de dividendos ao gráfico
                    fig_dividendos.add_trace(go.Scatter(
                        x=dividendos_5anos.index,
                        y=dividendos_5anos,
                        mode='markers+lines',
                        name='Dividendos',
                        hovertemplate="<b>Data:</b> %{x}<br><b>Dividendo:</b> %{y:.2f}<extra></extra>"
                        )
                    )

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
