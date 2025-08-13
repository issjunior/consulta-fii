from datetime import datetime
from babel.numbers import format_currency

# Função auxiliar para formatar valores monetários com a biblioteca babel
def real(valor):
    try:
        valor = float(valor)  # Tenta converter o valor para um número
        return format_currency(valor, 'BRL', locale='pt_BR')
    except (ValueError, TypeError):
        return "N/A"  # Retorna um valor padrão em caso de erro

def dolar(valor):
    return format_currency(valor, 'USD', locale='en_US')

# Função auxiliar para formatar valores como porcentagem
def porcentagem(valor):
    return f"{valor:.2f}%".replace('.', ',')