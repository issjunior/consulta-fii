# IMPORTAÇÃO DE BIBLIOTECAS
from datetime import datetime, timedelta
import yfinance as yf

# Código ANSI para uso de cores
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
RESET = '\033[0m'  # Reseta a cor para o padrão

# CONSTANTES
media_ntnb = 6.41

print(f"{VERMELHO}{'#'*15} Cálculo de preço teto de FII {'#'*15}{RESET}")
data_hora_atual = datetime.now()
print(f"{AZUL}{data_hora_atual.strftime('%d/%m/%Y as %H:%M:%S')}{RESET}")
print(f"Média NTN-B: {AMARELO}{media_ntnb}{"%"}{RESET}")

# INPUTs
ticker = input(f"Qual o ticker: ").upper()
ticker = ticker + ".SA"

try:
    # Obter o ticker do ativo
    acao = yf.Ticker(ticker)

    # Obter o histórico de dividendos
    dividendos = acao.dividends

    # Verificar se há dados de dividendos
    if not dividendos.empty:
        # Filtrar dividendos dos últimos 12 meses
        hoje = datetime.now()
        doze_meses_atras = hoje - timedelta(days=365)
        dividendos_12_meses = dividendos[dividendos.index >= doze_meses_atras.strftime('%Y-%m-%d')]

        # Verificar se há dividendos nos últimos 12 meses
        if not dividendos_12_meses.empty:
            # Calcular a média dos dividendos dos últimos 12 meses
           media_dividendos = dividendos_12_meses.mean()
        else:
            print(f"Não há dividendos registrados para {ticker} nos últimos 12 meses.")
except KeyError:
    print(f"Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.")

spread = float(input(f"Qual o spread (risco) do fundo: ").replace(",", "."))

# CALCULOS
total_dividendos = media_dividendos * 12
preco_atual = acao.info.get("currentPrice", None)
media_dividendos_porcentagem = (total_dividendos/preco_atual) * 100
preco_teto = total_dividendos/(media_ntnb + spread)*100

# RESULTADOS
print(f"{VERMELHO}{'#'*15} Resultados do {ticker.replace('.SA', '')} {'#'*15}{RESET}")
print(f"Cotação atual: {AMARELO}{'R$ '}{preco_atual}{RESET}")
print(f"A média dos dividendos nos últimos 12 meses é de {AMARELO}R$ {media_dividendos:.2f}{RESET} equivalente a {AMARELO}{media_dividendos_porcentagem:.2f}%{RESET} nos últimos 12 meses")
print(f"Total dividendos recebidos em 12 meses é {AMARELO}R$ {total_dividendos:.2f}{RESET}")
print(f"O preço teto seria de {VERMELHO}R$ {preco_teto:.2f}{RESET} com o spread de {AMARELO}{spread}%{RESET}")