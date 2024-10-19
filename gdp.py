import pandas as pd


#funcao para ler arquivos .csv
df_gdp = pd.read_csv('GDP.csv', decimal='.')

#aply e funcao inline com a logica de split para pegar apenas o ano(DD/MM/YYYY)[-1]
df_gdp['Year'] = df_gdp['Year'].apply(lambda x: int(x.split('/')[-1]))


#verificar os nomes das colunas(podem conter espacos e dificultar na leitura)
# print(df_gdp.columns)

#split de só que agora para tirar o espaço em branco 
#e replace pois o valores acima dos milhares são representados por vigula no states
#troca a virgula por
df_gdp['gdp_pp'] = df_gdp[' GDP_pp '].apply(lambda x: float(x.split()[0].replace(',','')))

del df_gdp[' GDP_pp ']

#agora o dataFrame(tabela) contém na coluna year apenas o valor do ano
#e a parte do gdp.py possui os valores float

#Agora com os dados tratados pode se retirar perguntas do gdp per capita de 1901 a 2011

#qual o primeiro valor registrado de cada país?
#usar o groupby e o método min

df_gdp.groupby('Country')['Year'].min()

#ver os anos mínimos e a quantidade de anos correspondente
df_gdp.groupby('Country')['Year'].min().value_counts()

#verificar as informações (pais e ano) de determinado ano
df_gdp.groupby('Country')['Year'].min()[df_gdp.groupby('Country')['Year'].min() == 1991]


df_gdp[df_gdp['Year'] < 2000].max()

#primeiro ano coletado
df_gdp_start = df_gdp[df_gdp['Year'] == 1901]

#ultimo ano antes da virado de século
df_gdp_end = df_gdp[df_gdp['Year'] == 1996]

# Organizado por crescimento das regiões do menor para o maior gdp_pp
((df_gdp_end.groupby('Region')['gdp_pp'].mean()/df_gdp_start.groupby('Region')['gdp_pp'].mean() - 1) * 100).sort_values()

