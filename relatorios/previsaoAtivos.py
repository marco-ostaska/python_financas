#Importando as bibliotecas necessárias
import numpy as np
import yfinance as yf
from scipy.stats import norm
from datetime import datetime

class Ativo:
    def __init__(self, ticker, anos_historico):
        self.ticker = ticker
        self.anos_historico = anos_historico
        self.historico = self.download_data()
        self._log_returns = self.log_returns()

    def add_SA(self, ticker):
        return [t.upper() + ".SA" for t in ticker]

    def download_data(self):
        ticker = self.add_SA([self.ticker])
        today = datetime.now()
        start = f"{today.year-self.anos_historico}-{today.month}-{today.day}"
        return yf.download(ticker, start=start, progress=False)['Adj Close']

    def log_returns(self):
        return np.log(1+self.historico.pct_change(1)).dropna()

    @property
    def log_returns_mean(self):
        return self._log_returns.mean()

    @property
    def log_returns_var(self):
        return self._log_returns.var()

    @property
    def log_returns_std(self):
        return self._log_returns.std()

    @property
    def drift(self):
        return self.log_returns_mean - (0.5 * self.log_returns_var)

    def forecast(self, dias_futuro, qtd_analises):
        np.random.seed(100)
        daily_future_returns = (np.exp(self.drift + self.log_returns_std * norm.ppf(np.random.rand(dias_futuro, qtd_analises))))
        price_list = np.zeros_like(daily_future_returns)
        price_list[0] = self.historico.iloc[-1]

        for t in range(1, dias_futuro):
            price_list[t] = price_list[t - 1] * daily_future_returns[t]

        return price_list


def dias_ate_final_ano():
    # Data atual
    hoje = datetime.now()

    # Último dia do ano atual
    ultimo_dia_do_ano = datetime(hoje.year, 12, 31)

    # Cálculo da diferença
    dias_restantes = (ultimo_dia_do_ano - hoje).days

    return dias_restantes if dias_restantes > 0 else 1
