#Libraries
from PIL import Image
import plotly.express as px

#Bibliotecas necessárias
import pandas as pd
import inflection
import streamlit as st



#Configuração básica da página
st.set_page_config(page_title='Cuisines', layout="wide")

# ======================================
# Funções
# ======================================


#Métrica culinárias mais comuns
def metric_help_cuisines(df, principal_culinaria):
    cols = ['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'currency', 'average_cost_for_two', 'aggregate_rating', 'votes']
    lins = (df['cuisines'] == 'Brazilian')| (df['cuisines'] == 'Arabian') | (df['cuisines'] == 'Italian') | (df['cuisines'] == 'Japanese') | (df['cuisines'] == 'American')

    dfaux_df = df.loc[lins, cols].groupby(['country_name', 'city', 'currency', 'average_cost_for_two', 'restaurant_name', 'cuisines']).agg({'aggregate_rating' : 'max', 'restaurant_id' : 'min'}).sort_values(by=['aggregate_rating', 'restaurant_id', 'cuisines'], ascending=[False, True, True]).reset_index()

    df_principal_culinaria = dfaux_df.loc[dfaux_df['cuisines'] == principal_culinaria, :]

    df_principal_culinaria = df_principal_culinaria.head(1)
    
    label_metric = f'{df_principal_culinaria.iloc[0,5]}: {df_principal_culinaria.iloc[0,4]}'
    value_metric = f'{df_principal_culinaria.iloc[0,6]}/5.0'
    help_metric = (f'''País: {df_principal_culinaria.iloc[0,0]}
        
Cidade: {df_principal_culinaria.iloc[0,1]}

Preço Médio do prato para dois: {df_principal_culinaria.iloc[0,3]} ({df_principal_culinaria.iloc[0,2]})''')

    return label_metric, value_metric, help_metric



#Top 10 Restaurantes - Regras: Maior Aggregate_Rating, Desempate: Restaurant_id mais antigo

def top_restaurant(df):
    
    #Filtros de países
    linhas_selecionadas = df['country_name'].isin( countries_options )
    df = df.loc[linhas_selecionadas, :]

    #Filtros de culinarias
    linhas_selecionadas = df['cuisines'].isin( cuisines_options )
    df = df.loc[linhas_selecionadas, :]
    
    cols = ['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']
    df = df.loc[:, cols].sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True])
    
    df = df.head(valor_top)
    
    
    return df


#Top 10 Piores Tipos de Culinarias

def top_10_piores_culinarias(df):
    
    #Filtros de países
    linhas_selecionadas = df['country_name'].isin( countries_options )
    df = df.loc[linhas_selecionadas, :]
    
    cols = ['aggregate_rating', 'cuisines']

    dfaux = round(df.loc[: , cols].groupby(['cuisines']).mean().sort_values('aggregate_rating', ascending=True).reset_index(), 2)
    
    dfaux = dfaux.head(valor_top)
    
    fig = px.bar(dfaux, x='cuisines', y='aggregate_rating', text='aggregate_rating')
    
    fig = fig.update_layout(title=f'Top {valor_top} Piores Tipos de Culinárias',
                        xaxis_title='Tipos de Culinária',
                        yaxis_title='Média da Avaliação Média')
    
    fig = fig.update_traces(textfont=dict(size=14), hovertemplate='Tipo de Culinária: %{x} <br>Média da Avaliação Média: %{y}', texttemplate='%{y:.2f}')
    
    return fig

#Top 10 Melhores Tipos de Culinarias

def top_10_melhores_culinarias(df):
    
    #Filtros de países
    linhas_selecionadas = df['country_name'].isin( countries_options )
    df = df.loc[linhas_selecionadas, :]

    cols = ['aggregate_rating', 'cuisines']

    dfaux = round(df.loc[: , cols].groupby(['cuisines']).mean().sort_values('aggregate_rating', ascending=False).reset_index(), 2)
    
    dfaux = dfaux.head(valor_top)
    
    fig = px.bar(dfaux, x='cuisines', y='aggregate_rating', text='aggregate_rating')
    
    fig = fig.update_layout(title=f'Top {valor_top} Melhores Tipos de Culinárias',
                        xaxis_title='Tipos de Culinária',
                        yaxis_title='Média da Avaliação Média')
    
    fig = fig.update_traces(textfont=dict(size=14), hovertemplate='Tipo de Culinária: %{x} <br>Média da Avaliação Média: %{y}', texttemplate='%{y:.2f}')

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


