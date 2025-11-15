import streamlit as st

def init_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def get_history():
    return st.session_state.chat_history
