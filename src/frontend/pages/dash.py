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
    st.title("Dashboard de Resultados - Visão Geral")

    def load_data(table_name):
        con = sqlite3.connect('data/forecast.db')
        df = pd.read_sql(f'SELECT * FROM {table_name}', con)
        con.close()
        return df

    # Carregando os dados
    df_realizado = load_data("realizado")
    df_agregado = load_data("dfagregado")
    df_forecast = load_data("tbforecast")

    # Filtros interativos
    st.sidebar.header("Filtros")
    anos = sorted(df_agregado["Ano"].unique())
    negocios = sorted(df_agregado["Negocio"].unique())
    ano_selecionado = st.sidebar.selectbox("Ano", anos, index=len(anos) - 1)
    negocio_selecionado = st.sidebar.selectbox("Negócio", negocios)

    # Filtrar dados
    df_agregado_filtrado = df_agregado[
        (df_agregado["Ano"] == ano_selecionado) & (df_agregado["Negocio"] == negocio_selecionado)
    ]
    df_forecast_filtrado = df_forecast[df_forecast["Ano"] == ano_selecionado]

    # KPIs de Destaque
    st.subheader("KPIs de Destaque")
    total_realizado = df_agregado_filtrado["Realizado"].sum()
    total_orcado = df_agregado_filtrado["Orcado"].sum()
    atingimento = (total_realizado / total_orcado * 100) if total_orcado > 0 else 0
    st.metric("Total Realizado", f"R$ {total_realizado:,.2f}")
    st.metric("Total Orçado", f"R$ {total_orcado:,.2f}")
    st.metric("Atingimento (%)", f"{atingimento:.2f}%")

    # Gráfico de realizado vs orçado
    df_agrupado_mes = (
        df_agregado_filtrado.groupby("Mes")[["Realizado", "Orcado"]]
        .sum()
        .reset_index()
    )
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_agrupado_mes["Mes"],
        y=df_agrupado_mes["Realizado"],
        mode="lines+markers",
        name="Realizado",
        line=dict(color="blue", dash="solid"),
    ))
    fig1.add_trace(go.Scatter(
        x=df_agrupado_mes["Mes"],
        y=df_agrupado_mes["Orcado"],
        mode="lines+markers",
        name="Orçado",
        line=dict(color="red", dash="dash"),
    ))
    fig1.update_layout(
        title="Realizado vs Orçado por Mês",
        xaxis_title="Mês",
        yaxis_title="Valores (R$)",
        title_x=0.5,
        template="plotly_white",
    )
    st.plotly_chart(fig1)

    # Receita líquida por tecnologia
    df_tecnologia = (
        df_agregado_filtrado.groupby("Tecnologia")["Realizado"]
        .sum()
        .reset_index()
        .sort_values("Realizado", ascending=False)
    )
    fig2 = px.bar(
        df_tecnologia,
        x="Tecnologia",
        y="Realizado",
        text="Realizado",
        labels={"Tecnologia": "Tecnologia", "Realizado": "Realizado (R$)"},
        title="Realizado por Tecnologia",
    )
    fig2.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig2.update_layout(title_x=0.5, template="plotly_white")
    st.plotly_chart(fig2)

    # Projeções para os próximos 12 meses
    st.subheader("Projeções para os Próximos 12 Meses")
    df_forecast_mes = (
        df_forecast_filtrado.groupby("Mes")["Receita_Liquida"]
        .sum()
        .reset_index()
    )
    fig3 = px.line(
        df_forecast_mes,
        x="Mes",
        y="Receita_Liquida",
        title="Receita Projetada por Mês",
        labels={"Mes": "Mês", "Receita_Liquida": "Receita Líquida (R$)"},
    )
    fig3.update_layout(title_x=0.5, template="plotly_white")
    st.plotly_chart(fig3)

    # Tabelas interativas
    st.subheader("Dados Agregados")
    st.dataframe(df_agregado_filtrado)

    st.subheader("Forecast")
    st.dataframe(df_forecast_filtrado)
