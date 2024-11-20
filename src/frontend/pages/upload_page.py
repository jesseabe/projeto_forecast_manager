import streamlit as st
import pandas as pd
from pydantic import ValidationError
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.backend.contracts.schema import DataSchema

# Página de Upload
def upload_page():
    st.title("📂 Upload de Arquivos: Realizado e Orçado")

    # Layout com colunas para uploads lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.header("🔵 Upload Realizado")
        realizado_file = st.file_uploader("Escolha o arquivo Realizado (Excel)", type="xlsx", key="realizado")

    with col2:
        st.header("🟢 Upload Orçado")
        orcado_file = st.file_uploader("Escolha o arquivo Orçado (Excel)", type="xlsx", key="orcado")

    # Função para renomear colunas
    def renomeia_colunas(df: pd.DataFrame, renomeia_colunas: dict) -> pd.DataFrame:
        df.rename(columns=renomeia_colunas, inplace=True)
        return df

    # Processamento do arquivo
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

    # Validação do DataFrame
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

    # Botão de processamento
    st.markdown("---")
    if st.button("📊 Processar Arquivos"):
        for file, label in [(realizado_file, "Realizado"), (orcado_file, "Orçado")]:
            if file:
                st.subheader(f"Resultado do Arquivo {label}")
                data, errors = process_excel(file)
                if errors:
                    st.error(f"Erros no arquivo {label}:")
                    for error in errors:
                        st.error(error)
                else:
                    st.success(f"Arquivo {label} processado com sucesso!")
                    st.dataframe(data)
            else:
                st.warning(f"Arquivo {label} não foi enviado.")
