import requests
from bs4 import BeautifulSoup

# URL do site
url_ibge = 'https://www.ibge.gov.br/explica/inflacao.php'

# Realiza a requisição GET para o site
response = requests.get(url_ibge)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parse do conteúdo HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra todos os elementos <p> com a classe 'variavel-dado'
    ipca_elements = soup.find_all('p', class_='variavel-dado')

    # Verifica se existe pelo menos dois elementos encontrados
    if len(ipca_elements) >= 2:
        # Pega o segundo elemento e retorna seu valor
        ipca_value = ipca_elements[1].text.strip()
    else:
        ipca_value = None  # Ou qualquer outra ação se não encontrar o segundo elemento
else:
    ipca_value = None  # Ou qualquer outra ação em caso de falha na requisição
