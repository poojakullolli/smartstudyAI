import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import api_client

st.set_page_config(page_title="Doubt Explainer", page_icon="💡", layout="wide")

if "token" not in st.session_state:
    st.warning("Please login from the main page.")
    st.stop()

token = st.session_state["token"]

st.title("Smart Doubt Explainer 💡")

# Sidebar for history
st.sidebar.title("Your Previous Doubts")
history = api_client.get_history(token)

if history:
    for item in history[:10]: # show last 10
        with st.sidebar.expander(item["question"][:30] + "..."):
            st.markdown(f"**Difficulty:** {item['difficulty']}")
            st.markdown(item["answer"])
else:
    st.sidebar.info("No doubt history yet.")

difficulty = st.radio("Explain it to me:", ["like I'm 10", "intermediate", "technical"], horizontal=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("E.g. What is quantum entanglement?"):
    st.chat_message("user").markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    with st.spinner("AI is thinking..."):
        response = api_client.explain_doubt(token, prompt, difficulty)
        
        if response and "answer" in response:
            answer = response["answer"]
            st.chat_message("assistant").markdown(answer)
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            st.rerun() # Refresh history
        else:
            st.error("Failed to fetch explanation.")
            
