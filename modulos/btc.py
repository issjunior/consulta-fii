import yfinance as yf
import pandas as pd

def obter_dados_bitcoin():
    data_corte = pd.to_datetime("today").normalize()
    data_inicio = data_corte - pd.DateOffset(years=2)  # período de pesquisa
    
    dados_btc = yf.download(
        "BTC-USD",
        start=data_inicio,
        end=data_corte,
        auto_adjust=False  # garante que venha "Adj Close"
    )
    
    # Remove colunas apenas se existirem
    colunas_para_remover = [col for col in ["Adj Close", "Open", "Volume"] if col in dados_btc.columns]
    dados_btc.drop(columns=colunas_para_remover, inplace=True)
    
    dados_btc = dados_btc.sort_index(ascending=False)
    dados_btc.index = pd.to_datetime(dados_btc.index).strftime('%d/%m/%Y')
    
    return dados_btc, data_inicio, data_corte
