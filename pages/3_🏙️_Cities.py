#Libraries
from PIL import Image
import plotly.express as px

#Bibliotecas necessárias
import pandas as pd
import inflection
import streamlit as st


#Configuração básica da página
st.set_page_config(page_title='Cities', layout="wide")

# ======================================
# Funções
# ======================================


#Top 10 cidades com mais Tipo de culinarias distintos na base de dados
def top_10_cities_types_cuisines(df):
    cols = ['cuisines', 'city', 'country_name']

    dfaux = df.loc[:, cols].groupby(['country_name', 'city']).nunique().sort_values(by=['cuisines', 'city'], ascending=[False, True]).reset_index()

    dfaux = dfaux.head(10)
    
    fig = px.bar(dfaux, x='city', y='cuisines', color='country_name', text='country_name', title='Top 10 Cidades com Mais Restaurantes com Tipos de Culinárias Distintos')
    
    fig = fig.update_layout(xaxis_title='Cidades',
                            yaxis_title='Quantidade de Restaurantes',
                            legend_title='País')
    
    fig = fig.update_traces(texttemplate='%{y}', hovertemplate='País: %{text} <br>Cidades: %{x} <br>Quantidade de Tipos Culináarias Únicas: %{y}')


    return fig


#Top 10 cidades com mais Restaurantes na base de dados
def top_10_cities_restaurant(df):
    cols = ['restaurant_id', 'city', 'country_name']

    dfaux = df.loc[:, cols].groupby(['country_name', 'city']).count().sort_values(by=['restaurant_id', 'city'], ascending=[False, True]).reset_index()

    dfaux = dfaux.head(10)
    
    fig = px.bar(dfaux, x='city', y='restaurant_id', color='country_name', text='country_name', title='Top 10 Cidades com Mais Restaurantes na Base de Dados')
    
    fig = fig.update_layout(xaxis_title='Cidades',
                            yaxis_title='Quantidade de Restaurantes',                            
                            legend_title='País')
    
    fig = fig.update_traces(texttemplate='%{y}', hovertemplate='País: %{text} <br>Cidades: %{x} <br>Quantidade de Restaurantes: %{y}')


    return fig



#Top 7 cidades com Restaurantes com média de avaliação abaixo de 2.5 -> menores avaliações
def top_7_cities_highest_rating(df):
    cols = ['aggregate_rating', 'restaurant_name', 'city', 'country_name']
    lins = (df['aggregate_rating'] <= 2.5)
    
    dfaux = df.loc[lins, :].groupby(['country_name','city']).agg({'restaurant_name': 'count'}).sort_values(by=['restaurant_name', 'city'], ascending=[False, True]).reset_index()

    dfaux = dfaux.head(7)
    
    fig = px.bar(dfaux, x='city', y='restaurant_name', color='country_name', text='country_name', title='Top 7 Cidades com Restaurantes com Média de Avaliação Abaixo de 2.5')
    
    
    fig = fig.update_layout(xaxis_title='Cidades',
                            yaxis_title='Quantidade de Restaurantes',
                            legend_title='País')
    
    fig = fig.update_traces(texttemplate='%{y}', hovertemplate='País: %{text} <br>Cidades: %{x} <br>Quantidade de Restaurantes: %{y}')

    return fig



#Top 7 cidades com Restaurantes com média de avaliação acima de 4 -> maiores avaliações
def top_7_cities_lowest_rating(df):
    cols = ['aggregate_rating', 'restaurant_name', 'city', 'country_name']
    lins = (df['aggregate_rating'] >= 4)
    
    dfaux = df.loc[lins, :].groupby(['country_name','city']).agg({'restaurant_name': 'count'}).sort_values(by=['restaurant_name', 'city'], ascending=[False, True]).reset_index()

    dfaux = dfaux.head(7)


    fig = px.bar(dfaux, x='city', y='restaurant_name', color='country_name', text='country_name', title='Top 7 Cidades com Restaurantes com Média de Avaliação Acima de 4.0')
    
    fig = fig.update_layout(xaxis_title='Cidades',
                            yaxis_title='Quantidade de Restaurantes',
                            legend_title='País')
    
    fig = fig.update_traces(texttemplate='%{y}', hovertemplate='País: %{text} <br>Cidades: %{x} <br>Quantidade de Restaurantes: %{y}')

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


#Cities

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


#Título da página Cities
st.markdown('# 🏙️ Visão Cidades')

with st.container():

    fig = top_10_cities_restaurant(df)

    st.plotly_chart(fig, use_container_width=True) 

    
with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1: 
    
        fig = top_7_cities_lowest_rating(df)
        
        st.plotly_chart(fig, use_container_width=True) 

    
    with col2:
  
        fig = top_7_cities_highest_rating(df)
        
        st.plotly_chart(fig, use_container_width=True)     
    
with st.container():
    fig = top_10_cities_types_cuisines(df)
        
    st.plotly_chart(fig, use_container_width=True)   
    
    


    
    