import streamlit as st
import pandas as pd
from pydantic import ValidationError
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.backend.contracts.schema import DataSchema

# Upload Page Function
def upload_page():
    st.title("Upload de Arquivos")

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
        except Exception as e:
            error_message = f"Erro na leitura do arquivo: {str(e)}"
            return None, [error_message]

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

    uploaded_file = upload_file_ui()
    if uploaded_file is not None:
        file_path = os.path.join("data", uploaded_file.name)
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        data, errors = process_excel(file_path)
        if errors:
            display_errors(errors)
        else:
            if confirm_upload():
                st.success("Dados enviados com sucesso!")
                st.dataframe(data)
