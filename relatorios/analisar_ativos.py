import numpy as np
import pandas as pd
import yfinance as yf
from prettytable import PrettyTable
from datetime import datetime, timedelta

class BCB:
    SELIC = {"nome": "SELIC", "codigo": 11}
    IPCA = {"nome": "IPCA", "codigo": 10844}

    def __init__(self):
        self.selic_history = self.parse_bcb()

    def parse_bcb(codigo_serie, indice):
        hoje = datetime.now()
        data_inicio = f"{hoje.day}/{hoje.month}/{hoje.year-ANOS_PASSADOS}"

    def parse_bcb(self):
        return BCB.SELIC["nome"]

class Indices():
    TOTAL_DIAS_NEGOCIACAO=252
    BENCHMARK="^BVSP"


    def __init__(self, anos_historico):
        self.anos_historico = anos_historico
        self.ipca_media = round(self.parse_bcb(10844).mean().values[0]*12,2)
        self.selic_media = round(self.parse_bcb(11).mean().values[0]*22*12,2)


    def parse_bcb(self, codigo):
        hoje = datetime.now()
        data_inicio = f"{hoje.day}/{hoje.month}/{hoje.year-self.anos_historico}"
        data_final = f"{hoje.day}/{hoje.month}/{hoje.year}"

        URL = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=csv&dataInicial={data_inicio}&dataFinal={data_final}"
        df = pd.read_csv(URL, sep=";")

        # Convertendo a coluna "data" para o formato datetime
        # Aqui, ajustei o formato da data para corresponder ao formato fornecido: %d/%m/%Y
        df.rename(columns={"data": "date"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"], format='%d/%m/%Y')
        df.set_index('date', inplace=True)
        df["valor"] = df["valor"].str.replace(',', '.').astype(float)
        df.rename(columns={"valor": "indice"}, inplace=True)
        return df
    
    def taxa_livre_risco(self):
        return self.ipca_media if self.ipca_media >  self.selic_media else  self.selic_media 



def main():

    indices=Indices(5)

    print(indices.taxa_livre_risco())


if __name__ == "__main__":
    main()

