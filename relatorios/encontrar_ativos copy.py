# Importando as bibliotecas necessárias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm
from tqdm import tqdm
from datetime import datetime

# Classe para definir e analisar um Ativo financeiro
class Ativo:
    
    # Inicializador da classe
    def __init__(self, ticker, anos_historico):
        self.ticker = ticker
        self.anos_historico = anos_historico
        self.historico = self.download_data()
    
    # Método para adicionar '.SA' ao final do ticker
    def add_SA(self,ticker):
        return [t.upper() + ".SA" for t in ticker]
    
    # Método para fazer o download dos dados históricos
    def download_data(self):
        ticker=self.add_SA([self.ticker])
        today=datetime.now()
        start=f"{today.year-self.anos_historico}-{today.month}-{today.day}"
        return yf.download(ticker, start=start, progress=False)['Adj Close']
    
    # Método para calcular os retornos logarítmicos
    def log_returns(self):
        return np.log(1+self.historico.pct_change(1)).dropna()
    
    # Média dos retornos logarítmicos
    def log_returns_mean(self):
        return self.log_returns().mean()
    
    # Variância dos retornos logarítmicos
    def log_returns_var(self):
        return self.log_returns().var()
    
    # Desvio padrão dos retornos logarítmicos
    def log_returns_std(self):
        return self.log_returns().std()
    
    # Cálculo do drift
    def drift(self):
        return self.log_returns_mean()-(0.5*self.log_returns_var())
    
    # Previsão do preço do ativo nos próximos dias
    def forecast(self, dias_futuro, qtd_analises):
        np.random.seed(100)
        daily_future_returns = (np.exp(
            self.drift() + self.log_returns_std() * norm.ppf(np.random.rand(dias_futuro,qtd_analises))
            ))
        price_list=np.zeros_like(daily_future_returns)
        price_list[0] = self.historico.iloc[-1]

        for t in range(1,dias_futuro):
            price_list[t] = price_list[t -1]*daily_future_returns[t]
        
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

   
def calcula_projetado(ativo):
    forecast= ativo.forecast(30,10)
    projetado = round(forecast.mean(),2)
    projetado_pct = round(((projetado - ativo.historico[-1]) / ativo.historico[-1]) * 100, 2)

    return projetado_pct

def print_melhores(retornos):
    #Ordena a lista retornos baseado no retorno_anual_estimado (decrescente)
    retornos_ordenados = sorted(retornos, key=lambda x: x[1] if x[1] is not None else -np.inf, reverse=True)
    # Pega os 10 primeiros ou todos se tiver menos de 10
    top_10_retornos = retornos_ordenados[:10]

    for ticker, retorno in top_10_retornos:
        if retorno is not None:
            print(f"{ticker}: {retorno:.2f}%")

    print()

def print_cabecalho(i, dias_previsoes):
    print("------------------------------------------------------------------")
    if i == dias_previsoes[-1]:
        print(f"Ativos com melhores projeção até final do ano")
    else:
        print(f"melhores projeção para os proximos {i} dias")
    print("------------------------------------------------------------------")


def ler_tickers(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        # Lê as linhas, retira os espaços em branco e adiciona à lista
        tickers = [linha.strip() for linha in arquivo.readlines()]
    return tickers


# Função principal
def main():
    ativos = ler_tickers("tickers_bolsa")
    anos_historico=5

    retornos = []
    
    dias_previsoes=[7,30,90,dias_ate_final_ano()]
    for dp in dias_previsoes:
        retornos = []
        print_cabecalho(dp, dias_previsoes)
        pbar = tqdm(ativos)
        
        for a in pbar:
            pbar.set_description(f"Processando {a}")
            ativo=Ativo(a, anos_historico)
            retornos.append((ativo.ticker, calcula_projetado(ativo)))
        
        print_melhores(retornos)
        



    

# Iniciando o programa
if __name__ == "__main__":
    main()
