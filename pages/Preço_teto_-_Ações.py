import streamlit as st
from modulos.scraping_acoes import obter_dados_acao

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Header principal
st.title("📊 Cálculo de Preço Teto - Ações")

# Seção explicativa
with st.expander("ℹ️ Entenda o Método Graham"):
    col_text, col_img = st.columns([1, 1])

    with col_text:
        st.subheader("Método Graham")
        st.write(
            "Determina um valor justo para uma ação com base no lucro por ação (LPA) "
            "e na taxa de crescimento esperada da empresa."
        )

    with col_img:
        st.image("img/formula_graham.png")

st.divider()

# Seção de busca
st.header("🔍 Buscar Fundamentalista")

col_input, col_button = st.columns([4, 1])

with col_input:
    ticker = st.text_input(
        "Ticker da Ação",
        placeholder="Ex: PETR4, VALE3",
        label_visibility="collapsed"
    ).upper()

with col_button:
    buscar = st.button("Buscar", use_container_width=True)

# Processamento da busca
if buscar:
    if not ticker:
        st.warning("⚠️ Digite um ticker válido")
    else:
        with st.spinner(f"Buscando dados de {ticker}..."):
            dados = obter_dados_acao(ticker)

        if "erro" in dados:
            st.error(dados["erro"])
        else:
            st.success(f"✅ Dados carregados com sucesso")
            st.caption(
                f"Fonte: [Investidor10](https://investidor10.com.br/acoes/{ticker})"
            )
            st.divider()

            # Exibição dos dados
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Segmento")
                st.write(dados['Segmento'] or "N/A")

            with col2:
                st.subheader("🏷️ Tag Along")
                st.write(dados['Tag Along'] or "N/A")

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("🔄 Free Float")
                st.write(dados['Free Float'] or "N/A")

            with col4:
                st.subheader("📊 PAYOUT")
                st.write(dados['PAYOUT'] or "N/A")

            st.metric(
                "💰 LPA (Lucro por Ação)",
                f"R$ {dados['LPA']:.2f}" if dados['LPA'] else "N/A"
            )