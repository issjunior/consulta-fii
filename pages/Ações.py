import streamlit as st
import yfinance as yf

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
)

st.title("Cálculo de Ações")
st.caption("Método de análise de desempenho de ações")

with st.expander("Entenda o cálculo"):
    st.title("Método ")
    st.write("Fórmula utilizada para estimar o preço justo ou preço-teto de um ativo baseado em seus dividendos futuros. No contexto de fundos imobiliários, esse modelo assume que os dividendos crescem a uma taxa constante ao longo do tempo ou não subir.")

    moldura = st.container(border=True)
    moldura.image("img/modelo_gordon.png")

    st.markdown(""" 
    ##### Explicando cada termo:
    O método Graham calcula o preço-teto (ou valor justo) de uma ação usando a fórmula: Valor Justo = √ (22,5 x LPA x VPA), onde LPA é o Lucro por Ação e VPA é o Valor Patrimonial por Ação
    """)

    st.write("Usamos os títulos NTN-B (Tesouro IPCA+) para precificar fundos imobiliários, porque eles oferecem uma taxa de retorno praticamente livre de risco e protegida contra a inflação. Essa taxa serve como base de comparação para o retorno esperado dos FIIs, já que, por terem maior risco, os fundos imobiliários precisam oferecer uma rentabilidade superior a média NTN-B. Além disso, essa comparação ajuda os investidores a avaliar se os FIIs estão caros ou baratos.")

st.divider()