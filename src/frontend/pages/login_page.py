import streamlit as st

# Dictionary to simulate a user database
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "userpass"
}

def login_page():
    st.header("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
        else:
            st.error("Invalid username or password.")
