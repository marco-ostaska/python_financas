import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from prettytable import PrettyTable
from datetime import datetime, timedelta
from tqdm import tqdm


# Constantes
POUPANCA=0.6248
SELIC=12.75
ANO_DIAS_UTEIS=252


def dados_usuario():
    tickers = input("Entre os tickers separados por virgula: ")
    tickers = [t.upper().strip() for t in tickers.split(",")]
    tickers = [t + ".SA" for t in tickers]

    # Solicitar os pesos dos ativos ao usuário
    pesos_str = input("Entre com os pesos dos ativos, separados por vírgula: ")
    alocacao = np.array([float(p.strip())/100 for p in pesos_str.split(",")])

    if len(alocacao) != len(tickers):
        print("Numero de % não bate com o numero de tickers")
        exit()
    return tickers, alocacao


def cinco_anos_atras():
    # Obtém a data atual
    data_atual = datetime.now()

    # Subtrai 5 anos da data atual
    data_inicio = data_atual - timedelta(days=365 * 5)

    # Formata a data de início como uma string no formato 'YYYY-MM-DD'
    return data_inicio.strftime('%Y-%m-%d')


def retorno_ano(ticker):
    hoje = datetime.today().date()
    inicio_ano = datetime(hoje.year, 1, 1).date()
    data = yf.download(ticker, start=inicio_ano, end=hoje,
                       progress=False)['Adj Close'].dropna()
    if not data.empty:
        preco_inicial = data.iloc[0]
        preco_final = data.iloc[-1]
        retorno_percentual = (
            (preco_final - preco_inicial) / preco_inicial) * 100
        return retorno_percentual
    else:
        print(f"Dados históricos não disponíveis para {ticker}")
        return None

def calcular_semivariancia(retorno_diario, peso):
    """Calcula a semivariância da carteira."""
    # Calcular o retorno diário da carteira
    retorno_port = np.dot(retorno_diario, peso)

    # Identificar os retornos negativos
    downside_return = retorno_port[retorno_port < 0]

    # Calcular a semivariância
    semivariancia = np.mean(downside_return**2)

    return semivariancia



def calcular_indices(ativos, peso):
    retorno_diario = ativos.pct_change()
    retorno_anual = retorno_diario.mean() * ANO_DIAS_UTEIS

    # Cálculo da covariância diária e anual
    cov_diaria = retorno_diario.cov()
    cov_anual = cov_diaria * ANO_DIAS_UTEIS

    retorno = np.dot(peso, retorno_anual)
    volatilidade = np.sqrt(np.dot(peso.T, np.dot(cov_anual, peso)))
    semivariancia = calcular_semivariancia(retorno_diario, peso)
    sharpe = retorno / volatilidade

    return retorno, volatilidade, semivariancia, sharpe



def montar_carteira(ativos, peso):
    retorno, volatilidade, semivariancia, sharpe = calcular_indices(ativos, peso)

    carteira = {
        'Retorno': [retorno],
        'Volatilidade': [volatilidade],
        'Semivariância': [semivariancia],
        'Sharpe Ratio': [sharpe]
    }
    for contar, acao in enumerate(ativos.columns.to_list()):
        carteira[acao+' Peso'] = [peso[contar]]

    df = pd.DataFrame(carteira)
    colunas = ['Retorno', 'Volatilidade', 'Semivariância', 'Sharpe Ratio'] + [acao+' Peso' for acao in ativos.columns.to_list()]
    df = df[colunas]

    return df


def calcular_retorno_carteira_recomendada(df, tickers):
    retornos = []
    for ticker in tickers:
        retorno = retorno_ano(ticker)
        peso = df[ticker + " Peso"].iloc[0]
        retornos.append(retorno * peso)
    return sum(retornos)

def print_portfolio(df, title, tickers):
    retorno_atual = calcular_retorno_carteira_recomendada(df, tickers)

    carteira_status = "Sharpe Ratio bom" if df['Sharpe Ratio'].iloc[0] > 0.5 else "Sharpe Ratio ruim"
    table = PrettyTable()
    table.title = title
    table.field_names = ["Descrição", "Valor"]
    table.align["Descrição"] = "l"  # Alinhamento à esquerda
    table.align["Valor"] = "r"  # Alinhamento à direita
    table.add_row(["Retorno Esperado", f"{df['Retorno'].iloc[0]*100:.2f}%"])
    table.add_row(["Retorno Atual", f"{retorno_atual:.2f}%"])
    table.add_row(["Status", f"{carteira_status}"])
    table.add_row(["Volatilidade (Risco )", f"{df['Volatilidade'].iloc[0]*100:.2f}%"])
    table.add_row(["Sharpe Ratio", f"{df['Sharpe Ratio'].iloc[0]:.2f}"])
    table.add_row(["Semivariância", f"{df['Semivariância'].iloc[0]*100:.2f}%"])


    print(table)

    table = PrettyTable()
    table.title = "Alocaçao"
    table.field_names = ["Ativo", "Alocação"]

    weights = df.drop(columns=['Retorno', 'Volatilidade', 'Sharpe Ratio']).iloc[0] * 100

    for ticker, weight in zip(tickers, weights):
        table.add_row([ticker.replace('.SA', ''), f"{weight:.2f}%"])

    # fazendo isso pra conseguir ordenar as tabelas, sou meio burro entao depois penso em algo melhor
    # Pegando os nomes das colunas
    columns = table.field_names

    # Pegando os valores
    values = [list(row) for row in table._rows]

    # Criando o dataframe
    dfaux = pd.DataFrame(values, columns=columns)

    # Convertendo a coluna Alocação para float
    dfaux['Alocação'] = dfaux['Alocação'].str.rstrip('%').astype('float') / 100.0
    dfaux = dfaux.sort_values(by="Alocação", ascending=False)

    # Limpar as linhas do objeto table para inserir os valores atualizados de dfaux
    table.clear_rows()

    # Adicionar os valores de dfaux à tabela
    for index, row in dfaux.iterrows():
        table.add_row([row['Ativo'], f"{row['Alocação']*100:.2f}%"])

    print(table)
    print()
    print()



print()
print()


def main():
    tickers, peso = dados_usuario()
    ativos = yf.download(tickers, start=cinco_anos_atras(),
                         progress=False)['Adj Close'].dropna()
    carteira = montar_carteira(ativos, peso)
    carteira_df = pd.DataFrame(carteira)
    print_portfolio(carteira_df, "Perfomance da Carteira", tickers)


if __name__ == "__main__":
    main()
