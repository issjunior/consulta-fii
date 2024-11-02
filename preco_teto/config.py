from datetime import datetime
from babel.numbers import format_currency

# Cores ANSI
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
RESET = '\033[0m'

# funções
def exibir_cabecalho():
    print(f"{VERMELHO}{'#'*15} Cálculo de preço teto de FII {'#'*15}{RESET}")
 #  print(f"{AZUL}{'#'*15}{datetime.now().strftime(' %d/%m/%Y as %Hh:%Mm ')}{'#'*15}{RESET}")

# Função auxiliar para formatar valores monetários com a biblioteca babel
def real(valor):
    return format_currency(valor, 'BRL', locale='pt_BR')

def dollar(valor):
    return format_currency(valor, 'USD', locale='en_US')

