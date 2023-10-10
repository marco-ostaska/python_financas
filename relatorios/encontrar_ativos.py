# Importando as bibliotecas necessárias
import numpy as np
from scipy.stats import norm
from tqdm import tqdm
import previsaoAtivos

def calcula_projetado(ativo,dias):
    forecast= ativo.forecast(dias,10)
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
    if i == dias_previsoes[-2]:
        print("Ativos com melhores projeção até final do ano")
    elif i == dias_previsoes[-1]:
        print("Ativos com melhores projeção para 5 anos")
    else:
        print(f"melhores projeção para os proximos {i} dias")
    print("------------------------------------------------------------------")


def ler_tickers(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        # Lê as linhas, retira os espaços em branco e adiciona à lista
        tickers = [linha.strip() for linha in arquivo.readlines()]
    return tickers


def gerar_lista_ativos(ativos,anos_historico):
    lista_ativos = []
    pbar = tqdm(ativos)

    for a in pbar:
        pbar.set_description(f"Coletando dados para: {a}")
        lista_ativos.append(previsaoAtivos.Ativo(a, anos_historico))

    return lista_ativos


def get_sel(selecao):
    if selecao == 1:
        return "ibov.txt"
    if selecao == 2:
        return "idiv.txt"
    if selecao == 3:
        return "small.txt"
    if selecao == 4:
        return "ifix.txt"
    if selecao == 6:
        return "custom.txt"


def opt():
    selecao=0
    while selecao<1 or selecao>6:
        print("Selecione uma das opções")
        print("1 - IBOV")
        print("2 - IDIV")
        print("3 - Small Caps")
        print("4 - Ifix")
        print("5 - Todas")
        print("6 - Custom (preencher o arquivo custom.txt)")
        selecao=int(input("opçao desejada: "))

    return get_sel(selecao)



def main():
    ativos = ler_tickers(opt())
    anos_historico = 5
    dias_previsoes = [7, 30, 90, previsaoAtivos.dias_ate_final_ano(), 5*365]

    lista_ativos = gerar_lista_ativos(ativos,anos_historico)

    for dp in dias_previsoes:
        print_cabecalho(dp, dias_previsoes)

        retornos = [
            (ativo.ticker, calcula_projetado(ativo, dp))
            for ativo in lista_ativos
        ]
        print_melhores(retornos)

# Iniciando o programa
if __name__ == "__main__":
    main()


