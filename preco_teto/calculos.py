import math

def calcular_total_dividendos(media_dividendos):
    return media_dividendos * 12                 # media dividendos nos ultimos 12 meses

def calcular_preco_teto(total_dividendos, media_ntnb, spread):
    return total_dividendos / (media_ntnb + spread) * 100

def calcular_media_dividendos_porcentagem(total_dividendos, preco_atual):
    return (total_dividendos / preco_atual) * 100

def calcular_cotas_necessarias(preco_atual, media_dividendos): # calculo para do magic number
        return math.ceil(preco_atual / media_dividendos)

def calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual):
        return (cotas_necessarias * preco_atual)

def calcular_cap_rate(media_dividendos, preco_atual):
    return ((media_dividendos * 12) / preco_atual) * 100