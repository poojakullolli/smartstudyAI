import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import api_client

st.set_page_config(page_title="Study Tracker", page_icon="✅", layout="wide")

if "token" not in st.session_state:
    st.warning("Please login from the main page.")
    st.stop()

token = st.session_state["token"]

st.title("Study Tracker ✅")
st.write("Track your tasks and progress.")

with st.expander("Add New Task"):
    with st.form("new_task"):
        c1, c2, c3 = st.columns(3)
        with c1:
            subject = st.text_input("Subject")
        with c2:
            topic = st.text_input("Topic")
        with c3:
            duration = st.number_input("Duration (minutes)", min_value=10, value=60, step=10)
        
        if st.form_submit_button("Add Task"):
            if subject and topic:
                success = api_client.create_task(token, subject, topic, duration)
                if success:
                    st.success("Added!")
                    st.rerun()
            else:
                st.error("Subject and Topic are required.")

st.subheader("Your Tasks")
tasks = api_client.get_tasks(token)

if not tasks:
    st.info("No tasks added yet.")
else:
    for task in tasks:
        col1, col2, col3, col4 = st.columns([0.5, 3, 1, 1])
        
        is_done = task["is_completed"]
        
        with col1:
            if st.checkbox("Done", value=is_done, key=f"check_{task['id']}"):
                if not is_done:
                    api_client.toggle_task(token, task["id"])
                    st.rerun()
            else:
                if is_done:
                    api_client.toggle_task(token, task["id"])
                    st.rerun()
                    
        with col2:
            st.markdown(f"**{task['subject']}** - {task['topic']} (~{task['duration_minutes']} min)")
        with col3:
            st.write(task["date"][:10])
        with col4:
            if st.button("Delete", key=f"del_{task['id']}"):
                api_client.delete_task(token, task["id"])
                st.rerun()
