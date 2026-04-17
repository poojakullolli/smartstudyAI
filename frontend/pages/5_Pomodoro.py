import streamlit as st
import time

st.set_page_config(page_title="Pomodoro", page_icon="🍅", layout="centered")

st.title("Pomodoro Timer 🍅")

if "pomodoro_running" not in st.session_state:
    st.session_state["pomodoro_running"] = False

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    mode = st.radio("Mode", ["Focus (25m)", "Short Break (5m)", "Long Break (15m)"], horizontal=True)
    
    if mode == "Focus (25m)":
        minutes = 25
    elif mode == "Short Break (5m)":
        minutes = 5
    else:
        minutes = 15

    timer_placeholder = st.empty()
    timer_placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{minutes:02d}:00</h1>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    start = c1.button("Start Timer")
    stop = c2.button("Stop Timer")

    if start:
        st.session_state["pomodoro_running"] = True
    if stop:
        st.session_state["pomodoro_running"] = False

    if st.session_state["pomodoro_running"]:
        total_seconds = minutes * 60
        for i in range(total_seconds, -1, -1):
            if not st.session_state["pomodoro_running"]:
                break
            
            mins, secs = divmod(i, 60)
            timer_placeholder.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
            time.sleep(1)
        
        if i == 0:
            st.success("Time's up!")
            st.balloons()
            st.session_state["pomodoro_running"] = False
