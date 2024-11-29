import pandas as pd
import pandera as pa
import os
from pandera import Column, DataFrameSchema


# Definindo o schema com Pandera
data_schema = DataFrameSchema({
    "Ano": Column(pa.Int),
    "Mes": Column(pa.Int),
    "Negocio": Column(pa.String),
    "Gerencia": Column(pa.String),
    "Tecnologia": Column(pa.String),
    "Produto": Column(pa.String),
    "Receita_Liquida": Column(pa.Float)
})

# Função para ler e validar o arquivo XLSX
def ler_xlsx(file):
    df = pd.read_excel(file)
    
    # Selecionando as colunas desejadas
    df = df[['Ano', 'Mes', 'Negocio', 'Gerencia', 'Tecnologia', 'Produto', 'Receita_Liquida']]
    
    print(df.head())
    
    try:
        # Validando o DataFrame com Pandera
        validated_df = data_schema.validate(df)
        return validated_df
    except pa.errors.SchemaError as exc:
        print("Erro ao validar os dados com Pandera")
        print(exc)
    
    return pd.DataFrame()

def process_forecast_data(filepath):
    # Carrega o arquivo Excel
    df = pd.read_excel(filepath)

    # Remove o prefixo "Agrupadores_" dos nomes das colunas
    df.columns = [col.replace("Agrupadores_", "") for col in df.columns]

    # Transforma as colunas de Ano_Mes (ex: 2024_11) em linhas usando melt
    df_melted = df.melt(id_vars=["Negocio", "Gerencia", "Tecnologia", "Produto"], 
                        var_name="Ano_Mes", 
                        value_name="Receita_Liquida")

    # Remove linhas com Receita_Liquida igual a 0 (opcional, caso deseje apenas os valores não nulos)
    df_melted = df_melted[df_melted["Receita_Liquida"] != 0]

    # Separa a coluna "Ano_Mes" em duas colunas: "Ano" e "Mes"
    df_melted[["Ano", "Mes"]] = df_melted["Ano_Mes"].str.split("_", expand=True)

    # Converte as colunas "Ano" e "Mes" para tipo inteiro
    df_melted["Ano"] = df_melted["Ano"].astype(int)
    df_melted["Mes"] = df_melted["Mes"].astype(int)

    # Converte Receita_Liquida para float64 e arredonda para 2 casas decimais
    df_melted["Receita_Liquida"] = df_melted["Receita_Liquida"].astype('float64').round(2)

    # Converte as colunas de texto para string específico do pandas (string[python])
    df_melted[['Negocio', 'Gerencia', 'Tecnologia', 'Produto']] = df_melted[['Negocio', 'Gerencia', 'Tecnologia', 'Produto']].astype('string')

    # Substitui espaços por underline (_) nos nomes das colunas
    df_melted.columns = [col.replace(" ", "_") for col in df_melted.columns]

    # Imprime os tipos de dados para verificação
    print(df_melted.dtypes)
    
    # Exclui a coluna temporária "Ano_Mes"
    df_final = df_melted.drop(columns=["Ano_Mes"])

    df_final.to_excel("data/forecast_processed.xlsx", index=False)
    os.remove(filepath)
    return df_final




    