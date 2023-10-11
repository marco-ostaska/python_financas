from matplotlib.pyplot import tick_params
import bancoCentral
import fundamentusData
from tabulate import tabulate

def taxa_livre_risco():
    selic = bancoCentral.SELIC(5)
    ipca = bancoCentral.IPCA(5)

    if ipca.media_ganho_real() > selic.media_anual():
        return ipca.media_ganho_real()

    return selic.media_anual()


def get_tickers():
    tickers = input("Entre os tickers separados por virgula: ")
    return [t.upper().strip() for t in tickers.split(",")]


def get_tipo():
    tipo=None
    while tipo not in ["1","2"]:
        print("--------------------------------------------")
        print("1 - Ações")
        print("2 - FII")
        print("--------------------------------------------")
        tipo = input("Selecione uma opção:")

    return tipo

def process_acoes(ticker, free_risk):
    ativo = fundamentusData.Acao(ticker)
    df = [
        ["Cotação",f"R$ {ativo.cotacao}"],
        ["P/L", f"{ativo.pl}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Ghaham", f"R$ {ativo.graham}"],
        ["Bazin", f"R$ {ativo.bazin(free_risk)}"]

        ]

    print()
    print(tabulate(df, headers=[ativo.ticker, "Valores"], tablefmt='simple'))

    return {
        'ticker': ativo.ticker,
        'bazin': ativo.bazin(free_risk)
    }


def process_fii(ticker, free_risk):
    ativo = fundamentusData.FII(ticker)
    df = [
        ["Cotação", f"R$ {ativo.cotacao}"],
        ["P/VP", f"{ativo.pvp}"],
        ["DY", f"{ativo.div_yield}%"],
        ["Ghaham", f"R$ {ativo.graham}"],
        ["Bazin", f"R$ {ativo.bazin(free_risk)}"]

    ]
    print()
    print(tabulate(df, headers=[ativo.ticker, "Valores"], tablefmt='simple'))

    return {
        'ticker': ativo.ticker,
        'bazin': ativo.bazin(free_risk)
    }




def main():
    tipo=get_tipo()
    tickers = get_tickers()
    risk_free = taxa_livre_risco()

    results = []
    for t in tickers:
        if tipo == "1":
            results.append(process_acoes(t, risk_free))
        else:
            results.append(process_fii(t, risk_free))
  # Ordena os resultados pelo desconto Bazin
    sorted_results = sorted(results, key=lambda x: x['bazin'])

    # Agora imprime os ativos ordenados
    for result in sorted_results:
        print(f"Ticker: {result['ticker']} - Bazin: R$ {result['bazin']}")










if __name__ == "__main__":
    main()
