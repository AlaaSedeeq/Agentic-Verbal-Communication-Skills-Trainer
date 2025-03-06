import streamlit as st
from src.presentation.utils import save_user_data, verify_user

def login_page():
    st.title("🤖 AI Verbal Communication Skills Trainer")
    col1, col2, col3 = st.columns([1,3,1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            with st.form("Login"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if verify_user(username, password):
                        st.session_state.username = username
                        st.session_state.authenticated = True
                        st.session_state.current_page = "choose_module"
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        with tab2:
            with st.form("Register"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")

                st.session_state.username = new_user

                if st.form_submit_button("Register"):
                    save_user_data(new_user, new_pass)
                    st.success("Registration successful!")
