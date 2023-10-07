import numpy as np
import pandas as pd
import yfinance as yf
from prettytable import PrettyTable
from datetime import datetime, timedelta



POUPANCA=0.6248
SELIC=12.75
TOTAL_DIAS_NEGOCIACAO=252
COMPARAR_MERCADO="DIVO11.SA"

def aviso():
    print()
    print()
    print("----------------------------------------------------------------------------------------------------")
    print("                                            AVISO                                                   ")
    print("----------------------------------------------------------------------------------------------------")
    print("Este script funciona somente para ativos negociados na B3 (Bolsa de São Paulo).")
    print("Certifique-se de que os ativos que você deseja analisar estão listados na B3 antes de continuar")
    print("----------------------------------------------------------------------------------------------------")
    print()

Class Ativo():



def estimativa_retorno_anual(ticker):
    hoje = datetime.today().date()
    inicio_ano = datetime(hoje.year, 1, 1).date()
    data = yf.download(ticker, start=inicio_ano, end=hoje, progress=False)['Adj Close'].dropna()
    if not data.empty:
        preco_inicial = data.iloc[0]
        preco_final = data.iloc[-1]
        # Calcular o número de dias de negociação até agora no ano
        dias_negociacao = len(data)
        # Calcular a taxa de retorno diária média até agora no ano
        taxa_retorno_diaria_media = ((preco_final / preco_inicial) ** (1/dias_negociacao)) - 1
        # Assumir que a taxa de retorno diária média continuará pelo resto do ano
        # Calcular o número total de dias de negociação em um ano (aproximadamente 252 dias)
        total_dias_negociacao = TOTAL_DIAS_NEGOCIACAO
        # Calcular o retorno anual estimado
        retorno_anual_estimado = ((1 + taxa_retorno_diaria_media) ** total_dias_negociacao) - 1
        return retorno_anual_estimado * 100  # converter para porcentagem
    else:
        print(f"Dados históricos não disponíveis para {ticker}")
        return None

def retorno_ano(ticker):
    hoje = datetime.today().date()
    inicio_ano = datetime(hoje.year, 1, 1).date()
    data = yf.download(ticker, start=inicio_ano, end=hoje, progress=False)['Adj Close'].dropna()
    if not data.empty:
        preco_inicial = data.iloc[0]
        preco_final = data.iloc[-1]
        retorno_percentual = ((preco_final - preco_inicial) / preco_inicial) * 100
        return retorno_percentual
    else:
        print(f"Dados históricos não disponíveis para {ticker}")
        return None

def ticker_info(ticker):
    return yf.Ticker(ticker)

def get_bid(ticker_info):
    if 'bid' in ticker_info.info and ticker_info.info['bid'] is not None:
        return ticker_info.info['bid']
    return None

def get_ask(ticker_info):
    if 'ask' in ticker_info.info and ticker_info.info['ask'] is not None:
        return ticker_info.info['ask']
    return None

def get_price(ticker_info):
    if 'currentPrice' in ticker_info.info and ticker_info.info['currentPrice'] is not None:
        return ticker_info.info['currentPrice']
    return None

def get_last_dividend(ticker_info):
    if 'lastDividendValue' in ticker_info.info and ticker_info.info['lastDividendValue'] is not None:
        return ticker_info.info['lastDividendValue']
    return None


def preco_teto_adaptado(ticker_info, taxa_retorno_esperada):
    # Verificar se 'previousClose' está presente no dicionário info
    if 'previousClose' in ticker_info.info and ticker_info.info['previousClose'] is not None:
        preco_fechamento = ticker_info.info['previousClose']
        margem_seguranca = 0.02
        taxa = ((100 - (100/(SELIC*0.85))) /100) - margem_seguranca
        preco_teto = preco_fechamento * (taxa + taxa_retorno_esperada)

        return preco_teto

    return None


