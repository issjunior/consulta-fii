import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def obter_pvp(ticker):
    ticker = ticker.replace(".SA", "")
    url = f"https://investidor10.com.br/fiis/{ticker}"
    
    # Headers simulando um navegador real
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        )
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gera uma exceção para códigos de status 4xx e 5xx
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procura por um span específico que contém o valor do P/VP
        # Ajuste o identificador com base na inspeção do HTML
        span = soup.find('span', string='P/VP')
        if span:
            pvp_span = span.find_next('span')
            if pvp_span:
                pvp = pvp_span.text.strip()
                
                # Remove possíveis caracteres não numéricos e converte para float
                pvp = pvp.replace(',', '.')  # Substitui vírgulas por pontos
                return float(pvp) if pvp.replace('.', '', 1).isdigit() else None
        
        # Caso o P/VP não seja encontrado
        return None
    except requests.exceptions.RequestException as e:
        # Log de erro para debugging
        st.error(f"Erro ao acessar a página: {e}")
        return None
    except Exception as e:
        # Log de erro para debugging
        st.error(f"Erro ao processar a página: {e}")
        return None
