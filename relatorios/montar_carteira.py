from calendar import c
import bancoCentral
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime

from retorno_carteira import ANO_DIAS_UTEIS

class Carteira:
    ANO_DIAS_UTEIS = 252
    retorno = []
    peso_ativos = []
    volatilidade = []
    volatilidade_ajustada = []
    sharpe_ratio = []
    sortino_ratio = []

    def __init__(self, data, selic):
        self.data = data
        self.numero_ativos = len(data.columns)
        self.selic = selic/100

    def retorno_anual(self):
        retorno_diario = self.data.pct_change()
        return retorno_diario.mean() * self.ANO_DIAS_UTEIS

    def cov_anual(self):
        retorno_diario = self.data.pct_change()
        cov_diaria = retorno_diario.cov()
        return cov_diaria * self.ANO_DIAS_UTEIS

    def semi_cov_anual(self):
        retorno_diario = self.data.pct_change()
        retorno_diario = retorno_diario[retorno_diario < 0].dropna()
        cov_diaria_neg = retorno_diario.cov()
        return  cov_diaria_neg * self.ANO_DIAS_UTEIS

    def get_pesos(self, numero_ativos):
        pesos = np.random.random(numero_ativos)
        pesos /= np.sum(pesos)
        return pesos

    def retorno_portfolio(self, pesos):
        return np.dot(pesos, self.retorno_anual())


    def volatilidade_portfolio(self,pesos):
        return np.sqrt(np.dot(pesos.T, np.dot(self.cov_anual(), pesos)))


    def volatilidade_ajustada_portifolio(self, pesos):
        return  np.sqrt(
            np.dot(pesos.T, np.dot(self.semi_cov_anual(), pesos)))

    def calcular_pesos_carteira(self, pesos):
        taxa_livre_risco = self.selic
        retorno_portfolio = self.retorno_portfolio(pesos)
        volatilidade_portfolio = self.volatilidade_portfolio(pesos)
        volatilidade_ajustada = self.volatilidade_ajustada_portifolio(pesos)
        sharpe = (retorno_portfolio - taxa_livre_risco) / \
            volatilidade_portfolio
        sortino = (retorno_portfolio - taxa_livre_risco) / \
            volatilidade_ajustada

        self.retorno.append(retorno_portfolio)
        self.volatilidade.append(volatilidade_portfolio)
        self.volatilidade_ajustada.append(volatilidade_ajustada)

        self.sharpe_ratio.append(sharpe)
        self.sortino_ratio.append(sortino)

        self.peso_ativos.append(pesos)

    def monte_carlo(self, numero_simulacoes):
        np.random.seed(101)
        for _ in range(numero_simulacoes):
            pesos = self.get_pesos(self.numero_ativos)
            self.calcular_pesos_carteira(pesos)

    def df_carteira(self):

        carteira = {'Retorno': self.retorno,
                    'Volatilidade': self.volatilidade,
                    'Sharpe Ratio': self.sharpe_ratio,
                    'Vol Ajustada': self.volatilidade_ajustada,
                'Sortino Ratio': self.sortino_ratio}

        for contar,a in enumerate(self.data):
            carteira[a+' Peso'] = [Peso[contar] for Peso in self.peso_ativos]

        # vamos transformar nosso dicionário em um dataframe
        df = pd.DataFrame(carteira)

        # vamos nomear as colunas do novo dataframe
        colunas = ['Retorno', 'Volatilidade', 'Sharpe Ratio', 'Vol Ajustada', 'Sortino Ratio'] + [a+' Peso' for a in self.data]
        df = df[colunas]

        return df

    def minima_variancia(self):
        df = self.df_carteira()
        valor = df['Volatilidade'].min()
        return df.loc[df['Volatilidade'] == valor]

    def maior_sharpe_ratio(self):
        df = self.df_carteira()
        valor = df['Sortino Ratio'].max()
        return df.loc[df['Sortino Ratio'] == valor]

    def maior_sortino_ratio(self):
        df = self.df_carteira()
        valor = df['Sharpe Ratio'].max()
        return df.loc[df['Sharpe Ratio'] == valor]

    def minima_variancia_ajustada(self):
        df = self.df_carteira()
        valor = df['Vol Ajustada'].min()
        return df.loc[df['Vol Ajustada'] == valor]

    def maior_retorno(self):
        df = self.df_carteira()
        valor = df['Retorno'].max()
        return df.loc[df['Retorno'] == valor]

    def round100(self, valor):
        return round(valor*100, 2)

def get_tickers():
    tickers = input("Entre os tickers separados por virgula: ")
    tickers = [t.upper().strip() for t in tickers.split(",")]
    tickers=(sorted(tickers))
    return [f"{t}.SA" for t in tickers]

def download_data(tickers, anos_hist):
    hoje = datetime.now()
    start_date=f"{hoje.year-anos_hist}-{datetime.now().month}-{datetime.now().day}"
    return yf.download(tickers, start=start_date)['Adj Close']

def main():
    tickers=get_tickers()
    anos_hist=5
    data=download_data(tickers,anos_hist)
    selic=bancoCentral.SELIC(anos_hist).media_anual()

    carteira = Carteira(data,selic)
    carteira.monte_carlo(10000)

    print("Essa é a carteira de Mínima Variância:",
          '\n', carteira.minima_variancia().T)
    print()
    print("Essa é a carteira com maior Sharpe Ratio:", '\n', carteira.maior_sharpe_ratio().T)
    print()
    print("Essa é a carteira com maior Sortino Ratio:",
          '\n', carteira.maior_sortino_ratio().T)
    print()
    print("Essa é a carteira com menor Risco Ajustado:", '\n',  carteira.minima_variancia_ajustada().T)
    print()
    print("Maior Retorno:", '\n', carteira.maior_retorno().T)

if __name__ == "__main__":
    main()
