import tempfile
import os
from groq import Groq
import streamlit as st
import audio_recorder_streamlit as ars
from src.common.config import load_config

CONFIG = load_config().llms
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
voice_model_name = CONFIG.opensource.groq.voice_llm if CONFIG.opensource.voice_llm == "groq" \
                    else CONFIG.opensource.huggingface.voice_llm

def get_graph_response():
    # try:
    print("State : ", st.session_state.graph_state)
    print("Config: ", st.session_state.graph_config)
    graph_response = st.session_state.graph.invoke(st.session_state.graph_state, st.session_state.graph_config)
    print("Graph Response: ", graph_response)
    st.session_state.graph_state = graph_response
    return graph_response["messages"][-1].content    
    # except Exception as e:
    #     print(e)
    #     st.error(f"There was an error, please try later!====")
    #     return None

def transcribe_audio(audio_file_path):
    """Transcribe audio using Groq's Whisper implementation."""
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model=voice_model_name,
                prompt=(
                    """The audio is by a programmer discussing programming issues, """
                    """the programmer mostly uses python and might mention python """
                    """libraries or reference code in his speech."""
                ),  # Fixed missing comma and closing parenthesis
                response_format="text",
                language="en",
            )
        return transcription.text if hasattr(transcription, 'text') else str(transcription)
    except Exception as e:
        st.error(f"Transcription error: {str(e)}")
        return None

def handle_audio_input(audio_bytes):
    """Handle audio input and return transcription."""
    if audio_bytes:
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        # Transcribe the audio
        transcript = transcribe_audio(temp_audio_path)
        
        # Clean up temporary file
        os.unlink(temp_audio_path)
        
        return transcript
    return None

def chat_page():
    st.title("💬 Verbal Communication Skills Trainer")
    
    if st.session_state.user_choices["module"] == "Presentation Assessment":
        st.subheader("🎤 Presentation Assessment Session")
    else:
        st.subheader(f"📚 {st.session_state.user_choices['skill']} - {st.session_state.user_choices['category']}")
    
    chat_container = st.container(height=400)
    
    for msg in st.session_state.chat_history:
        with chat_container:
            if msg["role"] == "user":
                if msg["type"] == "audio":
                    st.markdown(f"<div class='chat-bubble user-bubble audio-message'>🎤 Audio submitted</div>", 
                               unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-bubble user-bubble'>{msg['content']}</div>", 
                               unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble bot-bubble'>{msg['content']}</div>", 
                           unsafe_allow_html=True)
    
    with st.form("chat_input"):
        user_input = st.text_input("Type your message...", key="user_input")
        audio_bytes = ars.audio_recorder(pause_threshold=2.0)
        submitted = st.form_submit_button("Submit")

    if submitted:
        if user_input or audio_bytes:
            # Handle text input
            if user_input:
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_input,
                    "type": "text"
                })
                st.session_state.graph_state["messages"].append(
                    {
                        "role": "user", 
                        "content": user_input
                        }
                    )

                response = get_graph_response()
                print("Response: ", response)
                st.session_state.chat_history.append({
                    "role": "bot",
                    "content": response
                })

                st.rerun()            

            # Handle audio input
            if audio_bytes:
                # Save audio to session state
                st.session_state.audio_bytes = audio_bytes
                
                # Add audio message to chat history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": "[Audio Recording]",
                    "type": "audio"
                })
                
                # Transcribe audio and get response
                transcript = handle_audio_input(audio_bytes)
                if transcript:
                    # Add transcription to chat history
                    st.session_state.chat_history.append({
                        "role": "bot",
                        "content": f"Transcript: {transcript}"
                    })
                    
                    # Get analysis from LLM
                    analysis_response = get_graph_response()
                    st.session_state.chat_history.append({
                        "role": "bot",
                        "content": analysis_response
                    })
                else:
                    st.session_state.chat_history.append({
                        "role": "bot",
                        "content": "Could not process audio. Please try again."
                    })
                
                st.rerun()