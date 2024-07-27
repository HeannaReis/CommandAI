import investpy
import fundamentus
import pandas as pd
import matplotlib.pyplot as plt

# Obter lista de ações do Brasil
acoes_brasil = investpy.stocks.get_stocks(country='brazil')

# Exibir as primeiras linhas do DataFrame
print(acoes_brasil.head())

df = fundamentus.get_resultado()
