import requests
from bs4 import BeautifulSoup
import streamlit as st
import time

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
def obter_pvp(ticker):
    ticker = ticker.replace(".SA", "")
    url = f"https://investidor10.com.br/fiis/{ticker}"

    # Rate limiting: pause before request to avoid hammering the site
    time.sleep(1.5)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            verify=True
        )
        response.raise_for_status()  # Will raise HTTPError for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')

        # Procura por um span específico que contém o valor do P/VP
        span = soup.find('span', string='P/VP')
        if span:
            pvp_span = span.find_next('span')
            if pvp_span:
                pvp = pvp_span.text.strip()

                # Remove possíveis caracteres não numéricos e converte para float
                pvp = pvp.replace(',', '.')  # Substitui vírgulas por pontos
                # Additional cleanup: remove any non-numeric characters except dot and minus
                pvp = ''.join(c for c in pvp if c.isdigit() or c in '.-')
                return float(pvp) if pvp else None

        # Caso o P/VP não seja encontrado
        return None

    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout ao acessar a página do FII - possivelmente bloqueado ou lento.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Erro de conexão ao acessar a página do FII - verifique se o IP está bloqueado.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("🔒 Erro 401: Não autorizado ao acessar a página do FII - possível bloqueio de IP.")
        elif e.response.status_code == 403:
            st.error("🚫 Erro 403: Acesso negado à página do FII - IP provavelmente bloqueado.")
        elif e.response.status_code == 404:
            st.error("❌ Erro 404: Página do FII não encontrada - verifique o ticker.")
        elif e.response.status_code == 429:
            st.error("⏳ Erro 429: Muitas requisições - limite de taxa excedido.")
        else:
            st.error(f"🌐 Erro HTTP {e.response.status_code}: {e.response.reason}")
        return None
    except Exception as e:
        st.error(f"💥 Erro inesperado ao processar a página do FII: {e}")
        return None