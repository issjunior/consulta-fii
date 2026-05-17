import requests
from bs4 import BeautifulSoup
import re
import statistics
import streamlit as st
import time

# URL pública do Investidor10 para tesouro direto (usada em outros módulos)
url_investidor10 = "https://investidor10.com.br/tesouro-direto/"

# Enhanced headers to mimic a real browser and reduce blocking chances
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'
}

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def scrape_tesouro_ipca():
    url_investidor10 = "https://investidor10.com.br/tesouro-direto/"

    # Rate limiting: pause before request to avoid hammering the site
    time.sleep(1.5)

    try:
        response = requests.get(
            url_investidor10,
            headers=HEADERS,
            timeout=20,  # Increased timeout for potentially slower connections in cloud
            verify=True
        )
        response.raise_for_status()  # Will raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        titulos_info = []

        elementos = soup.find_all('tr')

        for elemento in elementos:
            texto = elemento.get_text(strip=True)
            if 'Tesouro IPCA+' in texto:
                titulo_match = re.search(r'(Tesouro IPCA\+[^\d%\n]*)', texto)
                porcentagem_match = re.search(r'IPCA \+\s*(\d+,\d+)%', texto)

                if titulo_match and porcentagem_match:
                    titulo = titulo_match.group(1).strip()
                    porcentagem = porcentagem_match.group(1)
                    titulos_info.append((titulo, porcentagem))

        return titulos_info

    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout ao acessar o site de tesouro - possivelmente bloqueado ou lento.")
        return []
    except requests.exceptions.ConnectionError:
        st.error("🔌 Erro de conexão ao acessar o site de tesouro - verifique se o IP está bloqueado.")
        return []
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("🔒 Erro 401: Não autorizado ao acessar o site de tesouro - possível bloqueio de IP.")
        elif e.response.status_code == 403:
            st.error("🚫 Erro 403: Acesso negado ao site de tesouro - IP provavelmente bloqueado.")
        elif e.response.status_code == 429:
            st.error("⏳ Erro 429: Muitas requisições - limite de taxa excedido.")
        else:
            st.error(f"🌐 Erro HTTP {e.response.status_code}: {e.response.reason}")
        return []
    except Exception as e:
        st.error(f"💥 Erro inesperado durante o scraping de tesouro: {e}")
        return []


@st.cache_data(ttl=10800)
def scrape_tesouro_ipca_2040():
    """Retorna a taxa do Tesouro IPCA+ 2040 ou None se não for encontrado."""
    titulos_info = scrape_tesouro_ipca()
    for titulo, porcentagem in titulos_info:
        if titulo == "Tesouro IPCA+ 2040":
            try:
                return float(porcentagem.replace(',', '.'))
            except ValueError:
                return None
    return None


def calcular_media_taxas(titulos_info):
    if not titulos_info:
        return 0
    taxas = []
    for _, taxa in titulos_info:
        taxa_float = float(taxa.replace(',', '.'))
        taxas.append(taxa_float)

    return statistics.mean(taxas) if taxas else 0

@st.cache_data(ttl=10800)  # TTL em segundos (10800 segundos = 3 horas)
def exibir_resultados(manual_ntnb=None):
    """Obtém a média da taxa NTN‑B e a lista de títulos.
    Caso o scraping não retorne nenhum título (por bloqueio ou mudança de layout),
    a função devolve ``0`` como média e exibe um aviso no Streamlit para que o usuário
    saiba que não foi possível coletar os dados.

    Se o usuário informar um valor manual em ``manual_ntnb``, esse valor será usado
    como média em vez da média calculada automaticamente.
    """
    # Pequena pausa para respeitar o servidor
    time.sleep(1)
    titulos_info = scrape_tesouro_ipca()

    if manual_ntnb is not None:
        media_ntnb = manual_ntnb
    else:
        if titulos_info:
            media_ntnb = calcular_media_taxas(titulos_info)
        else:
            media_ntnb = 0

    return media_ntnb, titulos_info  # Retorna a média e a lista de títulos