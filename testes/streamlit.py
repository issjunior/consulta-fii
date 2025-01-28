import streamlit as st

url_ibge = "https://www.ibge.gov.br/"  # exemplo de URL
ipca_valor = "3.5%"  # exemplo de valor do IPCA

# Criação de uma moldura com CSS e HTML no Streamlit
st.markdown(
    """
    <div style='border: 2px solid #4CAF50; padding: 10px; border-radius: 8px;'>
        <h3 style='margin-top: 0;'>IPCA</h3>
        <p class='reduced-space'>Busca automática no site do <a href='{url_ibge}' target='_blank'>IBGE</a></p>
        <p><strong>IPCA</strong>: {ipca_valor}</p>
    </div>
    """.format(url_ibge=url_ibge, ipca_valor=ipca_valor),
    unsafe_allow_html=True
)
