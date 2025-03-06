import streamlit as st

from src.presentation.streamlit.modules import login_page, chat_page, choose_module, skills_training_page
from src.presentation.streamlit.ui import load_css
from src.presentation.streamlit.init_session import init_session_state


def main():
    load_css()
    init_session_state()
    if not st.session_state.authenticated:
        login_page()
    else:
        if st.session_state.current_page == "choose_module":
            choose_module()
        elif st.session_state.current_page == "skills_training":
            skills_training_page()
        elif st.session_state.current_page == "chat":
            chat_page()

if __name__ == "__main__":
    main()