def preco_teto_dividendo(ticker_info, taxa_retorno_esperada):
    # Verificar se 'previousClose' está presente no dicionário info
    if get_last_dividend(ticker_info) is not None:
        margem_seguranca = taxa_retorno_esperada * 0.80
        preco_teto = (get_last_dividend(ticker_info)
                      * (100/(SELIC)/margem_seguranca))
        return preco_teto

    return None





# Função para calcular o retorno esperado através do CAPM
def retorno_esperado_capm(ticker, mercado_ticker=COMPARAR_MERCADO):
    data = yf.download([ticker, mercado_ticker],
                       start=cinco_anos_atras(), progress=False)['Adj Close'].dropna()
    log_returns = np.log(data / data.shift(1))
    ativo_livre_risco = (POUPANCA/100) * 12 # Poupança
    premio_risco = SELIC/100 # Selic
    cov_mercado = log_returns.cov() * TOTAL_DIAS_NEGOCIACAO
    cov_com_mercado = cov_mercado.iloc[0, 1]
    var_mercado = log_returns[mercado_ticker].var() * TOTAL_DIAS_NEGOCIACAO
    beta = cov_com_mercado / var_mercado
    capm = ativo_livre_risco + beta * premio_risco
    return capm

# Função para calcular a volatilidade (risco) de cada ativo
def risco_ativo(ticker):
    data = yf.download(ticker, start=cinco_anos_atras(), progress=False)['Adj Close'].dropna()
    log_returns = np.log(data / data.shift(1))
    volatilidade = log_returns.std() * np.sqrt(TOTAL_DIAS_NEGOCIACAO)
    return volatilidade

def output(tickers):
# Usando as funções para calcular os valores desejados para todos os ativos
    for ticker in tickers:
        ticker_information=ticker_info(ticker)
        capm = retorno_esperado_capm(ticker)
        risco = risco_ativo(ticker)
        ticker_price_teto = preco_teto_adaptado(ticker_information, capm)
        teto_dividendo = preco_teto_dividendo(ticker_information, capm)
        retorno_percentual = retorno_ano(ticker)
        retorno_anual_estimado = estimativa_retorno_anual(ticker)

        table = PrettyTable()
        table.title = ticker
        table.field_names = ["Descrição", "Valor"]
        table.align["Descrição"] = "l"  # Alinhamento à esquerda
        table.align["Valor"] = "r"  # Alinhamento à direita
        table.add_row(["Retorno Anual Esperado para o risco ", f"{capm*100:.2f}%"])
        table.add_row(["Retorno Anual Estimado", f"{retorno_anual_estimado:.2f}%" if retorno_anual_estimado is not None else "N/A"])
        table.add_row(["Retorno no Ano", f"{retorno_percentual:.2f}%" if retorno_percentual is not None else "N/A"])
        table.add_row(["Performance", f"BOA" if retorno_anual_estimado >= capm else "RUIM"])
        table.add_row(["Risco (Volatilidade)", f"{risco*100:.2f}%"])
        table.add_row(["Preço Justo", f"R$ {ticker_price_teto:.2f}" if ticker_price_teto is not None else "N/A"])
        table.add_row(
            ["Preço Teto para dividendo", f"R$ {teto_dividendo:.2f}" if teto_dividendo is not None else "N/A"])
        table.add_row(["Preço Atual", f"R$ {get_price(ticker_information):.2f}" if get_price(ticker_information) is not None else "N/A"])
        table.add_row(["Venda", f"R$ {get_bid(ticker_information):.2f}" if get_bid(ticker_information) is not None else "N/A"])
        table.add_row(["Compra", f"R$ {get_ask(ticker_information):.2f}" if get_ask(ticker_information) is not None else "N/A"])
        table.add_row(["Preço Sugerido", f"R$ {get_ask(ticker_information)*0.995:.2f}" if get_ask(ticker_information) is not None else "N/A"])
        table.add_row(["Ultimo Dividendo", f"R$ {get_last_dividend(ticker_information):.2f}" if get_last_dividend(ticker_information) is not None else "N/A"])
        print(table)
        print()  # Linha em branco entre as tabelas

def main():
    aviso()
    output(tickers_usuario())

if __name__ == "__main__":
    main()
