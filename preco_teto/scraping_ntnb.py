from config import *
import requests
from bs4 import BeautifulSoup
import re
import statistics
import colorama
from colorama import Fore, Style

url = "https://investidor10.com.br/tesouro-direto/"


def scrape_tesouro_ipca():
    """
    Realiza web scraping do site Investidor 10 para obter título e porcentagem dos títulos IPCA+
    Returns:
        list: Lista com tuplas (título, porcentagem) dos títulos IPCA+
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        titulos_info = []
        
        elementos = soup.find_all('tr')
        
        for elemento in elementos:
            texto = elemento.get_text(strip=True)
            if 'IPCA+' in texto:
                # Usando regex para extrair o título e a porcentagem
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
    """
    Calcula a média das taxas encontradas
    """
    taxas = []
    for _, taxa in titulos_info:
        # Converte a taxa de string para float, substituindo ',' por '.'
        taxa_float = float(taxa.replace(',', '.'))
        taxas.append(taxa_float)
    
    return statistics.mean(taxas) if taxas else 0

media_ntnb = 0  # Declaração global para passagem de valor para a variavel "media_ntnb_local" no main.py 

def exibir_resultados():
    titulos_info = scrape_tesouro_ipca()
    
    if titulos_info:
        print(f"{Fore.LIGHTRED_EX}{'#'*15} Buscando titulos IPCA+ {'#'*15}{Style.RESET_ALL}")
        print(f"Títulos encontrados em {Fore.BLUE}{url}{Style.RESET_ALL}")
        
        for titulo, porcentagem in titulos_info:
            print(f"{titulo} - Rentabilidade anual: IPCA + {porcentagem}%")
        
        # Calcula e define a média
        media_ntnb = calcular_media_taxas(titulos_info)
        print("="*40)
        print(f"Média das taxas: {Fore.YELLOW}{media_ntnb:.2f}%{Style.RESET_ALL}")
        print("="*40)
    else:
        print("Nenhum título IPCA+ encontrado ou ocorreu um erro.")
    
    return media_ntnb # Retorna o valor de media_ntnb para uso no main.py com a variavel "media_ntnb_local"

if __name__ == "__main__":
    exibir_resultados()