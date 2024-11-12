import yfinance as yf

ativo = yf.Ticker('TRXF11.SA')
#print(f"{ativo.info['longName']}")
#print(f"{ativo.dividends}") #traz todos os dividendos
#print(f"{ativo.info}") #traz informações
#print(f"{ativo.info['address1']}") #traz informação especifica
#print(f"{ativo.info['currentPrice']}")
#print(f"{ativo.info['dividendRate']}") #Dividendo futuro e rendimento
#print(f"{ativo.info['trailingEps']}") #Lucro por Ação (LPA)
#print(f"{ativo.info['fiftyTwoWeekHigh']}") #Maior cotação nas últimas 52 semanas (1 ano)
#print(f"{ativo.info['fiftyTwoWeekLow']}") #Menor cotação nas últimas 52 semanas (1 ano)

# Carregar dados históricos para uma ação (por exemplo, Apple - AAPL)
ticker = yf.Ticker("HGLG11.SA")
#historico = ticker.history(period="2y")  # Dados dos últimos 1 ano
#print(historico.head())

# Dividendos
dividendos = ticker.dividends
print(dividendos)