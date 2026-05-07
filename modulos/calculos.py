import math

def calcular_total_dividendos(media_dividendos):                            # media dividendos nos ultimos 12 meses
    return media_dividendos * 12

def calcular_preco_teto(total_dividendos, media_ntnb, spread, tx_crescimento_dy):
    """
    Calcula o preço teto (valor justo) usando o Modelo de Gordon.
    - total_dividendos: soma anual dos dividendos (R$)
    - media_ntnb: taxa média NTN‑B (%)
    - spread: prêmio de risco adicional (%), soma ao custo de capital
    - tx_crescimento_dy: taxa de crescimento esperada dos dividendos (%)
    """
    # custo de capital (r) em decimal
    custo_capital = (media_ntnb + spread) / 100.0
    # taxa de crescimento (g) em decimal
    taxa_crescimento = tx_crescimento_dy / 100.0
    # protege contra divisão por zero ou custo < crescimento
    if custo_capital <= taxa_crescimento:
        return None
    preco_teto = total_dividendos / (custo_capital - taxa_crescimento)
    return preco_teto

def calcular_media_dividendos_porcentagem(total_dividendos, preco_atual):
    return (total_dividendos / preco_atual) * 100

def calcular_cotas_necessarias(preco_atual, media_dividendos):              # calculo para do magic number
    return math.ceil(preco_atual / media_dividendos)

def calcular_valor_cotas_para_magicnumber(cotas_necessarias, preco_atual):
    return (cotas_necessarias * preco_atual)

def calcular_cap_rate_ajustado(media_dividendos, vacancia, preco_atual):    # calcula o CAP Rate ajustado
    vacancia = float(vacancia) if vacancia else 1.0                         # converte "vacancia" para float ou assume 1.0 se estiver vazia ou for zero
    if vacancia == 0:                                                       # referência: https://www.infomoney.com.br/guias/cap-rate/
        vacancia = 1.0
    return (((media_dividendos * 12) / (1 - vacancia/100)) / preco_atual) * 100



