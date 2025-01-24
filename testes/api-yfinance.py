import yfinance as yf

ativo = yf.Ticker('TRXF11.SA')
#print(f"{ativo.info}") #traz informações
#print(f"{ativo.info['longName']}")
#print(f"{ativo.dividends}") #traz todos os dividendos
#print(f"{ativo.info['address1']}") #traz informação especifica
#print(f"{ativo.info['currentPrice']}")
#print(f"{ativo.info['dividendRate']}") #Dividendo futuro e rendimento
#print(f"{ativo.info['trailingEps']}") #Lucro por Ação (LPA)
#print(f"{ativo.info['fiftyTwoWeekHigh']}") #Maior cotação nas últimas 52 semanas (1 ano)
#print(f"{ativo.info['fiftyTwoWeekLow']}") #Menor cotação nas últimas 52 semanas (1 ano)


# Símbolo do dólar em relação ao real
ticker = "USDBRL=X"

# Obtém os dados do ativo
dolar = yf.Ticker(ticker)

# Cotação atual
cotacao_atual = dolar.history(period="1d")['Close'].iloc[-1]

print(f"Cotação atual do dólar: R$ {cotacao_atual:.2f}")
