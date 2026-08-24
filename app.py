import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from plotly.subplots import make_subplots


def load_data():
    df = pd.read_csv('covid.csv', sep=';')
    df['data'] = pd.to_datetime(df['data'])
    return df

df = load_data()

st.header('Exercício 2: Gráfico de Barras')
estado = 'SP' 


df_estado_filtro = df[(df['estado'] == estado) & (df['municipio'].isna())]
df_casos_semana = df_estado_filtro.groupby('semanaEpi')['casosNovos'].sum().reset_index()

st.subheader(f'Evolução Semanal de Casos Novos - Estado: {estado}')
st.bar_chart(data=df_casos_semana, x='semanaEpi', y='casosNovos')

# Escolhido por ser o marco innicial da pandemia nno Brasil

st.header('Exercício 3: Gráfico de Linha')

df_brasil = df[df['regiao'] == 'Brasil']
df_obitos_semana_br = df_brasil.groupby('semanaEpi')['obitosAcumulado'].max().reset_index()

st.subheader('Número de Mortes Acumuladas por Semana (Brasil)')
st.line_chart(data=df_obitos_semana_br, x='semanaEpi', y='obitosAcumulado')

# Como os óbitos acumulados são uma soma contínua, essa curva só pode crescer ou estabilizar. Quando a curva tem uma inclina muito, indica um surto e quando a curva começa a fazer uma curva para baixo, significa q o numero de mortes se estabilizou


st.header('Exercício 4: Gráfico de Área')
st.subheader("Evolução de Casos Acumulados (SP, MG, RJ)")

df_comp = df[(df['municipio'].isna()) & (df['codmun'].isna()) & (df['estado'].isin(['SP', 'MG', 'RJ']))]

df_area = df_comp.pivot(index='data', columns='estado', values='casosAcumulado')
st.area_chart(df_area)

st.header('Exercício 5')

df_sp_cidades = df[(df['estado'] == 'SP') & (df['municipio'].notna())]
df_focos = df_sp_cidades.groupby('municipio')['casosAcumulado'].max().reset_index()

coordenadas_sp = {
    'São Paulo': [-23.5505, -46.6333],
    'Campinas': [-22.9099, -47.0626],
    'São José do Rio Preto': [-20.8197, -49.3794],
    'São José dos Campos': [-23.2237, -45.9009],
    'Ribeirão Preto': [-21.1704, -47.8103],
    'São Bernardo do Campo': [-23.6938, -46.5656],
    'Sorocaba': [-23.5015, -47.4581],
    'Santo André': [-23.6590, -46.5323],
    'Guarulhos': [-23.4628, -46.5333],
    'Piracicaba': [-22.7338, -47.6476]
}

def pegar_latitude(cidade):
    return coordenadas_sp.get(cidade, [None, None])[0]

def pegar_longitude(cidade):
    return coordenadas_sp.get(cidade, [None, None])[1]

df_focos['latitude'] = df_focos['municipio'].apply(pegar_latitude)
df_focos['longitude'] = df_focos['municipio'].apply(pegar_longitude)
df_mapa = df_focos.dropna(subset=['latitude', 'longitude'])

# 8. Visualização com proporção de Focos
st.map(
    data=df_mapa, 
    latitude='latitude', 
    longitude='longitude', 
    size='casosAcumulado', 
    color='#FF0000'        
)

st.header('Exercício 6')

semana_recente = df['semanaEpi'].max()
df_estados = df[(df['estado'].notna()) & (df['municipio'].isna()) & (df['codmun'].isna())]
df_ultima_semana = df_estados[df_estados['semanaEpi'] == semana_recente].groupby('estado')[['casosNovos', 'obitosNovos']].sum().reset_index()

fig, ax1 = plt.subplots(figsize=(12, 5))

x = range(len(df_ultima_semana))
bar_width = 0.4

color = 'tab:blue'
ax1.set_xlabel('Estado (UF)')
ax1.set_ylabel('Casos Novos', color=color)
ax1.bar([i - bar_width/2 for i in x], df_ultima_semana['casosNovos'], width=bar_width, color=color, label='Casos Novos')
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(x, df_ultima_semana['estado'], rotation=45)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Óbitos Novos', color=color)
ax2.bar([i + bar_width/2 for i in x], df_ultima_semana['obitosNovos'], width=bar_width, color=color, label='Óbitos Novos')
ax2.tick_params(axis='y', labelcolor=color)

