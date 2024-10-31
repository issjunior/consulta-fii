from config import *
from dividendos import *
from calculos import *
from constantes import *
import yfinance as yf

def main():
    exibir_cabecalho()
    ticker = input("Qual o ticker: ").upper() + ".SA"
    
    try:
        media_dividendos = obter_media_dividendos(ticker)
        
        if media_dividendos is None:
            print(f"Código {AMARELO}{ticker}{RESET} não encontrado.")
            return
        
        spread = float(input("Qual o spread (risco) do fundo: ").replace(",", "."))
        
        total_dividendos = calcular_total_dividendos(media_dividendos)
        
        acao = yf.Ticker(ticker)
        preco_atual = acao.info.get("currentPrice", None)
        media_dividendos_porcentagem = calcular_media_dividendos_porcentagem(total_dividendos, preco_atual)
        preco_teto = calcular_preco_teto(total_dividendos, media_ntnb, spread)
        cotas_necessarias = calcular_cotas_necessarias(preco_atual, media_dividendos)
        valor_cotas_magicnumber = calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual)
        
        # Exibição dos Resultados
        print(f"{VERMELHO}{'#'*15} Resultados do {ticker.replace('.SA', '')} {'#'*15}{RESET}")
        print(f"{acao.info['longName']}")
        print(f"Cotação atual: {AMARELO}{moeda(preco_atual)}{RESET}")
        print(f"A média dos dividendos nos últimos 12 meses é de {AMARELO}{moeda(media_dividendos)}{RESET} equivalente a {AMARELO}{media_dividendos_porcentagem:.2f}%{RESET} nos últimos 12 meses")
        print(f"Total dividendos recebidos em 12 meses é {AMARELO}{moeda(total_dividendos)}{RESET}")
        print(f"O preço teto seria de {VERMELHO}{moeda(preco_teto)}{RESET} com o spread de {AMARELO}{spread:.2f}%{RESET}")
        print(f"O magic number do {AMARELO}{ticker.replace('.SA', '')}{RESET} é de {AMARELO}{cotas_necessarias}{RESET} cotas")
        print(f"Seria necessário {AMARELO}{moeda(valor_cotas_magicnumber)}{RESET} para alcançar a quantidade de cotas do magic number")
    
    except KeyError:
        print(f"{VERMELHO}Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.{RESET}")

if __name__ == "__main__":
    main()
