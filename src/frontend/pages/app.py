import streamlit as st
import os
import sys
from upload_page import upload_page
from display_page import display_page
from dash import dashboard

# Configuração inicial do Streamlit (deve ser o primeiro comando do Streamlit)
st.set_page_config(page_title="Forecast Manager", layout="wide")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def main():
    st.title("Dashboard Navigation")
    
    # Navigation Menu
    page = st.radio("Navigate to:", ["Upload Arquivos", "Preencher Forecast", "Dashboard"])
    
    if page == "Upload Arquivos":
        upload_page()  # Call the function from upload_page.py
    elif page == "Preencher Forecast":
        display_page()  # Call the function from display_page.py
    elif page == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()

