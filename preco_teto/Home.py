import streamlit as st

# Configuração do layout
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="centered",  # ou "wide"
)

# Caminho para o arquivo da imagem
imagem_path = "img/logo_real_state_JR.png"

# Exibir a imagem com o novo parâmetro
st.image(imagem_path, caption="Sistema de Investimento", use_container_width=True)
