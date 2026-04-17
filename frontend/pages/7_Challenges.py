import streamlit as st
from api_client import create_challenge, accept_challenge, get_challenges
from datetime import datetime
import sys
sys.path.append('C:\\Users\\Admin\\Desktop\\smartstudyAI\\smartstudyAI-main\\frontend')
from style_utils import inject_custom_css, add_language_selector, create_navbar

st.set_page_config(page_title="SmartStudyAI – Challenges", page_icon="📚", layout="wide")

# Inject custom CSS
inject_custom_css()
add_language_selector()

# ── Handle logout from navbar (query-param approach) ──────────────────────────
if "logout" in st.query_params:
    st.query_params.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("app.py")

if "token" not in st.session_state or st.session_state.token is None:
    st.switch_page("app.py")

with st.spinner("Loading profile..."):
    from api_client import get_me
    res = get_me(st.session_state.token)
    if res.status_code == 200:
        user_data = res.json()
        user_email = user_data.get('email', 'JD')
        initials = ''.join([part[0].upper() for part in user_email.split('@')[0].split('.') if part])[:2]
    else:
        initials = "JD"

# Render navbar
st.markdown(create_navbar("Challenges", initials), unsafe_allow_html=True)

st.title("⚔️ Friend Challenges")
st.write("---")

# Create new challenge
st.subheader("🎯 Send Challenge")

with st.form("create_challenge"):
    col1, col2, col3 = st.columns(3)
    with col1:
        opponent_email = st.text_input("Friend's Email")
    with col2:
        goal = st.selectbox("Challenge Goal", ["xp", "tasks", "hours"])
    with col3:
        duration = st.selectbox("Duration", [1, 3, 7, 14], index=2)
    
    submitted = st.form_submit_button("Send Challenge", type="primary")
    
    if submitted and opponent_email:
        with st.spinner("Sending challenge..."):
            res = create_challenge(st.session_state.token, opponent_email, goal, duration)
            if res.status_code == 200:
                st.success("Challenge sent successfully!")
            else:
                st.error(res.json().get("detail", "Failed to send challenge"))

st.write("---")

# Show challenges
st.subheader("📋 Your Challenges")

with st.spinner("Loading challenges..."):
    res = get_challenges(st.session_state.token)
    if res.status_code != 200:
        st.error("Could not load challenges")
        st.stop()
    
    challenges = res.json()

if not challenges:
    st.info("No challenges yet. Send one to a friend above!")
else:
    # Check for completed challenges to celebrate
    for c in challenges:
        if c["status"] == "completed" and "celebrated_" + str(c["id"]) not in st.session_state:
            if c["winner_email"]:
                is_winner = c["winner_email"] == st.session_state.get("user_email", "")
                if is_winner:
                    st.balloons()
                    st.success("🎉 You won the challenge against " + (c["challenger_email"] if c["is_opponent"] else c["opponent_email"]) + "!")
                else:
                    st.info("Challenge completed against " + (c["challenger_email"] if c["is_opponent"] else c["opponent_email"]))
            st.session_state["celebrated_" + str(c["id"])] = True

    # Pending challenges
    pending = [c for c in challenges if c["status"] == "pending"]
    if pending:
        st.subheader("⏳ Pending Challenges")
        for c in pending:
            with st.expander(f"Challenge from {c['challenger_email']}", expanded=True):
                st.write(f"**Goal:** {c['goal'].upper()} | **Duration:** {c['duration_days']} days")
                st.write(f"Created: {datetime.fromisoformat(c['created_at']).strftime('%Y-%m-%d %H:%M')}")
                
                if c["is_opponent"]:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Accept", key=f"accept_{c['id']}", type="primary"):
                            accept_challenge(st.session_state.token, c["id"], True)
                            st.rerun()
                    with col2:
                        if st.button("❌ Decline", key=f"decline_{c['id']}"):
                            accept_challenge(st.session_state.token, c["id"], False)
                            st.rerun()
                else:
                    st.info("Waiting for opponent to accept...")

    # Active challenges
    active = [c for c in challenges if c["status"] == "active"]
    if active:
        st.subheader("🔥 Active Challenges")
        for c in active:
            with st.expander(f"Challenge vs {c['opponent_email'] if not c['is_opponent'] else c['challenger_email']}", expanded=True):
                opponent = c['challenger_email'] if c["is_opponent"] else c['opponent_email']
                my_gain = c["opponent_gain"] if c["is_opponent"] else c["challenger_gain"]
                their_gain = c["challenger_gain"] if c["is_opponent"] else c["opponent_gain"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Your XP Gain", value=f"{my_gain} XP")
                with col2:
                    st.metric(label=f"{opponent.split('@')[0]}'s XP Gain", value=f"{their_gain} XP")
                
                # Progress bar
                total = my_gain + their_gain
                if total > 0:
                    my_percent = (my_gain / total) * 100
                    st.progress(my_percent / 100)
                
                expires = datetime.fromisoformat(c["expires_at"])
                remaining = expires - datetime.utcnow()
                st.caption(f"⏰ Expires in: {remaining.days} days {remaining.seconds//3600} hours")

    # Completed challenges
    completed = [c for c in challenges if c["status"] in ["completed", "cancelled"]]
    if completed:
        st.subheader("✅ Completed Challenges")
        for c in completed:
            opponent = c['challenger_email'] if c["is_opponent"] else c['opponent_email']
            status_icon = "✅" if c["status"] == "completed" else "❌"
            
            with st.expander(f"{status_icon} {opponent}"):
                if c["status"] == "completed":
                    my_gain = c["opponent_gain"] if c["is_opponent"] else c["challenger_gain"]
                    their_gain = c["challenger_gain"] if c["is_opponent"] else c["opponent_gain"]
                    
                    st.write(f"Your XP: {my_gain} | Their XP: {their_gain}")
                    
                    if c["winner_email"]:
                        is_winner = c["winner_email"] == st.session_state.get("user_email", "")
                        if is_winner:
                            st.success("🎉 YOU WON!")
                        else:
                            st.info(f"{c['winner_email']} won this challenge")
                    else:
                        st.info("It was a tie!")