plt.title(f'Comparação: Casos Novos vs Óbitos Novos por Estado (Semana Epidemiológica {semana_recente})')
fig.tight_layout()

st.pyplot(fig)

# Dá pra ver uma diferença gigante de escala: os casos novos ficam na casa dos milhares, enquanto as mortes ficam nas dezenas ou centenas. Isso mostra a taxa de letalidade da doença, que é de uns 2% a 3%. Se algum estado tiver uma barra de mortes muito alta comparada aos casos, significa que a situação nos hospitais tava bem feia lá ou que tavam testando pouco.

st.header('Exercício 7')

df_estados = df[(df['estado'].notna()) & (df['municipio'].isna()) & (df['codmun'].isna())]
df_reg_semana = df_estados.groupby(['regiao', 'semanaEpi'])['casosNovos'].sum().reset_index()

df_3_regioes = df_reg_semana[df_reg_semana['regiao'].isin(['Norte', 'Nordeste', 'Sudeste'])]

fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=df_3_regioes, x='regiao', y='casosNovos', palette='Set2', ax=ax)

ax.set_title('Distribuição Semanal de Casos Novos por Região')
ax.set_xlabel('Região')
ax.set_ylabel('Casos Novos por Semana')

st.pyplot(fig)

# O gráfico mostra que o Sudeste foi a região que mais variou e que teve os maiores picos de casos por semana. O Nordeste ficou no meio do caminho, com os números mais estáveis, e o Norte teve os menores números absolutos porque tem bem menos gente morando lá.

st.header('Exercício 8')

df_estados = df[(df['estado'].notna()) & (df['municipio'].isna()) & (df['codmun'].isna())]
df_sudeste = df_estados[df_estados['regiao'] == 'Sudeste'].groupby('semanaEpi')['casosNovos'].sum().reset_index()

chart = alt.Chart(df_sudeste).mark_area(
    color='teal',
    opacity=0.6,
    line={'color': 'darkteal'}
).encode(
    x=alt.X('semanaEpi:O', title='Semana Epidemiológica'),
    y=alt.Y('casosNovos:Q', title='Casos Novos Registrados'),
    tooltip=['semanaEpi', 'casosNovos']
).properties(
    title='Evolução Semanal de Casos Novos - Região Sudeste',
    width=650,
    height=350
)

st.altair_chart(chart, use_container_width=True)

# Escolhi o Sudeste por ser a região mais populosa. O gráfico de área mostra que o contágio disparou no começo de 2021, batendo um pico absurdo de mais de 200 mil casos numa semana só , e depois deu uma estagnada num valor ainda alto.

st.header('Exercício 9')

df_sp = df[(df['estado'] == 'SP') & (df['municipio'].isna()) & (df['codmun'].isna())]

cols = ['casosNovos', 'obitosNovos', 'casosAcumulado', 'obitosAcumulado']
corr_matrix = df_sp[cols].corr().reset_index().melt(id_vars='index')
corr_matrix.columns = ['Variavel_1', 'Variavel_2', 'Correlacao']

heatmap = alt.Chart(corr_matrix).mark_rect().encode(
    x=alt.X('Variavel_1:N', title=None),
    y=alt.Y('Variavel_2:N', title=None),
    color=alt.Color('Correlacao:Q', scale=alt.Scale(scheme='viridis')),
    tooltip=['Variavel_1', 'Variavel_2', alt.Tooltip('Correlacao:Q', format='.2f')]
).properties(
    title='Matriz de Correlação - Variáveis COVID-19 (SP)',
    width=400,
    height=400
)

st.altair_chart(heatmap, use_container_width=False)

# O mapa de calor mostra uma correlação super forte (acima de 0,80) entre casos novos e mortes. Na prática, isso prova que quando os casos subiam numa semana, já dava pra saber que ia aumentar o número de mortes umas semanas depois.

st.header('Exercício 10')

