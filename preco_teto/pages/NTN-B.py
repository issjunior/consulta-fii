import streamlit as st
from scraping_ntnb import *
from scraping_ipca import *

st.markdown("<h3 style='color:red;'>IPCA</h3>", unsafe_allow_html=True)
st.markdown(f"<p class='reduced-space'>Busca automática no site do <a href='{url_ibge}' target='_blank'>IBGE</a></p>", unsafe_allow_html=True)
st.markdown(f"**IPCA**: {ipca_elements[1].text.strip()}")

# Exibe os títulos encontrados e suas porcentagens
media_ntnb_local, titulos_info = exibir_resultados()
if titulos_info:
    st.markdown("<h3 style='color:red;'>Títulos IPCA+ encontrados", unsafe_allow_html=True)
    st.markdown(f"<p class='reduced-space'>Busca automática no site do <a href='{url_investidor10}' target='_blank'>Investidor10</a></p>", unsafe_allow_html=True)
    for titulo, porcentagem in titulos_info:
        st.markdown(f"<p class='reduced-space'>{titulo} + {porcentagem}%</p>", unsafe_allow_html=True)
else:
    st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

# Exibição do resultado da função exibir_resultados() na barra lateral (media NTNB)
st.markdown(f"**Média NTN-B**: {media_ntnb_local:.2f}%")
