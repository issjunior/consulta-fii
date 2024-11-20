from datetime import datetime
from babel.numbers import format_currency

# Função auxiliar para formatar valores monetários com a biblioteca babel
def real(valor):
    return format_currency(valor, 'BRL', locale='pt_BR')

def dolar(valor):
    return format_currency(valor, 'USD', locale='en_US')

# Função auxiliar para formatar valores como porcentagem
def porcentagem(valor):
    return f"{valor:.2f}%".replace('.', ',')