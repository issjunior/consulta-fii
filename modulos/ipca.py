import streamlit as st
from bcb import sgs
import pandas as pd
import plotly.graph_objects as go

# Função para obter dados do IPCA
@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def obter_ipca():
    try:
        # Obtém os dados do IPCA (5 anos)
        ipca_5anos = sgs.get(13522)  # busco o código '13522' no https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
        if ipca_5anos is None or ipca_5anos.empty:  # Verifica se a resposta é inválida
            raise ValueError("Nenhum dado foi retornado para o IPCA.")
    except Exception as erro_busca_ipca:
        st.warning("Não foi possível obter os dados do IPCA (5 anos). Verifique sua conexão ou tente novamente mais tarde.")
        st.warning("Consulte o link: https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries código: 13522")
        st.error(f"Código do erro: {erro_busca_ipca}")
        return None, None, None, None  # Retorna valores default em caso de erro

    # Define a data de corte como a última data disponível
    data_corte = pd.to_datetime("today").normalize()

    # Define o período padrão para 5 anos e os últimos 12 meses
    data_inicio_5anos = data_corte - pd.DateOffset(years=5)  # 5 anos de histórico

    # Filtra os dados para os últimos 5 anos
    ipca_filtrado = ipca_5anos.loc[data_inicio_5anos:data_corte]

    # Inverte a ordem do DataFrame para que as datas mais recentes fiquem em cima
    ipca_filtrado = ipca_filtrado.iloc[::-1]

    # Remove a hora da coluna 'date' apenas no DataFrame para formatar as datas
    ipca_filtrado.index = pd.to_datetime(ipca_filtrado.index).strftime('%d/%m/%Y')

    # Converte a coluna IPCA para float (caso necessário) e formata com o símbolo de '%'
    ipca_filtrado = ipca_filtrado.apply(pd.to_numeric, errors='coerce')  # Garante que os valores sejam numéricos
    ipca_filtrado_formatado = ipca_filtrado.map(lambda x: f"{x:.2f} %" if isinstance(x, (int, float)) else x)

    return ipca_filtrado_formatado, ipca_5anos, data_inicio_5anos, data_corte

# Função para criar o gráfico
@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def criar_grafico_ipca(ipca_5anos, data_inicio_5anos, data_corte):
    # Define o início do intervalo como 12 meses atrás
    data_inicio_12meses = data_corte - pd.DateOffset(years=1)

    # Filtra os dados para os últimos 5 anos
    ipca_filtrado_5anos = ipca_5anos.loc[data_inicio_5anos:data_corte]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=ipca_filtrado_5anos.index,
            y=ipca_filtrado_5anos.values.flatten(),  # Transforma em vetor simples
            mode='markers+lines',
            name="IPCA (5 anos)",
            hovertemplate="<b>Data:</b> %{x}<br><b>IPCA:</b> %{y:.2f} %<extra></extra>",
        )
    )
    
    # Ajustes no layout do gráfico
    fig.update_layout(
        title="Histórico de IPCA (Últimos 5 anos)",
        xaxis_title="Período",
        yaxis_title="IPCA (%)",
        xaxis_rangeslider_visible=True,  # Controle de zoom (range slider)
        xaxis_range=[data_inicio_12meses, data_corte],  # Mostra os últimos 12 meses inicialmente
    )
    
    return fig


# Função para processar os títulos e adicionar a soma
@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def processar_titulos(titulos_info, ultimo_ipca_formatado):
    # Converte os resultados para um DataFrame
    df_titulos = pd.DataFrame(titulos_info, columns=['Título', 'Porcentagem'])

    # Substitui a vírgula por ponto e converte a coluna 'Porcentagem' para float
    df_titulos['Porcentagem'] = df_titulos['Porcentagem'].str.replace(',', '.').astype(float)

    # Calcula a média da coluna 'Porcentagem'
    media_porcentagem = df_titulos['Porcentagem'].mean()

    # Adiciona a média como última linha do DataFrame
    df_titulos.loc[len(df_titulos)] = ['Média de títulos NTN-B', media_porcentagem]

    # Aplica o símbolo de porcentagem a todos os valores da coluna 'Porcentagem'
    df_titulos['Porcentagem'] = df_titulos['Porcentagem'].map(lambda x: f"{x:.2f} %")

    # Converte o valor do último IPCA para um número, removendo o '%'
    ultimo_ipca_num = float(ultimo_ipca_formatado.replace(' %', ''))

    # Cria a nova coluna 'Último IPCA' com o valor formatado
    df_titulos['Último IPCA'] = ultimo_ipca_formatado

    # Soma da coluna 'Porcentagem' (convertida para número) e 'Último IPCA' (convertido para número)
    df_titulos['Soma'] = df_titulos['Porcentagem'].str.replace(' %', '').astype(float) + ultimo_ipca_num

    # Formata a nova coluna 'Soma' para exibir como porcentagem
    df_titulos['Soma'] = df_titulos['Soma'].map(lambda x: f"{x:.2f} %")

    return df_titulos
