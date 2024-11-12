import streamlit as st
import pandas as pd
from pydantic import ValidationError
from pandera.typing import DataFrame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.backend.contracts.schema import DataSchema



# Funções da UI
def upload_file_ui():
    return st.file_uploader("Escolha o arquivo Excel", type="xlsx")

def display_errors(errors):
    for error in errors:
        st.error(error)

def confirm_upload():
    return st.button("Subir Dados")

def renomeia_colunas(df: pd.DataFrame, renomeia_colunas: dict) -> pd.DataFrame:
    df.rename(columns=renomeia_colunas, inplace=True)
    return df

# Função para processar o arquivo Excel e salvar o DataFrame
def process_excel(file):
   renomeia_colunas_dict = {
    'Ano': 'Ano',
    'Mes': 'Mes',
    'Negocio': 'Negocio',
    'Gerencia': 'Gerencia',
    'Tecnologia': 'Tecnologia',
    'Produto': 'Produto',
    'Receita_Liquida': 'Receita_Liquida'
    }
   try:
        df = pd.read_excel(file)
        df = renomeia_colunas(df, renomeia_colunas_dict)
        
        errors = validate_dataframe(df)
        return df, errors
   
   except:
        # Tratamento de erro
        column_names = df.columns.tolist() if 'df' in locals() else 'N/A'
        error_message = f"Erro na leitura do arquivo: {str(e)}"
        if column_names != 'N/A':
            error_message += f"\nColunas do DataFrame: {', '.join(column_names)}"
            for column in column_names:
                try:
                    sample_data = df[column].head().tolist()  # Obtém amostras dos dados da coluna
                except KeyError:
                    sample_data = 'Coluna não encontrada'
                error_message += f"\nDados da coluna '{column}': {sample_data}"
        return None, [error_message]


# Função para validar o DataFrame usando ProdutoSchema
def validate_dataframe(df):
    errors = []
    required_columns = DataSchema.__annotations__.keys()
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        errors.append(f"Faltam colunas no arquivo: {', '.join(missing_columns)}")
    
    for _, row in df.iterrows():
        try:
            DataSchema(**row.to_dict())
        except ValidationError as e:
            errors.append(f"Erro de validação na linha {row.name + 1}: {e}")
    
    return errors

# Função principal
def main():
    st.title("Upload de Arquivos")

    uploaded_file = upload_file_ui()
    if uploaded_file is not None:
        # Definir o caminho de salvamento usando o nome do arquivo original
        file_path = os.path.join("data", uploaded_file.name)
        os.makedirs("data", exist_ok=True)
        
        # Salvar o arquivo no disco
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Processar o arquivo
        data, errors = process_excel(file_path)
        if errors:
            display_errors(errors)
        else:
            if confirm_upload():
                st.success("Dados enviados com sucesso!")
                # Opcional: mostrar uma amostra dos dados
                if data is not None:
                    st.dataframe(data)

if __name__ == "__main__":
    main()