#Importando as bibliotecas necessárias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm
from tqdm import tqdm
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

    if dias_restantes > 0:
        return dias_restantes
    
    return 1


def print_cabecalho(ativo):
    print("-----------------------------------------------------------------------------")
    print(f"{ativo.ticker.upper()} - Preço fechamento: R$ {round(ativo.historico[-1],2)}")
    print("-----------------------------------------------------------------------------")

def print_cabecalho_previsoes(i, dias_previsoes):
    if i == dias_previsoes[-2]:
        print(f"Previsão até final do ano")
    elif i== dias_previsoes[-1]:
        print(f"Previsão em cinco anos")
    else:
        print(f"Previsão para os proximos {i} dias")




# Função para exibir a previsão
def print_forecast(ativo):
    dias_previsoes=[7,30,90,dias_ate_final_ano(), 5*365]
    print_cabecalho(ativo)

    for dp in dias_previsoes:
        print_cabecalho_previsoes(dp, dias_previsoes)
        
        forecast=ativo.forecast(dp, 10)
        maximo = round(forecast.max(),2)
        maximo_pct = round(((maximo - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        projetado = round(forecast.mean(),2)
        projetado_pct = round(((projetado - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        minimo= round(forecast.min(),2)
        minimo_pct = round(((minimo - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

        print(f"Preço Otimista     : R$ {maximo} ({maximo_pct}%)")
        print(f"Preço Projetado    : R$ {projetado} ({projetado_pct}%)")
        print(f"Preço Pessimista   : R$ {minimo} ({minimo_pct}%)")
        print()


def gerar_lista_ativos(ativos,anos_historico):
    lista_ativos = []
    pbar = tqdm(ativos)

    for a in pbar:
        pbar.set_description(f"Coletando dados para: {a}")
        lista_ativos.append(Ativo(a, anos_historico))
    
    return lista_ativos

# Função principal
def main():
    ativos = input("Entre os ativos separado por virgula: ")
    ativos = [a.strip() for  a in ativos.split(",")]
    anos_historico=5
    lista_ativos = gerar_lista_ativos(ativos,anos_historico)
    
    for ativo in lista_ativos:
        print_forecast(ativo)

    

# Iniciando o programa
if __name__ == "__main__":
    main()
