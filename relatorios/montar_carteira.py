import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Definindo os tickers
tickers = ["BCRI11", "BDIF11", "BTAL11", "BTRA11", "FGAA11", "GALG11", "HGRU11", "HSAF11", "HSLG11", "HSML11", "IFRA11",
           "KNCA11", "KNCR11", "KNRI11", "MAXR11", "PATL11", "RURA11", "RZAG11", "VGIA11", "VISC11", "XPCA11", "XPID11",
           "XPML11", "XPIN11", "MGLU3"]
tickers = [t + ".SA" for t in tickers]


def preco_teto_graham(ticker):
    stock_info = yf.Ticker(ticker)
    eps = stock_info.info['trailingEps']  # Lucro por ação dos últimos 12 meses

    # Aqui, precisamos de uma estimativa da taxa de crescimento dos lucros (g).
    # Neste exemplo, estou usando um valor fictício de 0.05 (ou 5%).
    # Você deve substituir isso por um cálculo ou valor mais preciso.
    g = 0.05

    V = eps * (8.5 + 2 * (g * 100))
    return V


# Função para calcular o retorno esperado através do CAPM



def retorno_esperado_capm(ticker, mercado_ticker="DIVO11.SA"):
    data = yf.download([ticker, mercado_ticker],
                       start="2018-01-01", progress=False)['Adj Close'].dropna()
    log_returns = np.log(data / data.shift(1))
    ativo_livre_risco = 0.005 * 12
    premio_risco = 0.1275
    cov_mercado = log_returns.cov() * 250
    cov_com_mercado = cov_mercado.iloc[0, 1]
    var_mercado = log_returns[mercado_ticker].var() * 250
    beta = cov_com_mercado / var_mercado
    capm = ativo_livre_risco + beta * premio_risco
    return capm

# Função para calcular a volatilidade (risco) de cada ativo


def risco_ativo(ticker):
    data = yf.download(ticker, start="2018-01-01", progress=False)['Adj Close'].dropna()
    log_returns = np.log(data / data.shift(1))
    volatilidade = log_returns.std() * np.sqrt(250)
    return volatilidade


# Usando as funções para calcular os valores desejados para todos os ativos
for ticker in tickers:
    capm = retorno_esperado_capm(ticker)
    risco = risco_ativo(ticker)
    print(f"Retorno Esperado para {ticker}: {capm*100:.2f}%")
    print(f"Risco (Volatilidade) de {ticker}: {risco*100:.2f}%")
    ticker_price_teto = preco_teto_graham(ticker)
    print(f"Preço Teto (Graham) para {ticker}: R$ {ticker_price_teto:.2f}")

    print("-----------------------------------------------------")

# Baixando os dados
ativos = yf.download(tickers, start="2018-01-01")['Adj Close'].dropna()
retorno_diario = ativos.pct_change()
retorno_anual = retorno_diario.mean() * 250

# Cálculo da covariância diária e anual
cov_diaria = retorno_diario.cov()
cov_anual = cov_diaria * 250

# Simulação de carteiras
retorno_carteira = []
peso_acoes = []
volatilidade_carteira = []
sharpe_ratio = []
numero_acoes = len(tickers)
numero_carteiras = 100000
np.random.seed(101)

for cada_carteira in range(numero_carteiras):
    peso = np.random.random(numero_acoes)
    peso /= np.sum(peso)
    retorno = np.dot(peso, retorno_anual)
    volatilidade = np.sqrt(np.dot(peso.T, np.dot(cov_anual, peso)))
    sharpe = retorno / volatilidade
    sharpe_ratio.append(sharpe)
    retorno_carteira.append(retorno)
    volatilidade_carteira.append(volatilidade)
    peso_acoes.append(peso)

carteira = {'Retorno': retorno_carteira,
            'Volatilidade': volatilidade_carteira, 'Sharpe Ratio': sharpe_ratio}
for contar, acao in enumerate(ativos.columns.to_list()):
    carteira[acao+' Peso'] = [Peso[contar] for Peso in peso_acoes]

df = pd.DataFrame(carteira)
colunas = ['Retorno', 'Volatilidade', 'Sharpe Ratio'] + \
    [acao+' Peso' for acao in ativos.columns.to_list()]
df = df[colunas]

menor_volatilidade = df['Volatilidade'].min()
maior_sharpe = df['Sharpe Ratio'].max()
carteira_sharpe = df.loc[df['Sharpe Ratio'] == maior_sharpe]
carteira_min_variancia = df.loc[df['Volatilidade'] == menor_volatilidade]

# Função para imprimir os detalhes das carteiras


def print_portfolio(df, title):
    print(title)
    print(f"Retorno: {df['Retorno'].iloc[0]*100:.2f}%")
    print(f"Volatilidade: {df['Volatilidade'].iloc[0]*100:.2f}%")
    print(f"Sharpe Ratio: {df['Sharpe Ratio'].iloc[0]:.2f}")
    sorted_weights = df.drop(columns=[
                             'Retorno', 'Volatilidade', 'Sharpe Ratio']).iloc[0].sort_values(ascending=False) * 100
    for index, value in sorted_weights.items():
        print(f"{index.replace(' Peso','')}: {value:.2f}%")
    print()


print_portfolio(carteira_min_variancia,
                "Essa é a carteira de Mínima Variância:")
print_portfolio(carteira_sharpe, "Essa é a carteira com maior Sharpe Ratio:")
