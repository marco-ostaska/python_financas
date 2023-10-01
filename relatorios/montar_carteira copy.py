import numpy as np
import pandas as pd
import yfinance as yf
from prettytable import PrettyTable
from datetime import datetime

class Constants:
    DATA_INICIO = '2018-01-01'
    POUPANCA = 0.6248
    SELIC = 12.75
    TOTAL_DIAS_NEGOCIACAO = 252
    MERCADO_TICKER = "DIVO11.SA"

class TickerInput:
    @staticmethod
    def get_tickers():
        tickers = input("Entre os tickers separados por virgula: ")
        tickers = [t.upper().strip() for t in tickers.split(",")]
        return [t + ".SA" for t in tickers]

class YahooFinanceService:
    @staticmethod
    def download_data(ticker, start, end=datetime.today().date()):
        return yf.download(ticker, start=start, end=end, progress=False)['Adj Close'].dropna()

    @staticmethod
    def get_stock_info(ticker):
        return yf.Ticker(ticker).info

class FinanceMetrics:
    @staticmethod
    def annual_return_estimate(ticker_data):
        if ticker_data.empty:
            return None

        preco_inicial = ticker_data.iloc[0]
        preco_final = ticker_data.iloc[-1]
        dias_negociacao = len(ticker_data)
        taxa_retorno_diaria_media = ((preco_final / preco_inicial) ** (1/dias_negociacao)) - 1
        retorno_anual_estimado = ((1 + taxa_retorno_diaria_media) ** Constants.TOTAL_DIAS_NEGOCIACAO) - 1

        return retorno_anual_estimado * 100

    @staticmethod
    def annual_return(ticker_data):
        if ticker_data.empty:
            return None

        preco_inicial = ticker_data.iloc[0]
        preco_final = ticker_data.iloc[-1]
        return ((preco_final - preco_inicial) / preco_inicial) * 100

    @staticmethod
    def expected_return_capm(ticker_data, mercado_data):
        log_returns = np.log(ticker_data / ticker_data.shift(1))
        ativo_livre_risco = (Constants.POUPANCA/100) * 12
        premio_risco = Constants.SELIC/100
        cov_mercado = log_returns.cov() * Constants.TOTAL_DIAS_NEGOCIACAO
        cov_com_mercado = cov_mercado.iloc[0, 1]
        var_mercado = mercado_data.var() * Constants.TOTAL_DIAS_NEGOCIACAO
        beta = cov_com_mercado / var_mercado

        return ativo_livre_risco + beta * premio_risco

    @staticmethod
    def asset_risk(ticker_data):
        log_returns = np.log(ticker_data / ticker_data.shift(1))
        return log_returns.std() * np.sqrt(Constants.TOTAL_DIAS_NEGOCIACAO)

class DataVisualizer:
    @staticmethod
    def print_metrics(ticker, metrics):
        table = PrettyTable()
        table.title = ticker
        table.field_names = ["Descrição", "Valor"]
        table.align["Descrição"] = "l"
        table.align["Valor"] = "r"
        for key, value in metrics.items():
            table.add_row([key, value])

        print(table)
        print()

class PortfolioAnalyzer:
    def __init__(self, tickers):
        self.tickers = tickers

    def analyze(self):
        mercado_data = YahooFinanceService.download_data(Constants.MERCADO_TICKER, Constants.DATA_INICIO)
        for ticker in self.tickers:
            ticker_data = YahooFinanceService.download_data(ticker, Constants.DATA_INICIO)

            metrics = {
                "Retorno Anual Estimado": f"{FinanceMetrics.annual_return_estimate(ticker_data):.2f}%",
                "Retorno no Ano": f"{FinanceMetrics.annual_return(ticker_data):.2f}%",
                "Retorno Esperado CAPM": f"{FinanceMetrics.expected_return_capm(ticker_data, mercado_data):.2f}%",
                "Risco do Ativo": f"{FinanceMetrics.asset_risk(ticker_data):.2f}%",
            }

            DataVisualizer.print_metrics(ticker, metrics)

if __name__ == "__main__":
    tickers = TickerInput.get_tickers()
    analyzer = PortfolioAnalyzer(tickers)
    analyzer.analyze()
