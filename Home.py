import streamlit as st

# ================================================================
# CONFIGURAÇÃO DO LAYOUT
# ================================================================
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",                      # ✅ wide — padrão de todas as páginas
    initial_sidebar_state="auto",
    menu_items={
        "Get Help":    None,
        "Report a bug": None,
        "About": (
            "**Sistema de Investimento** — Desenvolvido para análise de FIIs, "
            "Ações, Índices Econômicos e Criptomoedas.\n\n"
            "Versão 1.0"
        )
    }
)

# ================================================================
# HEADER
# ================================================================
st.title("📊 Sistema de Investimento")
st.caption("Análise de FIIs, Ações, Índices Econômicos e Criptomoedas.")

st.divider()

# ================================================================
# LOGO CENTRALIZADA
# ================================================================
col_esq, col_centro, col_dir = st.columns([1, 2, 1])

with col_centro:
    st.image(
        "img/logo_real_state_JR.png",
        caption="Sistema de Investimento",
        use_container_width=True
    )

st.divider()

# ================================================================
# CARDS DE NAVEGAÇÃO
# ================================================================
st.subheader("🗂️ Navegue pelo sistema")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown("### 🏢 FIIs de Tijolo")
        st.caption("Cálculo de Preço Teto pelo Modelo de Gordon para fundos imobiliários.")

with col2:
    with st.container(border=True):
        st.markdown("### 📈 Índices")
        st.caption("Acompanhe IPCA, SELIC, CDI e IFIX em tempo real.")

with col3:
    with st.container(border=True):
        st.markdown("### ₿ Mercado")
        st.caption("Cotações de Bitcoin, Dólar e indicadores de mercado.")

with col4:
    with st.container(border=True):
        st.markdown("### 💹 Yield On Cost")
        st.caption("Calcule o retorno real dos seus investimentos ao longo do tempo.")