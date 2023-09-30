# Montagem de Carteira de Investimentos com Python

O script `montar_carteira.py` é um utilitário para análise e montagem de carteiras de ativos financeiros com base em dados históricos de preços. Ele fornece uma análise de retorno, risco e outras métricas financeiras relevantes, juntamente com a simulação de diferentes alocações de carteira para otimizar o perfil de risco/retorno.

## Instalação
É recomendável criar um ambiente virtual (venv) para instalar as dependências e executar este script. Para fazer isso, siga os passos abaixo:

1. Crie um ambiente virtual:

```bash
python -m venv myenv
``````

2. Ative o ambiente virtual:

```bash
# WIndows
.\myenv\Scripts\activate

# Linux
source myenv/bin/activate
```

3. Com o ambiente virtual ativado, instale as dependências necessárias com o comando:
```bash
pip install -r requirements.txt
```

## Uso
1. Certifique-se de que o ambiente virtual está ativado.
2. Execute o script montar_carteira.py com o comando:

```bash
python montar_carteira.py
```



## Exemplo Ouput:

```
$ python montar_carteira.py 

+-----------------------------------+
|              VALE3.SA             |
+------------------------+----------+
| Descrição              |    Valor |
+------------------------+----------+
| Retorno Esperado       |   17.83% |
| Risco (Volatilidade)   |   39.64% |
| Preço Teto             | R$ 79.31 |
| Retorno no Ano         |  -20.42% |
| Retorno Anual Estimado |  -26.37% |
+------------------------+----------+

+-----------------------------------+
|             TAEE11.SA             |
+------------------------+----------+
| Descrição              |    Valor |
+------------------------+----------+
| Retorno Esperado       |   13.87% |
| Risco (Volatilidade)   |   20.67% |
| Preço Teto             | R$ 39.38 |
| Retorno no Ano         |    7.51% |
| Retorno Anual Estimado |   10.25% |
+------------------------+----------+

+-----------------------------------+
|             KLBN11.SA             |
+------------------------+----------+
| Descrição              |    Valor |
+------------------------+----------+
| Retorno Esperado       |   13.05% |
| Risco (Volatilidade)   |   30.62% |
| Preço Teto             | R$ 26.79 |
| Retorno no Ano         |   24.14% |
| Retorno Anual Estimado |   33.84% |
+------------------------+----------+

+----------------------------------+
|             MGLU3.SA             |
+------------------------+---------+
| Descrição              |   Valor |
+------------------------+---------+
| Retorno Esperado       |  24.74% |
| Risco (Volatilidade)   |  62.34% |
| Preço Teto             | R$ 2.63 |
| Retorno no Ano         | -18.15% |
| Retorno Anual Estimado | -23.54% |
+------------------------+---------+



Carteiras recomendadas
-----------------------------------------------------

+----------------------------+
| Carteira como menor risto: |
+-----------------+----------+
| Descrição       |    Valor |
+-----------------+----------+
| Retorno         |   19.29% |
| Volatilidade    |   18.25% |
| Sharpe Ratio    |     1.06 |
+-----------------+----------+
+----------------------------------+
|             Alocaçao             |
+--------------------+-------------+
|       Ativo        | Porcentagem |
+--------------------+-------------+
| TAEE11.SA Alocação |    67.59%   |
| KLBN11.SA Alocação |    22.00%   |
| VALE3.SA Alocação  |    10.18%   |
| MGLU3.SA Alocação  |    0.23%    |
+--------------------+-------------+


+------------------------------------+
| Carteira como melhor risco/retorno |
+----------------------+-------------+
| Descrição            |       Valor |
+----------------------+-------------+
| Retorno              |      20.25% |
| Volatilidade         |      18.74% |
| Sharpe Ratio         |        1.08 |
+----------------------+-------------+
+----------------------------------+
|             Alocaçao             |
+--------------------+-------------+
|       Ativo        | Porcentagem |
+--------------------+-------------+
| TAEE11.SA Alocação |    73.23%   |
| VALE3.SA Alocação  |    16.02%   |
| KLBN11.SA Alocação |    10.19%   |
| MGLU3.SA Alocação  |    0.56%    |
+--------------------+-------------+

```