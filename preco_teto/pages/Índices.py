from bcb import sgs
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scraping_ntnb import *

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Sis. de Investimento",
    page_icon="📊",
    layout="wide",
)

# Obtém os dados do IPCA (5 anos)
ipca_5anos = sgs.get(13522)

# Define a data de corte como a última data disponível
data_corte = pd.to_datetime("today").normalize()

# Define o período padrão para 5 anos e os últimos 12 meses
data_inicio_5anos = data_corte - pd.DateOffset(years=5)  # 5 anos de histórico
data_inicio_12meses = data_corte - pd.DateOffset(years=1)  # Últimos 12 meses

# Filtra os dados para os últimos 5 anos
ipca_filtrado = ipca_5anos.loc[data_inicio_5anos:data_corte]

# Inverte a ordem do DataFrame para que as datas mais recentes fiquem em cima
ipca_filtrado = ipca_filtrado.iloc[::-1]

# Remove a hora da coluna 'date' apenas no DataFrame para formatar as datas
ipca_filtrado.index = pd.to_datetime(ipca_filtrado.index).strftime('%d/%m/%Y')

# Formata os valores para adicionar o símbolo de '%'
ipca_filtrado = ipca_filtrado.applymap(lambda x: f"{x:.2f} %")

# Layout 1 em duas colunas
col1, col2 = st.columns(2)

# Coluna 1: Gráfico
with col1:
    st.title("IPCA")
    st.caption("Dados retirados do Banco Central (5 anos)")
    st.dataframe(ipca_filtrado, use_container_width=True)  # Exibe os dados com '%' e usa toda a largura da coluna

# Coluna 2: Exibe o DataFrame dos últimos 5 anos (invertido), com '%' ao lado dos valores
with col2:
    #st.title("Evolução do IPCA (12 meses)")
    
    # Verifica se o DataFrame não está vazio
    if not ipca_5anos.empty:
        # Criação do gráfico
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=ipca_5anos.loc[data_inicio_5anos:data_corte].index,
                y=ipca_5anos.loc[data_inicio_5anos:data_corte].values.flatten(),  # Transforma em vetor simples
                #mode="lines",
                mode='markers+lines',
                name="IPCA (5 anos)",
            )
        )
        
        # Ajustes no layout do gráfico
        fig.update_layout(
            title="Histórico de IPCA (Últimos 5 anos)",
            xaxis_title="Escolha o período",
            yaxis_title="IPCA (%)",
            xaxis_rangeslider_visible=True,  # Controle de zoom (range slider)
            xaxis_range=[data_inicio_12meses, data_corte],  # Mostra apenas os últimos 12 meses inicialmente
        )

        # Exibe o gráfico interativo no Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Dados do IPCA não disponíveis.")

st.divider()

# Layout 2 em duas colunas
col1, col2 = st.columns(2)

with col1:
    # Exibe os títulos encontrados e suas porcentagens
    media_ntnb_local, titulos_info = exibir_resultados()
    
    if titulos_info:
        st.title("Títulos IPCA+ encontrados")
        st.caption(f"<p class='reduced-space'>Busca automática no site do <a href='{url_investidor10}' target='_blank'>Investidor10</a></p>", unsafe_allow_html=True)
        
        # Converte os resultados para um DataFrame
        df_titulos = pd.DataFrame(titulos_info, columns=['Título', 'Porcentagem'])
        
        # Substitui a vírgula por ponto e converte a coluna 'Porcentagem' para float
        df_titulos['Porcentagem'] = df_titulos['Porcentagem'].str.replace(',', '.').astype(float)
        
        # Calcula a média da coluna 'Porcentagem'
        media_porcentagem = df_titulos['Porcentagem'].mean()

        # Adiciona a média como última linha do DataFrame
        df_titulos.loc[len(df_titulos)] = ['Média de títulos NTN-B', media_porcentagem]
        
        # Aplica o símbolo de porcentagem a todos os valores da coluna 'Porcentagem'
        df_titulos['Porcentagem'] = df_titulos['Porcentagem'].apply(lambda x: f"{x:.2f} %")
        
        # Exibe o DataFrame
        st.dataframe(df_titulos, use_container_width=True)
    else:
        st.write("Nenhum título IPCA+ encontrado ou ocorreu um erro.")

with col2:
    st.write("Texto")