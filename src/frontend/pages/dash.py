import sys
import os
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import plotly.express as px
import plotly.graph_objects as go

def dashboard():
    st.title("Dashboard de Resultados")

    def load_data(table_name):
        con = sqlite3.connect('data/forecast.db')
        df = pd.read_sql(f'SELECT * FROM {table_name}', con)
        con.close()
        return df

    # Carregando os dados
    realizado = load_data("realizado")

    # Gráfico de linha do realizado por mês
    df_realizado_agrupado = (
        realizado.groupby(["Ano", "Mes"])["Receita_Liquida"]
        .sum()
        .reset_index()
    )
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_realizado_agrupado["Mes"],
        y=df_realizado_agrupado["Receita_Liquida"],
        mode='lines+markers',
        name="Receita Líquida",
        line=dict(color="blue"),
        marker=dict(size=8),
    ))
    fig1.update_layout(
        title="Receita Líquida RE por Mês",
        xaxis_title="Mês",
        yaxis_title="Receita Líquida (R$)",
        title_x=0.5,
        template="plotly_white",
    )
    st.plotly_chart(fig1)

    # Gráfico de barras por negócio
    df_realizado_uen = (
        realizado.groupby(["Negocio"])["Receita_Liquida"]
        .sum()
        .reset_index()
    )
    fig2 = px.bar(
        df_realizado_uen,
        x="Negocio",
        y="Receita_Liquida",
        text="Receita_Liquida",
        labels={"Negocio": "Negócio", "Receita_Liquida": "Receita Líquida (R$)"},
        title="Receita Líquida por Negócio",
    )
    fig2.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig2.update_layout(title_x=0.5, template="plotly_white")
    st.plotly_chart(fig2)

    # Gráfico de Realizado vs. Orcado
    dfagregado = load_data("dfagregado")
    dfagreado_agrupado = (
        dfagregado.groupby(["Ano", "Mes"])[["Realizado", "Orcado"]]
        .sum()
        .reset_index()
    )
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=dfagreado_agrupado["Mes"],
        y=dfagreado_agrupado["Realizado"],
        mode="lines+markers",
        name="Realizado",
        line=dict(color="blue", dash="solid"),
    ))
    fig3.add_trace(go.Scatter(
        x=dfagreado_agrupado["Mes"],
        y=dfagreado_agrupado["Orcado"],
        mode="lines+markers",
        name="Orçado",
        line=dict(color="red", dash="dash"),
    ))
    fig3.update_layout(
        title="Realizado vs Orçado por Mês",
        xaxis_title="Mês",
        yaxis_title="Valores (R$)",
        title_x=0.5,
        template="plotly_white",
    )
    st.plotly_chart(fig3)

