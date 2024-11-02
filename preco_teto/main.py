from config import *
from scraping_ntnb import exibir_resultados, media_ntnb
from dividendos import *
from calculos import *
import yfinance as yf

def main():
    media_ntnb_local = exibir_resultados()  # Recebe o valor atualizado da variavel "media_ntnb" do scraping_ntnb.py
    #exibir_resultados()
    exibir_cabecalho()
    
    ticker = input("Qual o ticker: ").upper() + ".SA"
    
    try:
        media_dividendos = obter_media_dividendos(ticker)
        
        if media_dividendos is None:
            print(f"Código {AMARELO}{ticker}{RESET} não encontrado.")
            return
        
        spread = float(input("Qual o spread (risco) do FII: ").replace(",", "."))
        
        total_dividendos = calcular_total_dividendos(media_dividendos)
        
        acao = yf.Ticker(ticker)
        preco_atual = acao.info.get("currentPrice", None)
        media_dividendos_porcentagem = calcular_media_dividendos_porcentagem(total_dividendos, preco_atual)
#       preco_teto = calcular_preco_teto(total_dividendos, media_ntnb, spread)
        preco_teto = calcular_preco_teto(total_dividendos, media_ntnb_local, spread)
        print(f"valor do total dividendos:{total_dividendos}, media NTNB:{media_ntnb_local:.2f} e spread:{spread}") # printar variaveis
        cotas_necessarias = calcular_cotas_necessarias(preco_atual, media_dividendos)
        valor_cotas_magicnumber = calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual)
        
        # Exibição dos Resultados
        print(f"{VERMELHO}{'#'*15} Resultados do {ticker.replace('.SA', '')} {'#'*15}{RESET}")
        print(f"{acao.info['longName']}")
        print(f"Cotação atual: {AMARELO}{real(preco_atual)}{RESET}")
        print(f"A média dos dividendos nos últimos 12 meses é de {AMARELO}{real(media_dividendos)}{RESET} equivalente a {AMARELO}{media_dividendos_porcentagem:.2f}%{RESET} nos últimos 12 meses")
        print(f"Total dividendos recebidos em 12 meses é {AMARELO}{real(total_dividendos)}{RESET}")
        print(f"O preço teto seria de {VERMELHO}{real(preco_teto)}{RESET} com o spread de {AMARELO}{spread:.2f}%{RESET}")
        print(f"O magic number do {AMARELO}{ticker.replace('.SA', '')}{RESET} é de {AMARELO}{cotas_necessarias}{RESET} cotas")
        print(f"Seria necessário {AMARELO}{real(valor_cotas_magicnumber)}{RESET} para alcançar a quantidade de cotas do magic number")
    
    except KeyError:
        print(f"{VERMELHO}Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.{RESET}")

if __name__ == "__main__":
    main()
