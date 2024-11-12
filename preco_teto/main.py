from config import *
from scraping_ntnb import *
from scraping_ipca import *
from dividendos import *
from calculos import *
import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Definindo o layout para wide mode
st.set_page_config(layout="wide")

with st.sidebar:
    # Explicando os termos do modelo de gordon
    st.image("preco_teto/img/modelo_gordon.png", use_container_width=True)
    
    st.markdown(""" 
    Onde:
    - **$D_{1}$**: Consideramos os 12 últimos.
    - **r**: Média NTN-B + spread.
    - **g**: Taxa de crescimento dos dividendos.
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

    st.markdown("<h3 style='color:red;'>IPCA</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='reduced-space'>Busca automática no site do <a href='{url_ibge}' target='_blank'>IBGE</a></p>", unsafe_allow_html=True)
    st.markdown(f"**IPCA**: {ipca_elements[1].text.strip()}")

    # Exibe os títulos encontrados e suas porcentagens
    media_ntnb_local, titulos_info = exibir_resultados()
    if titulos_info:
        st.markdown("<h3 style='color:red;'>Títulos IPCA+ encontrados", unsafe_allow_html=True)
        st.markdown(f"<p class='reduced-space'>Busca automática no site do <a href='{url_investidor10}' target='_blank'>Investidor10</a></p>", unsafe_allow_html=True)
        for titulo, porcentagem in titulos_info:
            st.markdown(f"<p class='reduced-space'>{titulo} + {porcentagem}%</p>", unsafe_allow_html=True)
    else:
        st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

    # Exibição do resultado da função exibir_resultados() na barra lateral (media NTNB)
    st.markdown(f"**Média NTN-B**: {media_ntnb_local:.2f}%")

def main():
    st.header("Cálculo de preço teto para FIIs")
    ticker = st.text_input("Digite o ticker do FII:", "").upper() + ".SA"
    spread = st.number_input("Qual o spread (risco) do FII:", value=2.5, step=0.5, format="%.2f")
    vacancia = st.number_input("Qual a vacância (%):", value=0.0, step=0.01, format="%.2f")
    tx_crescimento_dy = st.number_input("Taxa de crescimento esperado para os próximos 12 meses (%):", value=0.0, step=0.01, format="%.2f")

    if st.button("Consultar"):
        if ticker:
            try:
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

                # Criar colunas lado a lado para os gráficos
                col1, col2 = st.columns(2)

                # Fixar o período em 2 anos
                periodo = '2y'

                # Obter o histórico de preços do ticker com o período fixo
                historico = acao.history(period=periodo)

                # Verificar se o histórico contém dados antes de gerar o gráfico
                if not historico.empty:
                    # Selecionar apenas a coluna de fechamento para o gráfico
                    historico = historico[['Close']].dropna()

                    # Gerar o gráfico de linha com Matplotlib
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(historico.index, historico["Close"], color='tab:blue')
                    ax.set_title(f"Histórico de cota do {ticker.replace('.SA', '')} dos últimos 2 anos")
                    ax.set_xlabel("Data")
                    ax.set_ylabel("Preço de Fechamento")

                    # Exibir o gráfico no col1
                    col1.pyplot(fig)
                else:
                    col1.write("Histórico da cota não disponível para este ticker.")

                # Construção do gráfico de dividendos usando Matplotlib
                dividendos = acao.dividends

                # Verificar se há dividendos disponíveis
                if not dividendos.empty:
                    dividendos.index = dividendos.index.tz_localize(None)  # Remover o fuso horário
                    data_corte = pd.to_datetime('today').normalize()
                    dividendos_2anos = dividendos[dividendos.index >= data_corte - pd.DateOffset(years=2)]

                    # Gerar gráfico de dividendos
                    if not dividendos_2anos.empty:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(dividendos_2anos.index, dividendos_2anos.values, marker='o', color='tab:green')
                        ax.set_title(f"Dividendos pagos por {ticker.replace('.SA', '')} nos últimos 2 anos")
                        ax.set_xlabel("Data")
                        ax.set_ylabel("Valor do Dividendo (R$)")
                        ax.grid(True)

                        # Exibir o gráfico no col2
                        col2.pyplot(fig)
                    else:
                        col2.write("Nenhum dividendo pago nos últimos 2 anos para este ticker.")
                else:
                    col2.write("Nenhum dividendo pago para este ticker.")

            except KeyError:
                st.error(f"Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.")
        else:
            st.warning("Por favor, insira um ticker válido.")

if __name__ == "__main__":
    main()
