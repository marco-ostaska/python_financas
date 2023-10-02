import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from prettytable import PrettyTable
from datetime import datetime, timedelta
from tqdm import tqdm

# Definindo os tickers
# tickers = ["BCRI11", "BDIF11", "BTAL11", "BTRA11", "FGAA11", "GALG11", "HGRU11", "HSAF11", "HSLG11", "HSML11", "IFRA11",
#            "KNCA11", "KNCR11", "KNRI11", "MAXR11", "PATL11", "RURA11", "RZAG11", "VGIA11", "VISC11", "XPCA11", "XPID11",
#            "XPML11", "XPIN11"]


tickers = input("Entre os tickers separados por virgula: ")
tickers = [t.upper().strip() for t in tickers.split(",")]
print(tickers)
tickers=(sorted(tickers))
tickers = [t + ".SA" for t in tickers]
DATA_INICIO='2018-01-01'

POUPANCA=0.6248
SELIC=12.75
ANO_DIAS_UTEIS=252


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
        total_dias_negociacao = ANO_DIAS_UTEIS
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
    
def preco_teto_adaptado(ticker, taxa_retorno_esperada):
    stock_info = yf.Ticker(ticker)
    # Verificar se 'previousClose' está presente no dicionário info
    if 'previousClose' in stock_info.info and stock_info.info['previousClose'] is not None:
        preco_fechamento = stock_info.info['previousClose']
    else:
        return None
    
    margem_seguranca = 0.05
    taxa = ((100 - (100/(SELIC*0.85))) /100) - margem_seguranca
    preco_teto = preco_fechamento * (taxa + taxa_retorno_esperada)

    return preco_teto



# Função para calcular o retorno esperado através do CAPM
def retorno_esperado_capm(ticker, mercado_ticker="DIVO11.SA"):
    data = yf.download([ticker, mercado_ticker],
                       start=DATA_INICIO, progress=False)['Adj Close'].dropna()
    log_returns = np.log(data / data.shift(1))
    ativo_livre_risco = (POUPANCA/100) * 12 # Poupança
    premio_risco = SELIC/100 # Selic
    cov_mercado = log_returns.cov() * ANO_DIAS_UTEIS
    cov_com_mercado = cov_mercado.iloc[0, 1]
    var_mercado = log_returns[mercado_ticker].var() * ANO_DIAS_UTEIS
    beta = cov_com_mercado / var_mercado
    capm = ativo_livre_risco + beta * premio_risco
    return capm

# Função para calcular a volatilidade (risco) de cada ativo
def risco_ativo(ticker):
    data = yf.download(ticker, start="2018-01-01", progress=False)['Adj Close'].dropna()
    log_returns = np.log(data / data.shift(1))
    volatilidade = log_returns.std() * np.sqrt(ANO_DIAS_UTEIS)
    return volatilidade


# Usando as funções para calcular os valores desejados para todos os ativos
# for ticker in tickers:
#     capm = retorno_esperado_capm(ticker)
#     risco = risco_ativo(ticker)
#     ticker_price_teto = preco_teto_adaptado(ticker, capm)
#     retorno_percentual = retorno_ano(ticker)
#     retorno_anual_estimado = estimativa_retorno_anual(ticker)

    
#     table = PrettyTable()
#     table.title = ticker
#     table.field_names = ["Descrição", "Valor"]
#     table.align["Descrição"] = "l"  # Alinhamento à esquerda
#     table.align["Valor"] = "r"  # Alinhamento à direita
#     table.add_row(["Retorno Anual Esperado para valer correr o risco ", f"{capm*100:.2f}%"])
#     table.add_row(["Risco (Volatilidade)", f"{risco*100:.2f}%"])
#     table.add_row(["Preço Teto", f"R$ {ticker_price_teto:.2f}" if ticker_price_teto is not None else "Não disponível"])
#     table.add_row(["Retorno no Ano", f"{retorno_percentual:.2f}%" if retorno_percentual is not None else "Não disponível"])
#     table.add_row(["Retorno Anual Estimado", f"{retorno_anual_estimado:.2f}%" if retorno_anual_estimado is not None else "Não disponível"])
#     table.add_row(["Performance", f"BOM" if retorno_anual_estimado >= capm else "RUIM"])
 
#     print(table)
#     print()  # Linha em branco entre as tabelas




# Baixando os dados carteira
ativos = yf.download(tickers, start="2018-01-01", progress=False)['Adj Close'].dropna()
retorno_diario = ativos.pct_change()
retorno_anual = retorno_diario.mean() * ANO_DIAS_UTEIS

# Cálculo da covariância diária e anual
cov_diaria = retorno_diario.cov()
cov_anual = cov_diaria * ANO_DIAS_UTEIS

# Simulação de carteiras
retorno_carteira = []
peso_acoes = []
volatilidade_carteira = []
sharpe_ratio = []
numero_acoes = len(tickers)
numero_carteiras = 500000
np.random.seed(101)

print("Verificando melhor distribuição de carteiras")
for cada_carteira in tqdm(range(numero_carteiras)):
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
def calcular_retorno_carteira_recomendada(df):
    retornos = []
    for ticker in tickers:
        retorno = retorno_ano(ticker)
        peso = df[ticker + " Peso"].iloc[0]
        retornos.append(retorno * peso)
    return sum(retornos)

def print_portfolio(df, title):
    retorno_atual = calcular_retorno_carteira_recomendada(df)
    
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
    
    
    print(table)

    table = PrettyTable()
    table.title = "Alocaçao"
    table.field_names = ["Ativo", "Alocação"]

    weights = df.drop(columns=['Retorno', 'Volatilidade', 'Sharpe Ratio']).iloc[0] * 100

    for ticker, weight in zip(tickers, weights):
        table.add_row([ticker.replace('.SA', ''), f"{weight:.2f}%"])

    # # fazendo isso pra conseguir ordenar as tabelas, sou meio burro entao depois penso em algo melhor
    # # Pegando os nomes das colunas
    # columns = table.field_names

    # # Pegando os valores
    # values = [list(row) for row in table._rows]

    # # Criando o dataframe
    # dfaux = pd.DataFrame(values, columns=columns)

    # # Convertendo a coluna Alocação para float
    # dfaux['Alocação'] = dfaux['Alocação'].str.rstrip('%').astype('float') / 100.0
    # dfaux = dfaux.sort_values(by="Alocação", ascending=False)

    # # Limpar as linhas do objeto table para inserir os valores atualizados de dfaux
    # table.clear_rows()

    # # Adicionar os valores de dfaux à tabela
    # for index, row in dfaux.iterrows():
    #     table.add_row([row['Ativo'], f"{row['Alocação']*100:.2f}%"])
    
    print(table)
    
    print()
    print()



print()
print()
print("Carteiras recomendadas")
print("-----------------------------------------------------")
print()


print_portfolio(carteira_min_variancia, "Carteira com menor risco:")
print_portfolio(carteira_sharpe, "Carteira com melhor risco/retorno")