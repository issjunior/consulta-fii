import streamlit as st
import pandas as pd
from modulos.ipca import obter_ipca, processar_titulos
from modulos.scraping_ntnb import url_investidor10, exibir_resultados

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

manual_ntnb_input = st.number_input(
    "NTN-B manual (%):",
    min_value=0.0,
    value=0.0,
    step=0.01,
    format="%.2f",
    help=(
        "Opcional: insira a taxa NTN-B manualmente. "
        "O valor será usado nos cálculos quando informado."
    ),
    key="manual_ntnb_input"
)
manual_ntnb = manual_ntnb_input if manual_ntnb_input > 0 else None

# ================================================================
# COLETA DE DADOS COM LOADING
# ================================================================
loading_container = st.empty()
loading_container.info("📡 Buscando títulos IPCA+ no Investidor10...")

try:
    media_ntnb_local, titulos_info = exibir_resultados(manual_ntnb)
except Exception as e:
    loading_container.empty()
    st.error(f"❌ Erro ao buscar títulos NTN-B: {e}")
    st.stop()

loading_container.empty()

scraping_failed = not titulos_info
manual_override = manual_ntnb is not None

if scraping_failed and not manual_override:
    st.info(
        "Não foi possível obter automaticamente a taxa NTN-B via scraping do Investidor10. "
        "Por favor, informe abaixo o valor manualmente com duas casas decimais. "
        "Esse valor será usado nos cálculos e na tabela."
    )
elif manual_override:
    st.info(
        "A taxa NTN-B exibida está sendo usada a partir da entrada manual do usuário."
    )
else:
    st.info(
        "A taxa NTN-B exibida está sendo obtida automaticamente via scraping do Investidor10."
    )

if manual_override:
    media_ntnb_local = manual_ntnb

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
if titulos_info or manual_ntnb is not None:
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📈 Média NTN-B")
            if media_ntnb_local is not None:
                metric_label = (
                    "Média dos títulos encontrados"
                    if manual_ntnb is None
                    else "Taxa NTN-B manual utilizada"
                )
                st.metric(
                    label=metric_label,
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
        df_titulos = processar_titulos(titulos_info, ultimo_ipca_formatado, manual_ntnb=manual_ntnb)

        # Destaca o maior valor da coluna 'Soma'
        def highlight_max(data, color="#1f4e79"):
            attr  = f"background-color: {color}; color: white; font-weight: bold;"
            is_max = data == data.max()
            return [attr if v else "" for v in is_max]

        styled_df = df_titulos.style.apply(highlight_max, subset=["Soma"])

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Erro ao processar os títulos: {e}")

    if manual_override:
        st.caption("Fonte: Valor manual informado pelo usuário.")
    else:
        st.caption(
            f"Fonte: <a href='{url_investidor10}' target='_blank'>Investidor10</a> (scraping).",
            unsafe_allow_html=True
        )

elif not scraping_failed:
    st.warning("⚠️ Nenhum título IPCA+ encontrado ou ocorreu um erro ao buscar os dados.")