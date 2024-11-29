import requests
from bs4 import BeautifulSoup
import streamlit as st

# URL da página
url_alternative = "https://alternative.me/crypto/fear-and-greed-index/"

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def alternative():
    # Fazendo a requisição para obter o conteúdo da página
    response = requests.get(url_alternative)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscando as informações nas tags div.fng-circle
    fear_greed_info = soup.find_all('div', class_='fng-circle')

    # Extraindo os valores de cada período
    btc_fear_greed_now = fear_greed_info[0].get_text(strip=True) if len(fear_greed_info) > 0 else 'N/A'
    btc_fear_greed_yesterday = fear_greed_info[1].get_text(strip=True) if len(fear_greed_info) > 1 else 'N/A'
    btc_fear_greed_last_week = fear_greed_info[2].get_text(strip=True) if len(fear_greed_info) > 2 else 'N/A'
    btc_fear_greed_last_month = fear_greed_info[3].get_text(strip=True) if len(fear_greed_info) > 3 else 'N/A'

    return btc_fear_greed_now, btc_fear_greed_yesterday, btc_fear_greed_last_week, btc_fear_greed_last_month

# Exibindo os resultados
# print(f"Now: {btc_fear_greed_now}")
# print(f"Yesterday: {btc_fear_greed_yesterday}")
# print(f"Last week: {btc_fear_greed_last_week}")
# print(f"Last month: {btc_fear_greed_last_month}")
