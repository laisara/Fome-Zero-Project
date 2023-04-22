#Libraries
from PIL import Image
import plotly.express as px

#Bibliotecas necessárias
import pandas as pd
import inflection
import streamlit as st


#Configuração básica da página
st.set_page_config(page_title='Countries', layout="wide")

# ======================================
# Funções
# ======================================


#Gráfico Barras: Média Preço para Dois x Países
def average_cost_for_two_countries(df):
    
    #selecionar colunas
    cols = ['average_cost_for_two', 'country_name']

    #agrupar linhas por data
    #.sort_values('restaurant_id', ascending=False)
    dfaux = round(df.loc[:, cols].groupby(['country_name']).mean().sort_values('average_cost_for_two', ascending=False).reset_index(), 2)
    
    #desenhar o gráfico de barra
    fig = px.bar(dfaux, x='country_name', y='average_cost_for_two', text='average_cost_for_two', title='Média de Preço de Um Prato para Duas Pessoaas por País')
    
    fig = fig.update_layout(xaxis_title='Países',
                            yaxis_title='Preço do prato para duas Pessoas')
    
    fig = fig.update_traces(textfont=dict(size=14), hovertemplate='País: %{x} <br>Preço do prato para duas Pessoas: %{y:.2f}')


    return fig


#Gráfico Barras: Média Avaliações x Países
def mean_votes_countries(df):
    
    #selecionar colunas
    cols = ['votes', 'country_name']

    #agrupar linhas por data
    #.sort_values('restaurant_id', ascending=False)
    dfaux = round(df.loc[:, cols].groupby(['country_name']).mean().sort_values('votes', ascending=False).reset_index(), 2)
    
    #desenhar o gráfico de barra
    fig = px.bar(dfaux, x='country_name', y='votes', text='votes', title='Média de Avaliações Feitas por País')
    
    fig = fig.update_layout(xaxis_title='Países',
                            yaxis_title='Quantidade de Avaliações')
    
    fig = fig.update_traces(textfont=dict(size=14), hovertemplate='País: %{x} <br>Quantidade de Avaliações: %{y}')


    return fig

#Gráfico Barras: Qtd Cidades x Países
def cities_countries(df):
    
    #selecionar colunas
    cols =  ['city', 'country_name']

    #agrupar linhas por data
    #.sort_values('restaurant_id', ascending=False)
    dfaux = df.loc[:, cols].groupby(['country_name']).nunique().sort_values('city', ascending=False).reset_index()
    
    #desenhar o gráfico de barra
    fig = px.bar(dfaux, x='country_name', y='city', text='city', title='Quantidade de Cidades Registrados por País')
    
    fig = fig.update_layout(xaxis_title='Países',
                            yaxis_title='Quantidade de Cidades')
    
    fig = fig.update_traces(textfont=dict(size=14), hovertemplate='País: %{x} <br>Quantidade de de Cidades: %{y}')


    return fig


#Gráfico Barras: Qtd Restaurantes x Países
def restaurant_countries(df):
    #selecionar colunas
    cols =  ['restaurant_id', 'country_name']

    #agrupar linhas por data
    #.sort_values('restaurant_id', ascending=False)
    dfaux = df.loc[:, cols].groupby(['country_name']).count().sort_values('restaurant_id', ascending=False).reset_index()
    
    #desenhar o gráfico de barra
    fig = px.bar(dfaux, x='country_name', y='restaurant_id', text='restaurant_id', title='Quantidade de Restaurantes Registrados por País')
    
    fig = fig.update_layout(xaxis_title='Países',
                            yaxis_title='Quantidade de Restaurantes')
    
    fig = fig.update_traces(textfont=dict(size=14), hovertemplate='País: %{x} <br>Quantidade de Restaurantes: %{y}')

    return fig


#Nomeando/Preenchendo os códigos de países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]


#Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

    
#Nomeando/Preenchendo os códigos de países
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]


#Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new

    return df
  

#Limpeza e Tratamento do Dataframe
def clean_code(df):
    #Excluindo a coluna 'Switch to order menu' por não ter informaçãoes relevantes e todos os valores serem identicos
    df = df.drop('Switch to order menu', axis=1)

    #Identificando se há dados duplicados no dataframe
    df = df.drop_duplicates()

    #Excluir as linhas com a tipo de culinária vazia
    df = df.loc[df['Cuisines'].notnull()]

    #Criando nova coluna com nomes dos países
    df["country_name"] = df.loc[:, "Country Code"].apply(lambda x: country_name(x))

    #Criando nova coluna com o tipo de categoria de comida
    df["price_type"] = df.loc[:, "Price range"].apply(lambda x: create_price_tye(x))

    #Criando nova coluna com os nomes das cores por classificaçã0 (rating color)
    df["color_name"] = df.loc[:, "Rating color"].apply(lambda x: color_name(x))

    #Renomear nomes das colunas
    df = rename_columns(df)

    #Categorizar, inicialmente, todos os restaurantes somente por um tipo de culinária.
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(', ')[0])
    
        
    #Removendo Culinárias que não estão categorizadas como país/tipo culinária
    lin = (df['cuisines'] != 'Mineira' )
    df = df.loc[lin, :]

    lin = (df['cuisines'] != 'Drinks Only') 
    df = df.loc[lin, :]
    
    #resetar index
    df = df.reset_index()

    return df



#---------------------------------------------- Inicialização do Script ----------------------------------------------
# ======================================
# Limpeza do dataframe
# ======================================

#Import dataset
df_raw = pd.read_csv('dataset/zomato.csv')

# Fazendo uma cópia do DataFrame Lido
df = clean_code(df_raw)


#Countries

# ======================================
# Barra Lateral Streamlit
# ======================================

# Exibindo a logo na sidebar
image = Image.open("images/logofomezero.png")
st.sidebar.image( image, width=160)


# Exibição do filtro para escolha dos países
st.sidebar.markdown('## Filtros')

countries_options = st.sidebar.multiselect(
    '_Escolha os países que deseja visualizar os restaurantes_',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    
    default=['Brazil', 'Australia', 'Canada', 'England', 'Qatar', 'South Africa'] )


st.sidebar.markdown("""___""")
st.sidebar.markdown("###### Desenvolvido por Lais Araujo")


# ======================================
# Filtros Streamlit
# ======================================


#Filtros de transito para toda página
linhas_selecionadas = df['country_name'].isin( countries_options )
df = df.loc[linhas_selecionadas, :]

# ======================================
# Layout Streamlit
# ======================================


#Título da página Countries
st.markdown('# 🌎 Visão Países')
        

with st.container():
        
    fig = restaurant_countries(df)
    st.plotly_chart(fig, use_container_width=True) 
    
            
with st.container():
    
    fig = cities_countries(df)
    st.plotly_chart(fig, use_container_width=True) 
    
            
with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        fig = mean_votes_countries(df)
        st.plotly_chart(fig, use_container_width=True) 
        
    
    with col2:
        
        fig = average_cost_for_two_countries(df)
        st.plotly_chart(fig, use_container_width=True) 