df_estados = df[(df['estado'].notna()) & (df['municipio'].isna()) & (df['codmun'].isna())]
max_data = df_estados['data'].max()
df_reg_max = df_estados[df_estados['data'] == max_data].groupby('regiao')['casosAcumulado'].sum().reset_index()

fig = px.pie(
    df_reg_max, 
    values='casosAcumulado', 
    names='regiao',
    title='Distribuição Percentual dos Casos Acumulados por Região',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig, use_container_width=True)

# O gráfico de pizza deixa bem claro que o Sudeste ficou com a maior fatia de casos do país (uns 38%), seguido pelo Nordeste (~24%) e Sul (~19%). O Centro-Oeste (~10%) e o Norte (~9%) ficaram com as menores fatias, mostrando que o total de doentes acompanhou o tamanho da população de cada lugar.

st.header('Exercício 11')

df_estados = df[(df['estado'].notna()) & (df['municipio'].isna()) & (df['codmun'].isna())]
df_reg = df_estados.groupby(['regiao', 'semanaEpi'])[['casosNovos', 'obitosNovos']].sum().reset_index()

df_nordeste = df_reg[df_reg['regiao'] == 'Nordeste']
df_sul = df_reg[df_reg['regiao'] == 'Sul']

fig = make_subplots(rows=1, cols=2, subplot_titles=('Região Nordeste', 'Região Sul'))

fig.add_trace(
    go.Bar(x=df_nordeste['semanaEpi'], y=df_nordeste['casosNovos'], name='Casos (Nordeste)', marker_color='orange'),
    row=1, col=1
)
fig.add_trace(
    go.Bar(x=df_nordeste['semanaEpi'], y=df_nordeste['obitosNovos'], name='Óbitos (Nordeste)', marker_color='red'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=df_sul['semanaEpi'], y=df_sul['casosNovos'], name='Casos (Sul)', marker_color='blue'),
    row=1, col=2
)
fig.add_trace(
    go.Bar(x=df_sul['semanaEpi'], y=df_sul['obitosNovos'], name='Óbitos (Sul)', marker_color='darkred'),
    row=1, col=2
)

fig.update_layout(title_text="Evolução Semanal: Nordeste vs Sul", barmode='group')
st.plotly_chart(fig, use_container_width=True)

# Olhando os dois gráficos lado a lado, dá pra ver que a pandemia não rolou no mesmo ritmo em todo lugar. O Sul teve uma onda super concentrada e pesada logo no começo do ano (março e abril), enquanto no Nordeste a contaminação e as mortes foram acontecendo de forma mais espalhada ao longo dos meses.

st.header('Exercício 12')

df_sp_mun = df[(df['estado'] == 'SP') & (df['municipio'].notna())].copy()
df_resumo = df_sp_mun.groupby('municipio').agg({
    'casosAcumulado': 'max',
    'populacaoTCU2019': 'max'
}).reset_index()

df_resumo['taxa_incidencia'] = (df_resumo['casosAcumulado'] / df_resumo['populacaoTCU2019']) * 1000

coordenadas = {
    'São Paulo': [-23.5505, -46.6333],
    'Campinas': [-22.9099, -47.0626],
    'São José do Rio Preto': [-20.8197, -49.3794],
    'Ribeirão Preto': [-21.1704, -47.8103],
    'Santos': [-23.9618, -46.3322]
}

df_resumo['lat'] = df_resumo['municipio'].map(lambda x: coordenadas.get(x, [None, None])[0])
df_resumo['lon'] = df_resumo['municipio'].map(lambda x: coordenadas.get(x, [None, None])[1])
df_mapa = df_resumo.dropna(subset=['lat', 'lon'])

layer = pdk.Layer(
    'ColumnLayer',
    data=df_mapa,
    get_position='[lon, lat]',
    get_elevation='taxa_incidencia',
    elevation_scale=500,
    radius=3000,
    get_fill_color='[255, 100, 0, 200]',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=-23.55,
    longitude=-46.63,
    zoom=7,
    pitch=45
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Esse mapa em 3D mostra que quanto mais gente junta na cidade, mais rápido o vírus se espalha por causa das aglomerações. Mas quando a gente calcula a taxa por mil habitantes, dá pra ver que várias cidades menores do interior tiveram uma situação proporcionalmente tão grave quanto a capital.