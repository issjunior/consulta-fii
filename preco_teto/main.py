from config import *
from scraping_ntnb import exibir_resultados, media_ntnb
from dividendos import *
from calculos import *
from colorama import Fore, Style
import colorama
import yfinance as yf

# Inicializa o colorama para suportar de cores
colorama.init()

def main():
    media_ntnb_local = exibir_resultados()  # Recebe o valor atualizado da variavel "media_ntnb" do scraping_ntnb.py
    exibir_cabecalho()
    
    ticker = input("Qual o ticker: ").upper() + ".SA"
    
    try:
        media_dividendos = obter_media_dividendos(ticker)
        
        if media_dividendos is None:
            print(f"Código {Fore.YELLOW}{ticker}{Style.RESET_ALL} não encontrado.")
            return
        
        spread = float(input("Qual o spread (risco) do FII: ").replace(",", "."))
        
        total_dividendos = calcular_total_dividendos(media_dividendos)
        
        acao = yf.Ticker(ticker)
        preco_atual = acao.info.get("currentPrice", None)
        media_dividendos_porcentagem = calcular_media_dividendos_porcentagem(total_dividendos, preco_atual)
        preco_teto = calcular_preco_teto(total_dividendos, media_ntnb_local, spread)
        cotas_necessarias = calcular_cotas_necessarias(preco_atual, media_dividendos)
        valor_cotas_magicnumber = calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual)
        
        # Exibição dos Resultados
        print(f"{Fore.LIGHTRED_EX}{'#'*16} Resultados do {ticker.replace('.SA', '')} {'#'*16}{Style.RESET_ALL}")
        print(f"{acao.info['longName']}")
        print(f"Cotação atual        -> {Fore.YELLOW}{real(preco_atual)}{Style.RESET_ALL}")
        print(f"Variação da cota     -> {Fore.YELLOW}{real(acao.info['fiftyTwoWeekLow'])}{Style.RESET_ALL} <-> {Fore.YELLOW}{real(acao.info['fiftyTwoWeekHigh'])}{Style.RESET_ALL}")
        print(f"Média dividendos     -> {Fore.YELLOW}{real(media_dividendos)}{Style.RESET_ALL} equivalente a {Fore.YELLOW}{media_dividendos_porcentagem:.2f}%{Style.RESET_ALL} nos últimos 12 meses")
        print(f"Dividendos recebidos -> {Fore.YELLOW}{real(total_dividendos)}{Style.RESET_ALL}")
        print(f"Preço teto           -> {Fore.LIGHTRED_EX}{real(preco_teto)}{Style.RESET_ALL} com o spread de {Fore.YELLOW}{spread:.2f}%{Style.RESET_ALL}")
        print(f"O magic number       -> {Fore.YELLOW}{cotas_necessarias}{Style.RESET_ALL} cotas")
        print(f"Cotas necessárias    -> {Fore.YELLOW}{real(valor_cotas_magicnumber)}{Style.RESET_ALL} cotas")
        print(f"Cap rate             ->")

    except KeyError:
        print(f"{Fore.CYAN}Erro: Não foi possível encontrar dados para o ticker '{ticker}'. Verifique se o ticker está correto.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
