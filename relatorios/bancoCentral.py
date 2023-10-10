import pandas as pd
from datetime import datetime

class Indices:
    def __init__(self, anos_hist):
        self.anos_hist = anos_hist
        self.df = None

    def get_url(self, codigo_serie):
        hoje = datetime.now()
        data_inicio = f"{hoje.day}/{hoje.month}/{hoje.year-self.anos_hist}"
        data_final = f"{hoje.day}/{hoje.month}/{hoje.year}"
        URL = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=csv&dataInicial={data_inicio}&dataFinal={data_final}"
        return URL

    def parse(self, codigo_serie, indice):
        if self.df is None:
            URL = self.get_url(codigo_serie)
            df = pd.read_csv(URL, sep=";")
            df.rename(columns={"data": "date"}, inplace=True)
            df["date"] = pd.to_datetime(df["date"], format='%d/%m/%Y')
            df.set_index('date', inplace=True)
            df["valor"] = df["valor"].str.replace(',', '.').astype(float)
            df.rename(columns={"valor": indice}, inplace=True)
            self.df = df
        return self.df

class SELIC(Indices):
    def __init__(self, anos_hist):
        super().__init__(anos_hist)
        self.codigo_serie = 11
        self.indice = "Selic"

    def media_anual(self):
        dias_uteis = 22
        media = self.parse(self.codigo_serie, self.indice).mean().dropna().values[0] * dias_uteis * 12
        return round(media, 2)

class IPCA(Indices):
    def __init__(self, anos_hist):
        super().__init__(anos_hist)
        self.codigo_serie = 10844
        self.indice = "IPCA"

    def media_anual(self):
        media = self.parse(self.codigo_serie, self.indice).mean().dropna().values[0] * 12
        return round(media, 2)

    def media_ganho_real(self):
        return self.media_anual() + 2

def main():
    selic = SELIC(5)
    ipca = IPCA(5)
    print(selic.media_anual())
    print(ipca.media_ganho_real())

if __name__ == "__main__":
    main()