#Cuisines

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


valor_top = st.sidebar.slider('_Selecione a quantidade de Restaurantes que deseja visualizar_', 
                  value=10,
                  min_value=1,
                  max_value=20)


cuisines_options = st.sidebar.multiselect(
    '_Escolha os Tipos de Culinária_',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian', 'Author',
       'Gourmet Fast Food', 'Lebanese', 'Modern Australian', 'African',
       'Coffee and Tea', 'Australian', 'Middle Eastern', 'Malaysian',
       'Tapas', 'New American', 'Pub Food', 'Southern', 'Diner', 'Donuts',
       'Southwestern', 'Sandwich', 'Irish', 'Mediterranean', 'Cafe Food',
       'Korean BBQ', 'Fusion', 'Canadian', 'Breakfast', 'Cajun',
       'New Mexican', 'Belgian', 'Cuban', 'Taco', 'Caribbean', 'Polish',
       'Deli', 'British', 'California', 'Others', 'Eastern European',
       'Creole', 'Ramen', 'Ukrainian', 'Hawaiian', 'Patisserie',
       'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan', 'Burmese',
       'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian', 'Continental',
       'South Indian', 'North Indian', 'Salad', 'Finger Food', 'Mandi',
       'Turkish', 'Kerala', 'Pakistani', 'Biryani', 'Street Food',
       'Nepalese', 'Goan', 'Iranian', 'Mughlai', 'Rajasthani', 'Mithai',
       'Maharashtrian', 'Gujarati', 'Rolls', 'Momos', 'Parsi',
       'Modern Indian', 'Andhra', 'Tibetan', 'Kebab', 'Chettinad',
       'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi', 'Afghan',
       'Lucknowi', 'Charcoal Chicken', 'Mangalorean', 'Egyptian',
       'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian', 'Western',
       'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian', 'Balti',
       'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji', 'South African',
       'Durban', 'World Cuisine', 'Izgara', 'Home-made', 'Giblets',
       'Fresh Fish', 'Restaurant Cafe', 'Kumpir', 'Döner',
       'Turkish Pizza', 'Ottoman', 'Old Turkish Bars', 'Kokoreç'],
    
    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian'] )


st.sidebar.markdown("""___""")
st.sidebar.markdown("###### Desenvolvido por Lais Araujo")



# ======================================
# Layout Streamlit
# ======================================


#Título da página Cuisines
st.title('🍽️ Visão Tipos de Culinária')
st.markdown('## Melhores Restaurantes dos Principais Tipos de Culinárias')
         
with st.container():
    

    col1, col2, col3, col4, col5 = st.columns(5, gap = 'small') 

    with col1:
        
        resultado = metric_help_cuisines(df, 'Italian')
        st.metric(label=resultado[0], value=resultado[1], help=resultado[2])

    with col2:
        
        resultado = metric_help_cuisines(df, 'American')
        st.metric(label=resultado[0], value=resultado[1], help=resultado[2])
        
    with col3:
        
        resultado = metric_help_cuisines(df, 'Arabian')
        st.metric(label=resultado[0], value=resultado[1], help=resultado[2])

    with col4:

        resultado = metric_help_cuisines(df, 'Japanese')
        st.metric(label=resultado[0], value=resultado[1], help=resultado[2])

    with col5:

        resultado = metric_help_cuisines(df, 'Brazilian')
        st.metric(label=resultado[0], value=resultado[1], help=resultado[2])
        
        
with st.container():        
        
    st.markdown(f'## Top {valor_top} Restaurantes')
    
    tab = top_restaurant(df)
    st.dataframe(tab, use_container_width=True)
    
    
with st.container():
    
    col1, col2 = st.columns(2) 

    with col1:
        
        fig = top_10_melhores_culinarias(df)
        st.plotly_chart(fig, use_container_width=True)
    

    with col2:
    
        fig = top_10_piores_culinarias(df)
        st.plotly_chart(fig, use_container_width=True)
    

