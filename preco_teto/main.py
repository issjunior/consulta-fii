from config import *
from scraping_ntnb import *
from dividendos import *
from calculos import *
import yfinance as yf
import streamlit as st
import pandas as pd

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

    # Exibe os títulos encontrados e suas porcentagens
    media_ntnb_local, titulos_info = exibir_resultados()
    if titulos_info:
        st.markdown("### Títulos IPCA+ encontrados")
        st.markdown(f"Busca automática no site do [Investidor10]({url})")
        for titulo, porcentagem in titulos_info:
            st.write(f"{titulo} - IPCA + {porcentagem}%")
    else:
        st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

    # Exibição do resultado da função exibir_resultados() na barra lateral (media NTNB)
    st.markdown(f"**Média NTN-B:** {media_ntnb_local:.2f}%")

def main():
    st.header("Cálculo de preço teto para FIIs de tijolos")
    ticker = st.text_input("Digite o ticker do FII:", "").upper() + ".SA"
    spread = st.number_input("Qual o spread (risco) do FII:", value=2.5, step=0.5, format="%.2f")
    vacancia = st.number_input("Qual a vacância (%):", value=0.0, step=0.01, format="%.2f")
    tx_crescimento_dy = st.number_input("Taxa de crescimento esperado para os proximos 12 meses (%):", value=0.0, step=0.01, format="%.2f")

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
                    return ['background-color: #f0f0f0' if row.name % 2 == 0 else 'background-color: white'] * len(row)

                st.subheader(f"Resultados para {ticker.replace('.SA', '')}")
                st.dataframe(df_resultados.style.apply(colorir_linhas, axis=1), use_container_width=True)
#               st.markdown(f"Total dividendos: {total_dividendos}, media NTNB: {media_ntnb_local}, spread: {spread} e tx de cescimento: {tx_crescimento_dy}")

            except KeyError:
                st.error(f"Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.")
        else:
            st.warning("Por favor, insira um ticker válido.")
if __name__ == "__main__":
    main()
