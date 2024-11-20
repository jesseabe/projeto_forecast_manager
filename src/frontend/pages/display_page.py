import sys
import os
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def display_page():
    st.title("📊 Dados Realizado vs Orçado")

    def load_data(table_name):
        con = sqlite3.connect('data/forecast.db')
        df = pd.read_sql(f'SELECT * FROM {table_name}', con)
        con.close()
        return df

    def create_comparison_table(realizado, orcado):
        realizado['Tipo'] = 'Realizado'
        orcado['Tipo'] = 'Orçado'
        combined_df = pd.concat([realizado, orcado], ignore_index=True)

        pivot_table = pd.pivot_table(
            combined_df,
            values='Receita_Liquida',
            index=['Negocio', 'Gerencia', 'Tecnologia', 'Produto', 'Tipo'],
            columns=['Ano', 'Mes'],
            aggfunc='sum',
            fill_value=0
        )
        return pivot_table

    def create_forecast_input_table(orcado):
        today = datetime.today()
        forecast_dates = pd.date_range(today, periods=12, freq='M')
        unique_groups = orcado[['Negocio', 'Gerencia', 'Tecnologia', 'Produto']].drop_duplicates()
        
        forecast_df = unique_groups.copy()
        for date in forecast_dates:
            forecast_df[(date.year, date.month)] = float(0.01)
        
        forecast_df.columns = pd.MultiIndex.from_tuples([('Agrupadores', col) if isinstance(col, str) else col for col in forecast_df.columns])
        return forecast_df

    realizado = load_data('realizado')
    orcado = load_data('orcado')

    # Adicionar filtros para Negócio, Gerência e Produto
    st.sidebar.header("Filtros")
    negocio_filter = st.sidebar.multiselect("Selecione o Negócio:", options=realizado["Negocio"].unique(), default=realizado["Negocio"].unique())
    gerencia_filter = st.sidebar.multiselect("Selecione a Gerência:", options=realizado["Gerencia"].unique(), default=realizado["Gerencia"].unique())
    produto_filter = st.sidebar.multiselect("Selecione o Produto:", options=realizado["Produto"].unique(), default=realizado["Produto"].unique())

    # Aplicar filtros
    realizado = realizado[realizado["Negocio"].isin(negocio_filter) & realizado["Gerencia"].isin(gerencia_filter) & realizado["Produto"].isin(produto_filter)]
    orcado = orcado[orcado["Negocio"].isin(negocio_filter) & orcado["Gerencia"].isin(gerencia_filter) & orcado["Produto"].isin(produto_filter)]

    comparison_table = create_comparison_table(realizado, orcado)
    st.write("### 📈 Tabela de Realizado vs Orçado")
    st.dataframe(comparison_table, use_container_width=True, height=500)

    st.write("---")  # Separador visual
    st.subheader("📅 Preenchimento de Forecast para os Próximos 12 Meses")
    forecast_input_df = create_forecast_input_table(orcado)

    edited_forecast = st.data_editor(forecast_input_df, use_container_width=True, height=500)

    if st.button("💾 Salvar Forecast"):
        file_path = 'data/forecast.xlsx'
        edited_forecast.to_excel(file_path, index=False)
        st.success(f"✅ Forecast salvo com sucesso em {file_path}!")




