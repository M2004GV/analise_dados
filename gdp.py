import pandas as pd
import numpy as np

#funcao para ler arquivos .csv
df_gdp = pd.read_csv('GDP.csv', decimal='.')

#aply e funcao inline com a logica de split para pegar apenas o ano(DD/MM/YYYY)[-1]
df_gdp['Year'] = df_gdp['Year'].apply(lambda x: int(x.split('/')[-1]))


#verificar os nomes das colunas(podem conter espacos e dificultar na leitura)
# print(df_gdp.columns)

#split, só que agora para tirar o espaço em branco 
#e replace pois os valores acima dos milhares são representados por vírgula no sistema americano
#troca a virgula por ''
df_gdp['gdp_pp'] = df_gdp[' GDP_pp '].apply(lambda x: float(x.split()[0].replace(',','')))


#deleta uma series coluna do DataFrame
del df_gdp[' GDP_pp ']

#agora o dataFrame(tabela) contém na coluna 'Year' apenas o valor do ano
#e a parte do gdp.py possui os valores float

#Agora com os dados tratados pode se retirar perguntas do gdp per capita de 1901 a 2011

#qual o primeiro valor registrado de cada país?
#usar o groupby e o método min

df_gdp.groupby('Country')['Year'].min()

#ver os anos mínimos e a quantidade de anos correspondente
df_gdp.groupby('Country')['Year'].min().value_counts()

#verificar as informações (pais e ano) de determinado ano
df_gdp.groupby('Country')['Year'].min()[df_gdp.groupby('Country')['Year'].min() == 1991]


#primeiro ano coletado
df_gdp_start = df_gdp[df_gdp['Year'] == 1901]

#ultimo ano antes da virado de século
df_gdp[df_gdp['Year'] < 2000].max()
df_gdp_end = df_gdp[df_gdp['Year'] == 1996]

# Organizado por crescimento das regiões do menor para o maior gdp_pp
((df_gdp_end.groupby('Region')['gdp_pp'].mean()/df_gdp_start.groupby('Region')['gdp_pp'].mean() - 1) * 100).sort_values()


#criar um array(arange) de valores igualmente espaçados em um intervalo específico
arr_year = np.arange(df_gdp['Year'].min(), df_gdp['Year'].max())
df_all_years = pd.DataFrame(arr_year, columns=['Year'])
df_all_years.index = df_all_years['Year']

#verificar os anos ausentes na continuidade
df_years_off = ~df_all_years['Year'].isin(df_gdp['Year'])
df_years_off = df_all_years.loc[df_years_off].index

df_gdp = df_gdp.sort_values(['Country', 'Year'])

df_gdp['delta_gdp'] = df_gdp['gdp_pp'] - df_gdp['gdp_pp'].shift(1)
df_gdp['delta_year'] = df_gdp['Year'] - df_gdp['Year'].shift(1)
df_gdp['gdp_year'] = (df_gdp['delta_gdp']/df_gdp['delta_year']).shift(-1)


df_gdp['next_year'] = df_gdp['Year'].shift(-1)
del df_gdp['delta_gdp'], df_gdp['delta_year']

df_new_data = pd.DataFrame()

#iterar e ordenar
for idx, row in df_gdp.iterrows():
    if row['Year'] == 2011:
        continue
    years_to_add = df_years_off[(df_years_off < row['next_year']) & (df_years_off > row['Year'])]
    break


