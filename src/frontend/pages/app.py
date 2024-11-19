import streamlit as st
import os
import sys
from upload_page import upload_page
from display_page import display_page
from dash import dashboard
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
