from datetime import datetime
from babel.numbers import format_currency
import colorama
from colorama import Fore, Style

# funções
def exibir_cabecalho():
    print(f"{Fore.LIGHTRED_EX}{'#'*12} Cálculo de preço teto de FII {'#'*12}{Style.RESET_ALL}")

# Função auxiliar para formatar valores monetários com a biblioteca babel
def real(valor):
    return format_currency(valor, 'BRL', locale='pt_BR')

def dollar(valor):
    return format_currency(valor, 'USD', locale='en_US')

