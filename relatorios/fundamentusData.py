import pandas as pd
import numpy as np
import requests


class Ativos:

    headers = {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
               'Accept': 'text/html, text/plain, text/css, text/sgml, */*;q=0.01',
               'Accept-Encoding': 'gzip, deflate',
               }

    def __init__(self) -> None:
        self.data = self.download_info()

    def download_info(self):
        url = f"https://www.fundamentus.com.br/detalhes.php?papel={self.ticker}"
        content = requests.get(url, headers=self.headers)
        return pd.read_html(content.text, decimal=",", thousands='.')


class Acao(Ativos):

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        super().__init__()

    @property
    def cotacao(self):
        return float(self.data[0][3][0])

    @property
    def lpa(self):
        return float(self.data[2][5][1])

    @property
    def vpa(self):
        return float(self.data[2][5][2])

    @property
    def div_yield(self):
        return float(fix_pct(self.data[2][3][8]))

    @property
    def pl(self):
        return round(float(self.data[2][3][1]), 2)

    @property
    def pvp(self):
        return round(float(self.data[2][3][2]), 2)

    @property
    def graham(self):
        return round(np.sqrt(22.5 * self.lpa * self.vpa), 2)

    def bazin(self, juros):
        dpa = (self.div_yield/100) * self.cotacao
        margem = 100/juros
        return round(dpa*margem, 2)


class FII(Ativos):

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        super().__init__()

    @property
    def cotacao(self):
        return float(self.data[0][3][0])

    @property
    def lpa(self):
        return float(self.data[2][5][1])

    @property
    def vpa(self):
        return float(self.data[2][5][2])

    @property
    def div_yield(self):
        return float(fix_pct(self.data[2][3][2]))

    @property
    def pl(self):
        return round(float(self.data[2][3][1]), 2)

    @property
    def pvp(self):
        return round(float(self.data[2][3][3]), 2)

    @property
    def graham(self):
        return round(float(self.data[2][5][3]), 2)

    def bazin(self, juros):
        dpa = (self.div_yield/100) * self.cotacao
        margem = 100/juros
        return round(dpa*margem, 2)


def fix_pct(text):
    return text.replace("%", "").replace(",", ".")


def main():
    acao = Acao("ggbr4")
    print("Ticker :", acao.ticker)
    print("Cotacao:", acao.cotacao)
    print("PL     :", acao.pl)
    print("PVP    :", acao.pvp)
    print("DY     :", acao.div_yield)
    print("LPA    :", acao.lpa)
    print("VPA    :", acao.vpa)
    print("Graham :", acao.graham)
    print("Bazin  :", acao.bazin(7))

    print()
    print()

    acao = FII("hsml11")
    print("Ticker :", acao.ticker)
    print("Cotacao:", acao.cotacao)
    # print("PL     :", acao.pl)
    print("PVP    :", acao.pvp)
    print("DY     :", acao.div_yield)
    # print("LPA    :", acao.lpa)
    # print("VPA    :", acao.vpa)
    print("Graham :", acao.graham)
    print("Bazin  :", acao.bazin(7))


if __name__ == "__main__":
    main()
