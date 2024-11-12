from faker import Faker
import pandas as pd
import random
import openpyxl

# Inicializando Faker
faker = Faker('pt_BR')

# Definindo algumas categorias e produtos para simular
negocios = ['B2B', 'B2C']
gerencias = ['Moveis', 'Calcado', 'Construcao', 'Exportacao']
tecnologias = ['Aquosos', 'Solventes', 'Hot Melt']
produtos = {
    'Aquosos': ['Produto 2156', 'Produto 5149', 'Produto 5649'],
    'Solventes': ['Produto 1126', 'Produto 1254', 'Produto 9678'], 
    'Hot Melt': ['Produto 1314', 'Produto 1615', 'Produto 1821']
}

#Função para gerar os dados para o forecast
def gerar_dados_forecast(num_linhas=200):
    dados = []
    for _ in range(num_linhas):
        negocio = random.choice(negocios)
        gerencia = random.choice(gerencias)
        tecnologia = random.choice(tecnologias)
        produto = random.choice(produtos[tecnologia])
        
        receita_liquida = round(random.uniform(500, 50000), 2)
        
        linha = {
            'Ano': 2024,
            'Mes': faker.month(),
            'Negocio': negocio,
            'Gerencia': gerencia,
            'Tecnologia': tecnologia,
            'Produto': produto,
            'Receita Liquida': receita_liquida,
        }
        dados.append(linha)
    
    return pd.DataFrame(dados)


if __name__ == "__main__":
    df_re = gerar_dados_forecast(1000)
    df_re.to_excel("data/df_re.xlsx")

    df_or = gerar_dados_forecast(1000)
    df_or.to_excel("data/df_or.xlsx")