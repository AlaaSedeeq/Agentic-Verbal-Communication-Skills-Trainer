import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main { padding: 2rem; }
        .title { font-size: 2.5rem; color: #1f77b4; text-align: center; }
        .card { padding: 2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 1rem 0; }
        .chat-bubble { padding: 1rem; border-radius: 15px; margin: 0.5rem 0; max-width: 80%; }
        .user-bubble { background-color: #e3f2fd; margin-left: auto; }
        .bot-bubble { background-color: #f5f5f5; margin-right: auto; }
        .audio-message { color: #666; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)
