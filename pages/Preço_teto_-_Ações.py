import streamlit as st
from modulos.scraping_acoes import *

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

        if dados is None:
            st.error(f"❌ Não foi possível obter dados para {ticker}")
        else:
            st.success(f"✅ Dados carregados com sucesso")
            st.caption(
                f"Fonte: [Investidor10](https://investidor10.com.br/acoes/{ticker})"
            )
            st.divider()

            # Segmento em destaque
            st.title(f"{dados['Ticker']}")

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                with st.container(border=True):
                    st.subheader("📂 Segmento")
                    st.write(dados['Segmento'] or "Informação não disponível")

            with col2:
                with st.container(border=True):
                    st.subheader("🏷️ Tag Along")
                    st.write(dados['Tag Along'] or "Informação não disponível")

            with col3:
                with st.container(border=True):
                    st.subheader("🔄 Free Float")
                    st.write(dados['Free Float'] or "Informação não disponível")

            col4, col5, col6 = st.columns(3)

            with col4:
                with st.container(border=True):
                    st.subheader("📊 PAYOUT")
                    st.write(dados['PAYOUT'] or "Informação não disponível")

            with col5:
                with st.container(border=True):
                    st.subheader("💰 LPA")
                    st.write(f"{dados['LPA']:.2f}" if dados['LPA'] else "Informação não disponível")

            with col6:
                with st.container(border=True):
                    st.subheader("📈 VPA")
                    st.write(f"{dados['VPA']:.2f}" if dados.get('VPA') else "Informação não disponível")

            # Cálculo do preço teto pelo método Graham
            Graham_const = 22.5
            lpa = dados.get('LPA')
            vpa = dados.get('VPA')
            preco_teto = None
            if lpa and vpa and lpa > 0 and vpa > 0:
                preco_teto = (Graham_const * lpa * vpa) ** 0.5

            preco_atual = dados.get('PrecoAtual')

            # Exibir lado a lado: Preço Teto e Preço Atual
            col7, col8 = st.columns(2)

            with col7:
                with st.container(border=True):
                    st.subheader("💹 Preço Atual")
                    if preco_atual:
                        st.write(f"R$ {preco_atual:.2f}")
                    else:
                        st.write("Informação não disponível")

            with col8:
                with st.container(border=True):
                    st.subheader("🏁 Preço Teto (Graham)")
                    if preco_teto:
                        st.write(f"R$ {preco_teto:.2f}")
                    else:
                        st.write("Informação não disponível")

            st.divider()

            # Tabela resumida
            st.subheader("📋 Resumo Completo")

            df_resumo = {
                "Métrica": ["Ticker", "Segmento", "Tag Along", "Free Float", "PAYOUT", "LPA", "VPA", "Preço Atual", "Preço Teto (Graham)"],
                "Valor": [
                    dados['Ticker'] or "N/A",
                    dados['Segmento'] or "N/A",
                    dados['Tag Along'] or "N/A",
                    dados['Free Float'] or "N/A",
                    dados['PAYOUT'] or "N/A",
                    f"{dados['LPA']:.2f}" if dados['LPA'] else "N/A",
                    f"{dados['VPA']:.2f}" if dados.get('VPA') else "N/A",
                    f"R$ {preco_atual:.2f}" if preco_atual else "N/A",
                    f"R$ {preco_teto:.2f}" if preco_teto else "N/A"
                ]
            }

            st.dataframe(df_resumo, use_container_width=True, hide_index=True)