#Libraries
from PIL import Image
import plotly.express as px

#Bibliotecas necessárias
import pandas as pd
import inflection
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
from millify import millify


#Configuração básica da página
st.set_page_config(page_title='Home', layout="wide")

# ======================================
# Funções
# ======================================

#Mapa dos pontos de Restaurantes x Avaliação
def restaurant_maps(df):
    
    # Filtros Streamlit
    #filtro dos países
    linhas_selecionadas = df['country_name'].isin( countries_options )
    df = df.loc[linhas_selecionadas, :]
    
    #criando mapa com os pontos centrais das localizações (lat / long)
    map = folium.Map()
    
    cluster = MarkerCluster().add_to(map)

    for index, location_info in df.iterrows():
        
        texto_html = f"<h6><p style='line-height: 1.5;'><b> <i class='fa-solid fa-utensils fa-lg'></i> {location_info['restaurant_name']}</b><br><br> Price:  {'{:.2f}'.format(location_info['average_cost_for_two'])} ({location_info['currency']}) para dois<br> Type: {location_info['cuisines']} <br> Aggragete Rating: {location_info['aggregate_rating']}/5.0<br></p></h6>"
        
        folium.Marker([location_info['latitude'], 
                     location_info['longitude']],
                     popup=folium.Popup(texto_html, unsafe_allow_html=True, max_width=500),
                     icon=folium.Icon(color=location_info['color_name'],
                                      icon='house',
                                      prefix='fa')).add_to(cluster)


    folium_static(map, width=1024, height=600)
    

#Converter o DataFrame em CSV para download
def convert_df(df):
    lista_columns = list(['restaurant_id', 'restaurant_name', 'country_name', 'city', 'address',
       'locality', 'locality_verbose', 'longitude', 'latitude', 'cuisines', 
       'price_type', 'average_cost_for_two', 'currency', 'has_table_booking',
       'has_online_delivery', 'is_delivering_now', 'aggregate_rating', 
      'rating_color', 'color_name', 'rating_text', 'votes'])
    
    return df.to_csv(sep=';', columns=lista_columns, index=False, encoding='utf-8')



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
    df = df

    return df



#---------------------------------------------- Inicialização do Script ----------------------------------------------
# ======================================
# Limpeza do dataframe
# ======================================

#Import dataset
df_raw = pd.read_csv('dataset/zomato.csv')

# Fazendo uma cópia do DataFrame Lido
df = clean_code(df_raw)
        
    
#Main Page

# ======================================
# Barra Lateral Streamlit
# ======================================

# Exibindo a logo na sidebar
image_logo = Image.open("images/logofomezero.png")
st.sidebar.image( image_logo, width=160)


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
st.sidebar.markdown('## Dados Tratados')
st.sidebar.write('##### _Clique no botão abaixo para realizar o download do arquivo com os dados tratados_')


#Adicionando um botão de download na barra lateral
st.sidebar.download_button("📂 Download CSV File",
                           convert_df(df),
                           file_name="data_tratado.csv",
                           mime="text/csv")



#Informação final da sidebar - Desenvolvido por
st.sidebar.markdown("""___""")
st.sidebar.markdown("###### Desenvolvido por Lais Araujo")



# ======================================
# Layout Streamlit
# ======================================

#Texto de indtrodução ao app
st.image( image_logo, width=350)
st.markdown('<p><h2>➡️ O Melhor lugar para encontrar seu mais novo restaurante favorito!</h2></p>', unsafe_allow_html=True)

         
with st.container():
    st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
    

    col1, col2, col3, col4, col5 = st.columns(5, gap = 'small') 

    with col1:
        result = millify(df['restaurant_id'].nunique(), precision=1)
        col1.metric('Restaurantes Cadastrados', result)

    with col2:
        result = df['country_code'].nunique()
        col2.metric('Países Cadastrados', result)
        
    with col3:
        result = df['city'].nunique()
        col3.metric('Cidades Cadastradas', result)

    with col4:
        result = millify(df['votes'].sum(), precision=2)
        col4.metric('Avaliações Feitas na Plataforma', result)

    with col5:
        result = df['cuisines'].nunique()
        col5.metric('Tipos de Culinárias Oferecidas', result)

        
with st.container():

    restaurant_maps(df)
    
    