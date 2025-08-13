import yfinance as yf
from datetime import datetime, timedelta

def obter_media_dividendos(ticker):
    acao = yf.Ticker(ticker)
    dividendos = acao.dividends

    if not dividendos.empty:
        hoje = datetime.now()
        doze_meses_atras = hoje - timedelta(days=365)
        dividendos_12_meses = dividendos[dividendos.index >= doze_meses_atras.strftime('%Y-%m-%d')]
        
        if not dividendos_12_meses.empty:
            return dividendos_12_meses.mean()
    
    return None
