# 1. Problema de Negócio

Você acaba de ser contratado como Cientista de Dados da empresa
Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra
a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer
utilizando dados!
A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

### **O Desafio:**

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

### **Geral**

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

### **País:**

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas
6. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
7. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
8. Qual o nome do país que possui, na média, a maior nota média registrada?
11. Qual o nome do país que possui, na média, a menor nota média registrada?
12. Qual a média de preço de um prato para dois por país?

### **Cidade:**

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?

### **Restaurantes:**

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?

### **Tipos de Culinária:**

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Qual o tipo de culinária que possui a maior nota média?

O CEO também pediu que fosse gerado um dashboard que permitisse que ele
visualizasse as principais informações das perguntas que ele fez. O CEO precisa
dessas informações o mais rápido possível, uma vez que ele também é novo na
empresa e irá utilizá-las para entender melhor a empresa Fome Zero para conseguir
tomar decisões mais assertivas.
Seu trabalho é utilizar os dados que a empresa Fome Zero possui e responder as
perguntas feitas do CEO e criar o dashboard solicitado.

# 2. **Premissas assumidas para a análise**

1. Marketplace foi o modelo de negócio utilizado.
2. As 4 principais visões de negócio foram: Visão geral da base de dados, Visão países, visão cidades e visão tipos de culinária.

# 3. **Estratégia da solução**

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

1. 📈 Visão Geral
2. 🌎 Visão Países
3. 🏙️ Visão Cidades
4. 🍽️ Visão Tipos de Culinária

Cada visão é representada pelo seguinte conjunto de métricas.

1. 📈 **Visão Geral**
    1. Quantidade de restaurantes cadastrados na base de dados.
    2. Quantidade de países cadastrados na base de dados.
    3. Quantidade de cidades cadastradas na base de dados.
    4. Total de avaliações feitas na plataforma.
    5. Quantidade de tipos de culinárias cadastradas na base de dados.
    6. Visão geográfica dos estabelecimentos destacados de acordo com a classificação agregada.
    
2. 🌎 **Visão Países**
    1. Quantidade de restaurantes registrados por país.
    2. Quantidade de cidades registradas por país.
    3. Média de avaliações feitas por país.
    
3. 🏙️ **Visão Cidades**
    1. Top 10 cidades com mais restaurantes cadastrados na base de dados.
    2. Top 7 cidades com restaurantes que possuem média de avaliação acima de 4,0.
    3. Top 7 cidades com restaurantes que possuem média de avaliação abaixo de 2,5.
    4. Top 10 cidades com mais restaurantes que possuem tipos de culinária distintas.
    
4. 🍽️ **Visão Tipos de Culinárias**
    1. Melhores restaurantes de acordo com os principais tipos de culinárias (Italian, American, Arabian, Japanese e Brazilian).
    2. Top restaurantes de acordo com a quantidade selecionada no filtro pelo usuário.
    3. Top melhores e piores tipos de culinária de acordo com a quantidade selecionada no filtro pelo usuário.
    

# 4. **Top 3 Insights de dados**

1. A maior concentração de restaurantes cadastrados está localizado na Índia.
2. A Indonésia é o país que possui maior média de avaliações realizadas.
3. O pior tipo de culinária avaliado é o Tex-Mex, com avaliação 2,05.

# 5. **O produto final do projeto**

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: [https://ls-project-fome-zero.streamlit.app/](https://ls-project-fome-zero.streamlit.app/)

# 6. **Conclusão**

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

Foi gerado um dashboard que permite a visão macro das principais informações da empresa.

# 7. **Próximos passos**

1. Criar novos filtros.
2. Adicionar novas visões de negócio.
