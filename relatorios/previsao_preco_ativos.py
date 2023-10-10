#Importando as bibliotecas necessárias
import numpy as np
import yfinance as yf
from scipy.stats import norm
from tqdm import tqdm
import previsaoAtivos


def print_cabecalho(ativo):
    print("-----------------------------------------------------------------------------")
    print(f"{ativo.ticker.upper()} - Preço fechamento: R$ {round(ativo.historico[-1],2)}")
    print("-----------------------------------------------------------------------------")

def print_cabecalho_previsoes(i, dias_previsoes):
    if i == dias_previsoes[-2]:
        print("Previsão até final do ano")
    elif i== dias_previsoes[-1]:
        print("Previsão em cinco anos")
    else:
        print(f"Previsão para os proximos {i} dias")


# Função para exibir a previsão
def print_forecast(ativo):
    dias_previsoes=[7,30,90,previsaoAtivos.dias_ate_final_ano(), 5*365]
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
        lista_ativos.append(previsaoAtivos.Ativo(a, anos_historico))

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
