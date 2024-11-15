import streamlit as st
import pandas as pd
from pydantic import ValidationError
from pandera.typing import DataFrame
import sqlite3
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


# Função para carregar dados do banco de dados
def load_data(table_name):
    # Conecte-se ao banco de dados SQLite
    con = sqlite3.connect('data/forecast.db')
    # Leia a tabela específica do banco de dados
    df = pd.read_sql(f'SELECT * FROM {table_name}', con)
    # Feche a conexão
    con.close()
    return df

# Carregar dados Realizado e Orçado
st.subheader("Dados Realizado vs Orçado")
realizado = load_data('realizado')
orcado = load_data('orcado')

# Função para criar o layout Realizado vs Orçado
def create_comparison_table(realizado, orcado):
    # Adicionar uma coluna para diferenciar Realizado de Orçado
    realizado['Tipo'] = 'Realizado'
    orcado['Tipo'] = 'Orçado'
    combined_df = pd.concat([realizado, orcado], ignore_index=True)

    # Pivotar os dados com Negocio, Gerencia, Tecnologia, Produto na vertical e Ano/Mês na horizontal
    pivot_table = pd.pivot_table(
        combined_df,
        values='Receita_Liquida',  # Usar a coluna correta para valores
        index=['Negocio', 'Gerencia', 'Tecnologia', 'Produto', 'Tipo'],
        columns=['Ano', 'Mes'],
        aggfunc='sum',
        fill_value=0
    )
    return pivot_table

# Exibir tabela Realizado vs Orçado
comparison_table = create_comparison_table(realizado, orcado)
st.write("Tabela de Realizado vs Orçado")
st.dataframe(comparison_table)

# Função para criar a tabela de input do forecast com meses na horizontal
def create_forecast_input_table(orcado):
    # Gerar os próximos 12 meses
    today = datetime.today()
    forecast_dates = pd.date_range(today, periods=12, freq='M')
    
    # Obter todos os agrupadores únicos de Negocio, Gerencia, Tecnologia, Produto a partir do DataFrame Orçado
    unique_groups = orcado[['Negocio', 'Gerencia', 'Tecnologia', 'Produto']].drop_duplicates()
    
    # Criar um DataFrame com esses agrupadores e os meses na horizontal para o forecast
    forecast_df = unique_groups.copy()
    for date in forecast_dates:
        forecast_df[(date.year, date.month)] = float(0.01)  # Inicializa com zero para cada mês
    
    # Ajustar o índice e as colunas para exibir Ano/Mês na horizontal
    forecast_df.columns = pd.MultiIndex.from_tuples([('Agrupadores', col) if isinstance(col, str) else col for col in forecast_df.columns])
    return forecast_df

# Exibir e permitir input para o forecast
st.subheader("Preenchimento de Forecast para os Próximos 12 Meses")
forecast_input_df = create_forecast_input_table(orcado)

# Permitir a edição da tabela de forecast diretamente
edited_forecast = st.data_editor(forecast_input_df)

if st.button("Salvar Forecast"):
    # Especificar o caminho do arquivo CSV na pasta data
    file_path = 'data/forecast.xlsx'
    
    # Salvar o DataFrame editado como CSV
    edited_forecast.to_excel(file_path, index=False)
    
    st.write("Tabela de Forecast Preenchida:")
    st.dataframe(edited_forecast)
    st.success(f"Forecast salvo com sucesso em {file_path}!")



