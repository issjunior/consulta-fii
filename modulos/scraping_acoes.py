import requests
from bs4 import BeautifulSoup
import streamlit as st
import re

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

        st.write(f"Fonte: {url}")

        dados = {
            "Segmento": None,
            "Tag Along": None,
            "Free Float": None,
            "PAYOUT": None,
            "LPA": None,
        }

        def extract_numeric_value(text):
            """Converte texto numérico no formato brasileiro para float."""
            if '.' in text and ',' in text:
                text = text.replace('.', '').replace(',', '.')
            else:
                text = text.replace(',', '.')
            try:
                return float(text)
            except ValueError:
                return None

        # Captura informações gerais (Segmento, Tag Along, Free Float)
        for celula in soup.find_all('div', class_='cell'):
            texto = celula.get_text(strip=True)
            for chave in ["Segmento", "Tag Along", "Free Float"]:
                if chave.lower() in texto.lower():
                    dados[chave] = texto.replace(chave, '').strip()

        # Captura o PAYOUT
        node = soup.find(text=re.compile(r'PAYOUT', re.I))
        if node:
            parent = node.parent
            m = re.search(r'([\d.,]+%)', parent.get_text())
            if not m and parent.find_next_sibling():
                m = re.search(r'([\d.,]+%)', parent.find_next_sibling().get_text())
            if m:
                dados["PAYOUT"] = m.group(1)

        # Captura o LPA
        label_text = soup.find(text=re.compile(r'\bLPA\b', re.I))
        lpa_value = None

        if label_text:
            parent = label_text.parent
            text_parent = parent.get_text(" ", strip=True)
            m = re.search(r'LPA[^0-9\-:,]*([0-9\.,]+)', text_parent, re.I)
            if m:
                lpa_value = m.group(1)
            else:
                next_num = parent.find_next(string=re.compile(r'[0-9]{1,3}[.,][0-9]{1,3}'))
                if next_num:
                    lpa_value = next_num.strip()

        if not lpa_value:
            for td in soup.find_all(['td', 'th']):
                if td.get_text(strip=True).upper() == 'LPA':
                    sib = td.find_next_sibling(['td', 'th'])
                    if sib:
                        v = re.search(r'([0-9\.,]+)', sib.get_text())
                        if v:
                            lpa_value = v.group(1)
                            break

        if not lpa_value:
            fallback = soup.find(string=re.compile(r'\d+,\d{1,3}'))
            if fallback:
                lpa_value = re.search(r'([0-9\.,]+)', fallback).group(1)

        if lpa_value:
            dados["LPA"] = extract_numeric_value(lpa_value)

        return dados

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar a página: {e}")
        return None
    except Exception as e:
        st.error(f"Erro ao processar a página: {e}")
        return None