from datetime import datetime
from babel.numbers import format_currency

# funções
def exibir_cabecalho():
    print(f"{'#'*12} Cálculo de preço teto de FII {'#'*12}")

# Função auxiliar para formatar valores monetários com a biblioteca babel
def real(valor):
    return format_currency(valor, 'BRL', locale='pt_BR')

def dollar(valor):
    return format_currency(valor, 'USD', locale='en_US')

