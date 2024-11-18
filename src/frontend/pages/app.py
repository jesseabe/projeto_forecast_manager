import streamlit as st
import os
import sys
from upload_page import upload_page
from display_page import display_page
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def main():
    st.title("Dashboard Navigation")
    
    # Navigation Menu
    page = st.radio("Navigate to:", ["Upload Arquivos", "Preencher Forecast"])
    
    if page == "Upload Arquivos":
        upload_page()  # Call the function from upload_page.py
    elif page == "Preencher Forecast":
        display_page()  # Call the function from display_page.py

if __name__ == "__main__":
    main()
