import streamlit as st
import pandas as pd
from api_client import get_global_leaderboard, get_weekly_leaderboard
import sys
sys.path.append('C:\\Users\\Admin\\Desktop\\smartstudyAI\\smartstudyAI-main\\frontend')
from style_utils import inject_custom_css, add_language_selector, create_navbar

st.set_page_config(page_title="SmartStudyAI – Leaderboard", page_icon="📚", layout="wide")

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
st.markdown(create_navbar("Leaderboard", initials), unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Leaderboard</h1>
    <p style="color: var(--text-secondary); font-size: 1.1rem;">See how you rank against other students</p>
</div>
""", unsafe_allow_html=True)

# Tab selection
tab1, tab2 = st.tabs(["🌍 Global", "📅 Weekly"])

def display_leaderboard(data, xp_field="total_xp", title="Global Leaderboard"):
    # Top 3 cards
    if len(data["leaderboard"]) >= 1:
        st.subheader("🎖️ Top 3 Users")
        cols = st.columns(3)
        
        # Second place
        if len(data["leaderboard"]) >= 2:
            with cols[0]:
                user = data["leaderboard"][1]
                st.markdown(f"""
                <div class="leaderboard-top-card">
                    <span style="font-size: 2rem; display: block; margin-bottom: 0.5rem;">🥈</span>
                    <h3 style="margin: 0.5rem 0;">{user['badge_icon']} {user['email'].split('@')[0]}</h3>
                    <p style="color: var(--text-secondary); margin: 0.25rem 0;">Level {user['level']}</p>
                    <p style="margin: 0.5rem 0;"><span class="streak-fire">🔥</span> {user['streak']} day streak</p>
                    <div class="xp-bar-container" style="height: 8px;">
                        <div class="xp-bar-fill" style="width: {min(user[xp_field] / 5000 * 100, 100)}%"></div>
                    </div>
                    <p style="font-weight: 600; margin-top: 0.5rem;">✨ {user[xp_field]} XP</p>
                </div>
                """, unsafe_allow_html=True)
        
        # First place
        with cols[1]:
            user = data["leaderboard"][0]
            st.markdown(f"""
            <div class="leaderboard-top-card first">
                <span class="crown-icon">👑</span>
                <h2 style="margin: 0.5rem 0;">{user['badge_icon']} {user['email'].split('@')[0]}</h2>
                <p style="color: var(--text-secondary); margin: 0.25rem 0;">Level {user['level']}</p>
                <p style="margin: 0.5rem 0;"><span class="streak-fire">🔥</span> {user['streak']} day streak</p>
                <div class="xp-bar-container" style="height: 8px;">
                    <div class="xp-bar-fill" style="width: {min(user[xp_field] / 5000 * 100, 100)}%"></div>
                </div>
                <p style="font-weight: 700; font-size: 1.2rem; margin-top: 0.5rem;">✨ {user[xp_field]} XP</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Third place
        if len(data["leaderboard"]) >= 3:
            with cols[2]:
                user = data["leaderboard"][2]
                st.markdown(f"""
                <div class="leaderboard-top-card">
                    <span style="font-size: 2rem; display: block; margin-bottom: 0.5rem;">🥉</span>
                    <h3 style="margin: 0.5rem 0;">{user['badge_icon']} {user['email'].split('@')[0]}</h3>
                    <p style="color: var(--text-secondary); margin: 0.25rem 0;">Level {user['level']}</p>
                    <p style="margin: 0.5rem 0;"><span class="streak-fire">🔥</span> {user['streak']} day streak</p>
                    <div class="xp-bar-container" style="height: 8px;">
                        <div class="xp-bar-fill" style="width: {min(user[xp_field] / 5000 * 100, 100)}%"></div>
                    </div>
                    <p style="font-weight: 600; margin-top: 0.5rem;">✨ {user[xp_field]} XP</p>
                </div>
                """, unsafe_allow_html=True)

    st.write("---")
    
    # Full leaderboard
    st.subheader("📊 Full Rankings")
    
    # Create dataframe
    df_data = []
    for user in data["leaderboard"]:
        df_data.append({
            "Rank": f"#{user['rank']}",
            "Badge": user["badge_icon"],
            "User": user["email"].split('@')[0],
            "Level": user["level"],
            "Streak": f"🔥 {user['streak']}",
            "XP": user[xp_field]
        })
    
    # Add current user if not in top 50
    if data["user_rank"] > 50:
        df_data.append({
            "Rank": f"#{data['user_rank']}",
            "Badge": "⭐",
            "User": "You",
            "Level": data["user_level"],
            "Streak": f"🔥 --",
            "XP": data["user_xp"]
        })
    
    df = pd.DataFrame(df_data)
    
    # Highlight current user
    def highlight_user(row):
        if row["User"] == "You":
            return ["background: var(--primary-gradient); color: white; font-weight: 600;" for _ in row]
        return ["", "", "", "", "", ""]
    
    st.dataframe(
        df.style.apply(highlight_user, axis=1),
        use_container_width=True,
        hide_index=True
    )
    
    # User's position
    st.markdown(f"""
    <div class="glass-card" style="margin-top: 1rem; padding: 1rem; text-align: center;">
        <p style="margin: 0; font-size: 1.1rem;">
            Your rank: <strong style="font-size: 1.3rem;">#{data['user_rank']}</strong> | 
            Your XP: <strong>{data['user_xp']}</strong> | 
            Level: <strong>{data['user_level']}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)


with tab1:
    with st.spinner("Loading global leaderboard..."):
        res = get_global_leaderboard(st.session_state.token)
        if res.status_code == 200:
            data = res.json()
            display_leaderboard(data, "total_xp", "Global Leaderboard")
        else:
            st.error("Could not load leaderboard. Please try again later.")

with tab2:
    with st.spinner("Loading weekly leaderboard..."):
        res = get_weekly_leaderboard(st.session_state.token)
        if res.status_code == 200:
            data = res.json()
            display_leaderboard(data, "weekly_xp", "Weekly Leaderboard")
        else:
            st.error("Could not load leaderboard. Please try again later.")
