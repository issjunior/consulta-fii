import yfinance as yf
import pandas as pd

def obter_dados_bitcoin():
    data_corte = pd.to_datetime("today").normalize()
    data_inicio = data_corte - pd.DateOffset(years=2)  # período de pesquisa
    
    dados_btc = yf.download("BTC-USD", start=data_inicio, end=data_corte)
    dados_btc.drop(columns=["Adj Close", "Open", "Volume"], inplace=True)  # exclui colunas desnecessárias
    dados_btc = dados_btc.sort_index(ascending=False)
    
    # Ajusta o índice para o formato de data brasileiro (dd/mm/aaaa)
    dados_btc.index = pd.to_datetime(dados_btc.index).strftime('%d/%m/%Y')
    
    return dados_btc, data_inicio, data_corte
