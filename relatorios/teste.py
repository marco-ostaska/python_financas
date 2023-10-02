from prettytable import PrettyTable

# Exemplo da sua tabela
table = PrettyTable()
table.title = "Alocação"
table.field_names = ["Ativo", "Alocação"]
table.add_row(["HSML11", "0.01%"])
table.add_row(["IFRA11", "87.79%"])
table.add_row(["BDIF11", "12.20%"])

# Convertendo a tabela PrettyTable para um DataFrame do pandas
import pandas as pd

# Pegando os nomes das colunas
columns = table.field_names

# Pegando os valores
values = [list(row) for row in table._rows]

# Criando o dataframe
df = pd.DataFrame(values, columns=columns)

# Convertendo a coluna Alocação para float
df['Alocação'] = df['Alocação'].str.rstrip('%').astype('float') / 100.0

print(df)
