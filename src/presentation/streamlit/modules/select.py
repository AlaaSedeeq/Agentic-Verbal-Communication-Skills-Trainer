import streamlit as st

from src.presentation.utils import inint_graph_state
from src.presentation.utils import get_graph, get_config
from src.common.config import load_config

CONFIG = load_config().app.graphs.skills_training.topic_categories

def choose_module():
    st.title("🎯 Select Your Learning Path")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎤 Presentation Assessment", use_container_width=True):
            # print(st.session_state)
            st.session_state.user_choices = {
                "module": "Presentation Assessment",
                "skill": "",
                "category": ""
            }

            st.session_state.graph_config = get_config(st.session_state.username)
            st.session_state.graph = get_graph(st.session_state.user_choices)        
            st.session_state.graph_state = inint_graph_state(st.session_state)
            st.session_state.chat_history.append({
                        "role": "bot",
                        "content": f"Please enter your presentation transcript below.",
                    })

            st.session_state.current_page = "chat"
            st.rerun()
    
    with col2:
        if st.button("💡 Skills Training", use_container_width=True):
            st.session_state.user_choices["module"] = "Skills Training"
            st.session_state.current_page = "skills_training"
            st.rerun()


def skills_training_page():
    st.title("📚 Skills Training Options")
    skill_choice = st.radio("Select a skill:", 
                           ["Impromptu Speaking", "Storytelling", "Conflict Resolution"])
    
    categories = {
        "Impromptu Speaking": CONFIG.impromptu_categories,
        "Storytelling": CONFIG.story_categories,
        "Conflict Resolution": CONFIG.conflict_categories
    }
    
    selected_category = st.selectbox("Choose a topic category:", categories[skill_choice])
    
    if st.button("Start Training"):
        st.session_state.user_choices.update({
            "module": "Skills Training",
            "skill": skill_choice,
            "category": selected_category
        })
        st.session_state.current_page = "chat"

        st.session_state.graph_config = get_config(st.session_state.username)

        st.session_state.graph = get_graph(st.session_state.user_choices)
        st.session_state.graph_state = inint_graph_state(st.session_state)
        st.session_state.graph_state = st.session_state.graph.invoke(st.session_state.graph_state, st.session_state.graph_config)
        topic = st.session_state.graph_state["messages"][-1].content.strip().replace("\"", "")
        st.session_state.chat_history.append(
            {
                "role": "bot",
                "content": f"""Let's talk about:\n\n {topic}"""
                }
            )

        # print("GRAPH STATE: ", st.session_state.graph_state)
        st.rerun()
