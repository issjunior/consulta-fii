import streamlit as st
import pandas as pd
from pages.Índices import *

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",  # ou "centered"
)


# Exibe os títulos encontrados no investidor10 e suas porcentagens
media_ntnb_local, titulos_info = exibir_resultados()

if titulos_info:
    st.title("Títulos IPCA+")
    st.caption("Título de renda fixa emitido pelo governo brasileiro, com rendimento atrelado à inflação medida pelo IPCA (Índice de Preços ao Consumidor Amplo), que é o principal indicador da inflação no Brasil. Além disso, é muito utilizado para comparar a atratividade de FIIs")

    # Processa os títulos encontrados
    df_titulos = processar_titulos(titulos_info, ultimo_ipca_formatado)

    # Exibe o DataFrame com os títulos, agora incluindo a coluna 'Soma'
    st.dataframe(df_titulos, hide_index=True, use_container_width=True)
    st.caption(f"Fonte: <a href='{url_investidor10}' target='_blank'>Investidor10</a>.</p>", unsafe_allow_html=True)
else:
    st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

st.divider()
