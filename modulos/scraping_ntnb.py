from config import *
import requests
from bs4 import BeautifulSoup
import re
import statistics
import streamlit as st

url_investidor10 = "https://investidor10.com.br/tesouro-direto/"

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def scrape_tesouro_ipca():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url_investidor10, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        titulos_info = []
        
        elementos = soup.find_all('tr')
        
        for elemento in elementos:
            texto = elemento.get_text(strip=True)
            if 'IPCA+' in texto:
                titulo_match = re.search(r'(Tesouro IPCA\+ \d{4})', texto)
                porcentagem_match = re.search(r'IPCA \+ (\d+,\d+)%', texto)
                
                if titulo_match and porcentagem_match:
                    titulo = titulo_match.group(1)
                    porcentagem = porcentagem_match.group(1)
                    titulos_info.append((titulo, porcentagem))
        
        return titulos_info
        
    except requests.RequestException as e:
        print(f"Erro ao acessar o site: {e}")
        return []
    except Exception as e:
        print(f"Erro durante o scraping: {e}")
        return []

def calcular_media_taxas(titulos_info):
    taxas = []
    for _, taxa in titulos_info:
        taxa_float = float(taxa.replace(',', '.'))
        taxas.append(taxa_float)
    
    return statistics.mean(taxas) if taxas else 0

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def exibir_resultados():
    titulos_info = scrape_tesouro_ipca()
    
    if titulos_info:
        media_ntnb = calcular_media_taxas(titulos_info)
    else:
        media_ntnb = 0

    return media_ntnb, titulos_info  # Retorna a média e a lista de títulos
