import streamlit as st
import pandas as pd
from modulos.ipca import obter_ipca, processar_titulos
from modulos.scraping_ntnb import url_investidor10
from pages.Índices import exibir_resultados

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("📊 Títulos IPCA+")
st.caption(
    "Título de renda fixa emitido pelo governo brasileiro, com rendimento atrelado "
    "à inflação medida pelo IPCA (Índice de Preços ao Consumidor Amplo), que é o principal "
    "indicador da inflação no Brasil. Além disso, é muito utilizado para comparar a "
    "atratividade de FIIs."
)

st.divider()

# ================================================================
# COLETA DE DADOS COM LOADING
# ================================================================
loading_container = st.empty()
loading_container.info("📡 Buscando títulos IPCA+ no Investidor10...")

try:
    media_ntnb_local, titulos_info = exibir_resultados()
except Exception as e:
    loading_container.empty()
    st.error(f"❌ Erro ao buscar títulos NTN-B: {e}")
    st.stop()

try:
    ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte = obter_ipca()
except Exception as e:
    loading_container.empty()
    st.error(f"❌ Erro ao buscar dados do IPCA: {e}")
    st.stop()

loading_container.empty()

# ================================================================
# ÚLTIMO IPCA — com fallback seguro
# ================================================================
try:
    if ipca_filtrado_formatado is not None and not ipca_filtrado_formatado.empty:
        ultimo_ipca_bruto     = ipca_5anos.iloc[-1].values[0]
        ultimo_ipca_formatado = f"{ultimo_ipca_bruto:.2f} %"
    else:
        ultimo_ipca_formatado = "0.00 %"
except Exception:
    ultimo_ipca_formatado = "0.00 %"

# ================================================================
# CARDS DE DESTAQUE
# ================================================================
if titulos_info:
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📈 Média NTN-B")
            if media_ntnb_local is not None:
                st.metric(
                    label="Média dos títulos encontrados",
                    value=f"{media_ntnb_local:.2f} %",
                )
            else:
                st.write("Informação não disponível")

    with col2:
        with st.container(border=True):
            st.subheader("💹 Último IPCA")
            st.metric(
                label="Índice mais recente disponível",
                value=ultimo_ipca_formatado,
            )

    st.divider()

    # ================================================================
    # TABELA DE TÍTULOS
    # ================================================================
    st.subheader("📋 Títulos Encontrados")

    try:
        df_titulos = processar_titulos(titulos_info, ultimo_ipca_formatado)

        # Destaca o maior valor da coluna 'Soma'
        def highlight_max(data, color="#1f4e79"):
            attr  = f"background-color: {color}; color: white; font-weight: bold;"
            is_max = data == data.max()
            return [attr if v else "" for v in is_max]

        styled_df = df_titulos.style.apply(highlight_max, subset=["Soma"])

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Erro ao processar os títulos: {e}")

    st.caption(
        f"Fonte: <a href='{url_investidor10}' target='_blank'>Investidor10</a>.",
        unsafe_allow_html=True
    )

else:
    st.warning("⚠️ Nenhum título IPCA+ encontrado ou ocorreu um erro ao buscar os dados.")