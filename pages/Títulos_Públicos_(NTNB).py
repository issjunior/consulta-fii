import streamlit as st
import pandas as pd
from modulos.ipca import obter_ipca, processar_titulos
from modulos.scraping_ntnb import url_investidor10
from pages.Índices import exibir_resultados


# Configuração do layout (sempre primeiro)
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Obtém os títulos encontrados no Investidor10
media_ntnb_local, titulos_info = exibir_resultados()

# Obtém os dados do IPCA
ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte = obter_ipca()

# Define o último IPCA formatado de forma segura
if ipca_filtrado_formatado is not None and not ipca_filtrado_formatado.empty:
    ultimo_ipca_bruto = ipca_5anos.iloc[-1].values[0]
    ultimo_ipca_formatado = f"{ultimo_ipca_bruto:.2f} %"
else:
    ultimo_ipca_formatado = "0.00 %"

# Verifica se há títulos encontrados
if titulos_info:
    st.title("Títulos IPCA+")
    st.caption(
        "Título de renda fixa emitido pelo governo brasileiro, com rendimento atrelado "
        "à inflação medida pelo IPCA (Índice de Preços ao Consumidor Amplo), que é o principal "
        "indicador da inflação no Brasil. Além disso, é muito utilizado para comparar a atratividade de FIIs."
    )

    # Processa os títulos encontrados
    df_titulos = processar_titulos(titulos_info, ultimo_ipca_formatado)

    # Função de estilo para destacar o maior valor da coluna 'Soma'
    def highlight_max(data, color="gray"):
        attr = f"background-color: {color};"
        is_max = data == data.max()
        return [attr if v else "" for v in is_max]

    # Aplica o estilo
    styled_df = df_titulos.style.apply(highlight_max, subset=["Soma"])

    # Exibe o DataFrame com estilo
    st.table(styled_df)
    st.caption(
        f"Fonte: <a href='{url_investidor10}' target='_blank'>Investidor10</a>.",
        unsafe_allow_html=True
    )
else:
    st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

st.divider()
