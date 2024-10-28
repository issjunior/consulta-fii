import yfinance as yf

ativo = yf.Ticker('TRXF11.SA')
#print(f"{ativo.dividends}") #traz todos os dividendos
#print(f"{ativo.info}") #traz informações
print(f"{ativo.info['longName']}")
#print(f"{ativo.info['address1']}") #traz informação especifica
#print(f"{ativo.info['dividendRate']}") #DY por ano
