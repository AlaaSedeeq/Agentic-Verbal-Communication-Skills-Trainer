import streamlit as st

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "user_choices" not in st.session_state:
        st.session_state.user_choices = {}
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "audio_bytes" not in st.session_state:
        st.session_state.audio_bytes = None
