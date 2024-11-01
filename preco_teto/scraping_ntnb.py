import requests
from bs4 import BeautifulSoup
from config import VERMELHO, RESET

link = "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm"

# Definindo os cabeçalhos para a requisição
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"}

# Fazendo a solicitação com os cabeçalhos
requisicao = requests.get(link, headers=headers)

site = BeautifulSoup(requisicao.text, "html.parser")
#print(site.prettify()) # organiza o código HTML
#rentabilidade = site.find_all("table")
#print(rentabilidade)

print(f"{VERMELHO}A Cloudflare bloqueia o conteúdo do Tesouro Direto.{RESET}\n"
      f"{VERMELHO}Projeto no aguardo de outro site que seja possivel a raspagem dos dados necessários.{RESET}")
