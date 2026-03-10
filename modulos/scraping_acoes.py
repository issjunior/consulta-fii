import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(ttl=10800)
def obter_dados_acao(ticker):
    url = f"https://investidor10.com.br/acoes/{ticker}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontra todos os divs com a classe "cell"
        celulas = soup.find_all('div', class_='cell')

        dados = {
            "Segmento": None,
            "Tag Along": None,
            "Free Float": None,
        }

        # Processa cada célula encontrada
        for celula in celulas:
            texto = celula.get_text(strip=True)

            for chave in dados.keys():
                if chave.lower() in texto.lower():
                    # Extrai o valor removendo o rótulo
                    valor = texto.replace(chave, '').strip()
                    dados[chave] = valor
                    break

        return dados
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a página: {e}")
        return None
    except Exception as e:
        st.error(f"Erro ao processar a página: {e}")
        return None