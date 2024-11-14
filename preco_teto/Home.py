import streamlit as st

# Definindo o layout para wide mode
st.set_page_config(layout="wide")


# Caminho para o arquivo da imagem
imagem_path = "preco_teto/img/logo_real_state_JR.png"

# Exibir a imagem com o novo parâmetro
st.image(imagem_path, caption="Sistema de Investimento", use_container_width=True)
