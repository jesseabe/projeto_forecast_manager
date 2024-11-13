import pandas as pd
import pandera as pa
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



    