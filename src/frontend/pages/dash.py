import sys
import os
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import plotly.express as px
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def dashboard():
    st.title("Dashboard de resultados")

    def load_data(table_name):
        con = sqlite3.connect('data/forecast.db')
        df = pd.read_sql(f'SELECT * FROM {table_name}', con)
        con.close()
        return df

    realizado = load_data("realizado")

    df_realizado_agrupado = realizado.groupby(["Ano", "Mes"])["Receita_Liquida"].sum()
    df_realizado_agrupado = df_realizado_agrupado.reset_index()

    #Grafico de linha do Realizado por mês
    figure(figsize=(14,8))
    plt.plot(df_realizado_agrupado["Mes"], df_realizado_agrupado["Receita_Liquida"])
    plt.xlabel("Mês")
    plt.ylabel("Receita Líquida")
    plt.title("Receita Líquida RE por mês")
    st.pyplot(plt)

    df_realizado_uen = realizado.groupby(["Ano", "Mes", "Negocio"])["Receita_Liquida"].sum()
    df_realizado_uen = df_realizado_uen.reset_index()

    figure(figsize=(14,8))
    plt.bar(df_realizado_uen["Negocio"], df_realizado_uen["Receita_Liquida"])
    plt.xlabel("Mês")
    plt.ylabel("Receita Líquida")
    plt.title("Receita Líquida RE por Negócio")
    st.pyplot(plt)

    dfagregado = load_data("dfagregado")
