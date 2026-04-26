"""
SmartStudy AI — Single-Page Dashboard
======================================
One file, one app, zero page reloads.
Navigation is handled entirely via st.session_state["active_page"].
"""

import os
import sys
import time
import random
from datetime import datetime, timedelta, date

import streamlit as st
import pandas as pd

# ── Path ──────────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import (
    get_me, get_user_stats,
    create_study_plan, get_my_plans, delete_study_plan, toggle_complete,
    create_task, get_tasks, toggle_task, delete_task,
    explain_doubt, get_history,
    get_global_leaderboard, get_weekly_leaderboard,
)
from style_utils import inject_custom_css
from translations import t

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════
# st.set_page_config(
#     page_title="SmartStudy AI",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — dark theme, hide all Streamlit chrome
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global Styles (Full Page Look) ── */
html, body, [data-testid="stApp"], .stApp, .main, [data-testid="stAppViewContainer"] {
    background: var(--bg-gradient) !important;
    background-attachment: fixed !important;
    color: #ffffff !important;
    min-height: 100vh !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow-x: hidden !important;
}

.block-container, section {
    background: transparent !important;
    max-width: 100% !important;
}

/* Remove extra white sections */
section[data-testid="stSidebar"] {
    background: #0f172a !important;
}

/* ── Floating Particles ── */
.particles-container {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1;
    overflow: hidden;
}
.particle {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    animation: float 20s infinite linear;
}
@keyframes float {
    from { transform: translateY(100vh) rotate(0deg); }
    to { transform: translateY(-10vh) rotate(360deg); }
}

.block-container {
    padding-top: 5rem !important; /* Space for the 75px navbar */
    padding-left: 5% !important;
    padding-right: 5% !important;
    max-width: 1500px !important;
    margin: 0 auto !important;
    animation: mainFadeIn 0.8s ease-out;
}

@keyframes mainFadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Typography ── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
}

/* ── Navbar Layout ── */
div[data-testid="stHorizontalBlock"] {
    align-items: center !important;
}

/* ── Quick Action Cards Styling ── */
div[data-testid="stColumn"] div[data-testid="stButton"] > button {
    height: 100px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    white-space: pre-wrap !important;
    line-height: 1.4 !important;
    font-size: 1rem !important;
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* ── Hide Chrome ── */
[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }

/* ── Animations ── */
.section-enter {
    animation: elegantFadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes elegantFadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Custom Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
</style>

<div class="particles-container">
    <div class="particle" style="width:2px; height:2px; left:10%; animation-duration:15s;"></div>
    <div class="particle" style="width:3px; height:3px; left:25%; animation-duration:22s; animation-delay:2s;"></div>
    <div class="particle" style="width:1px; height:1px; left:45%; animation-duration:18s; animation-delay:5s;"></div>
    <div class="particle" style="width:4px; height:4px; left:70%; animation-duration:25s; animation-delay:1s;"></div>
    <div class="particle" style="width:2px; height:2px; left:85%; animation-duration:20s; animation-delay:3s;"></div>
</div>
""", unsafe_allow_html=True)

def _ss(key, default):
    """Shorthand to set session state if not already present."""
    if key not in st.session_state:
        st.session_state[key] = default

def init_session_state():
    """Initializes all necessary session state variables."""

    _ss("token",          None)
    _ss("active_page",    "Home")
    _ss("auth_mode",      "login")
    _ss("language",       "en")
    _ss("user_data",      {})
    _ss("user_initials",  "JD")
    _ss("user_name",      "User")
    _ss("pomodoro_time",   25 * 60)
    _ss("pomodoro_running", False)
    _ss("pomodoro_break",   False)
    _ss("focus_mode",       False)
    _ss("messages",         [])
    
    # Force dark theme
    st.session_state.theme = "dark"

init_session_state()

# ══════════════════════════════════════════════════════════════════════════════
# NAV CALLBACKS — update active_page WITHOUT page reload
# ══════════════════════════════════════════════════════════════════════════════
def _nav(page: str):
    st.session_state.active_page = page
    # exit focus mode if leaving that section
    if page != "Focus Mode":
        st.session_state.focus_mode = False
        st.session_state.pomodoro_running = False
    st.rerun()

def _logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.query_params.clear()  # Clear persistent login
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# NAVBAR — renders as HTML+CSS; 5 invisible st.buttons drive session_state
# ══════════════════════════════════════════════════════════════════════════════
def render_navbar():
    """
    Renders a clean horizontal navigation menu using native Streamlit columns and buttons.
    Styles them to look like a premium navbar.
    """
    # ── Navbar Styling ────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .nav-container {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 75px;
        background: rgba(10, 15, 28, 0.7);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        z-index: 10000;
        display: flex;
        align-items: center;
        padding: 0 5%;
    }
    
    .nav-anchor + div[data-testid="stHorizontalBlock"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 10001 !important;
        padding: 0 5% !important;
        height: 75px !important;
        display: flex !important;
        align-items: center !important;
        background: transparent !important;
    }

    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: transparent !important;
        border: none !important;
        color: rgba(255, 255, 255, 0.6) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        height: auto !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        color: #fff !important;
        background: rgba(255, 255, 255, 0.08) !important;
        transform: translateY(-1px);
    }

    .nav-active-btn::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 20%;
        width: 60%;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: 10px;
        box-shadow: 0 0 15px var(--primary-glow);
    }
    
    .logo-text {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.4rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Render Navbar ─────────────────────────────────────────────────────────
    st.markdown('<div class="nav-container"></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-anchor"></div>', unsafe_allow_html=True)
    
    # Using columns to create a horizontal layout
    cols = st.columns([1.5, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 0.5, 0.5])
    
    # 1. Logo
    with cols[0]:
        if st.button("📚 SmartStudy", key="nav_logo_btn"):
            _nav("Home")
    
    # 2. Nav Items
    pages = ["Home", "Planner", "Tracker", "Pomodoro", "Focus", "Profile"]
    page_map = {
        "Home": "Home", "Planner": "Study Planner", "Tracker": "Study Tracker",
        "Pomodoro": "Pomodoro", "Focus": "Focus Mode", "Profile": "Profile"
    }
    
    for i, page_label in enumerate(pages):
        with cols[i+1]:
            full_page_name = page_map[page_label]
            is_active = st.session_state.active_page == full_page_name
            btn_key = f"nav_{page_label.lower()}"
            
            if is_active:
                st.markdown(f'<div class="nav-active-btn" style="position:relative;">', unsafe_allow_html=True)
            else:
                st.markdown('<div>', unsafe_allow_html=True)
            
            if st.button(page_label, key=btn_key, use_container_width=True):
                _nav(full_page_name)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Right side icons
    with cols[8]:
        st.markdown(f"""
        <div style="width:36px; height:36px; border-radius:50%; 
                    background:var(--primary-gradient); 
                    box-shadow: 0 0 10px var(--primary-glow);
                    display:flex; align-items:center; justify-content:center; 
                    font-size:0.85rem; font-weight:800; color:#fff; cursor:pointer;
                    margin-top: 10px;">
            {st.session_state.user_initials}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _section_header(title: str, subtitle: str = ""):
    """Single styled heading + optional subtitle. Used once per page section."""
    sub_html = (
        f'<p style="font-family:\'Poppins\',sans-serif;color:rgba(148,163,184,.6);'
        f'font-size:.85rem;margin:.3rem 0 0;font-weight:400;">{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(f"""
<div class="section-enter" style="margin-bottom:1.75rem;">
    <h1 style="font-family:'Poppins',sans-serif;
               font-size:clamp(1.5rem,2.8vw,2.1rem);
               font-weight:700;
               background:linear-gradient(125deg,#a78bfa 0%,#818cf8 40%,#38bdf8 100%);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;margin:0;line-height:1.2;">{title}</h1>
    {sub_html}
</div>""", unsafe_allow_html=True)

def _sub_label(text: str):
    """Lightweight section divider label — replaces st.subheader() everywhere."""
    st.markdown(
        f'<p style="font-family:\'Poppins\',sans-serif;font-size:.78rem;font-weight:600;'
        f'letter-spacing:.8px;text-transform:uppercase;color:rgba(148,163,184,.5);'
        f'margin:1.875rem 0 1rem;">{text}</p>',
        unsafe_allow_html=True,
    )

def _glass_card_start():
    st.markdown('<div class="glass-card section-enter">', unsafe_allow_html=True)

def _glass_card_end():
    st.markdown('</div>', unsafe_allow_html=True)

def _get_daily_quote():
    quotes = [
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("Education is the passport to the future.", "Malcolm X"),
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("The harder you work, the greater you'll feel when you achieve it.", "Unknown"),
        ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
        ("Learning is the only thing the mind never exhausts.", "Leonardo da Vinci"),
    ]
    random.seed(int(datetime.now().strftime("%Y%m%d")))
    return random.choice(quotes)


# ══════════════════════════════════════════════════════════════════════════════
# RENDER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

# ── HOME ─────────────────────────────────────────────────────────────────────
def render_home():
    name  = st.session_state.user_name.split()[0]
    token = st.session_state.token
    hour  = datetime.now().hour
    
    if   5  <= hour < 12: greeting = "Good morning"
    elif 12 <= hour < 17: greeting = "Good afternoon"
    elif 17 <= hour < 21: greeting = "Good evening"
    else:                  greeting = "Good night"

    # 1️⃣ GREETING & HERO
    stats_res = get_user_stats(token)
    streak, xp, level = 0, 0, 1
    if stats_res.status_code == 200:
        sdata = stats_res.json()
        streak = sdata.get('streak', 0)
        xp = sdata.get('total_xp', 0)
        level = sdata.get('level', 1)

    streak_msg = f"🔥 {streak} day streak — keep going!" if streak > 0 else "🚀 Start your journey today!"

    st.markdown(f"""
    <div class="section-enter" style="margin-bottom:3rem; position:relative;">
        <div style="position:absolute; top:-50px; left:-50px; width:150px; height:150px; 
                    background:var(--primary); filter:blur(100px); opacity:0.15; z-index:-1;"></div>
        <p style="font-family:'Outfit',sans-serif; font-size:0.9rem; font-weight:600; 
                  letter-spacing:3px; color:rgba(255,255,255,0.4); margin-bottom:0.4rem; text-transform:uppercase;">
            {greeting}, <span style="color:#fff; font-weight:800;">{name}</span>
        </p>
        <h1 style="margin:0; font-size:3.5rem; line-height:1.1; font-weight:800; 
                   background:linear-gradient(135deg, #fff 0%, #a78bfa 100%);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            {streak_msg}
        </h1>
        <p style="color:rgba(148,163,184,0.6); font-size:1.2rem; margin-top:0.8rem; max-width:600px;">
            Elevate your learning experience. Your AI study companion is optimized and ready.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2️⃣ QUICK ACTIONS (Premium Grid)
    _sub_label("Quick Actions")
    qa_cols = st.columns(4)
    actions = [
        ("⏲", "Pomodoro", "qa_pomo", "Pomodoro"),
        ("📅", "Planner", "qa_plan", "Study Planner"),
        ("📝", "Tasks", "qa_track", "Study Tracker"),
        ("🧠", "Focus", "qa_focus", "Focus Mode")
    ]
    for i, (icon, label, key, page) in enumerate(actions):
        with qa_cols[i]:
            if st.button(f"{icon} \n {label}", use_container_width=True, key=key): 
                _nav(page)

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

    # 3️⃣ STATS & PROGRESS
    col_l, col_r = st.columns([1.6, 1])
    
    with col_l:
        _sub_label("Level Progress")
        progress = min((xp % 1000) / 10.0, 100.0)
        st.markdown(f"""
        <div class="glass-card" style="padding:2rem; margin-bottom:0;">
            <div style="display:flex; justify-content:space-between; margin-bottom:1rem;">
                <div>
                    <p style="font-size:0.85rem; color:rgba(255,255,255,0.4); margin:0; text-transform:uppercase; letter-spacing:1px;">Rank</p>
                    <p style="font-size:1.5rem; font-weight:800; color:var(--accent); margin:0;">Level {level}</p>
                </div>
                <div style="text-align:right;">
                    <p style="font-size:0.85rem; color:rgba(255,255,255,0.4); margin:0; text-transform:uppercase; letter-spacing:1px;">Experience</p>
                    <p style="font-size:1.5rem; font-weight:800; color:#fff; margin:0;">{xp % 1000} <span style="font-size:0.9rem; opacity:0.5;">/ 1000</span></p>
                </div>
            </div>
            <div style="width:100%; height:12px; background:rgba(255,255,255,0.05); border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.05);">
                <div style="width:{progress}%; height:100%; background:var(--primary-gradient); 
                            box-shadow:0 0 20px var(--primary-glow); border-radius:20px; transition: width 1s ease-in-out;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        _sub_label("Current Streak")
        st.markdown(f"""
        <div class="glass-card" style="padding:2rem; text-align:center; height:155px; display:flex; flex-direction:column; justify-content:center;">
            <p style="font-size:3rem; margin:0;">🔥</p>
            <p style="font-size:2.2rem; font-weight:900; margin:0; line-height:1;">{streak} <span style="font-size:1.1rem; font-weight:500; opacity:0.6;">Days</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:2.5rem'></div>", unsafe_allow_html=True)

    # 4️⃣ MOTIVATIONAL QUOTE
    quote, author = _get_daily_quote()
    st.markdown(f"""
    <div class="glass-card section-enter" style="border-left: 4px solid var(--primary); background:rgba(99,102,241,0.03);">
        <p class="motivational-quote" style="text-align:left; padding:0; margin:0; border:none; font-size:1.1rem;">“{quote}”
            <span style="display:block; margin-top:0.75rem; font-weight:500; font-size:0.85rem; color:rgba(148,163,184,0.6);">
                — {author}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)




# ── STUDY PLANNER ─────────────────────────────────────────────────────────────
def render_planner():
    _section_header("Study Planner", "Build your personalised AI study schedule")

    token = st.session_state.token
    res   = get_my_plans(token)
    if res.status_code != 200:
        st.error("Failed to load study plans. Please check your connection.")
        return

    data                = res.json()
    plans               = data.get("plans", [])
    schedule            = data.get("schedule", [])
    progress_percentage = data.get("progress_percentage", 0.0)

    col1, col2 = st.columns([1, 2])

    with col1:
        _sub_label("Add Subject")
        with st.form("create_plan_form"):
            subject     = st.text_input("Subject Name", placeholder="e.g. Mathematics")
            exam_date   = st.date_input("Exam Date", min_value=date.today())
            daily_hours = st.number_input(
                "Daily Available Hours", min_value=0.5, value=4.0, step=0.5,
                help="Distributed proportionally across subjects."
            )
            is_weak   = st.checkbox("Weak subject (+40% time)")
            submitted = st.form_submit_button("Add to Schedule", use_container_width=True)

            if submitted:
                if not subject:
                    st.error("Please enter a subject name.")
                else:
                    resp = create_study_plan(token, subject, exam_date, daily_hours, is_weak)
                    if resp.status_code == 200:
                        st.success("Added!")
                        st.rerun()
                    else:
                        st.error("Failed to add plan.")

    with col2:
        _sub_label(f"Overall Progress — {progress_percentage:.1f}%")
        st.progress(progress_percentage / 100.0)

        _sub_label("Your Subjects")
        if not plans:
            st.info("No subjects yet. Add one from the left panel.")
        else:
            for p in plans:
                is_checked      = p["is_completed"]
                c1, c2, c3, c4 = st.columns([0.1, 0.5, 0.3, 0.1])

                checked = c1.checkbox(
                    "Done", value=is_checked,
                    key=f"plan_chk_{p['id']}", label_visibility="collapsed"
                )
                if checked != is_checked:
                    toggle_complete(token, p["id"])
                    st.rerun()

                c2.write(f"**{p['subject']}** {'_(Weak)_' if p['is_weak_subject'] else ''}")
                c3.write(f"Exam: {p['exam_date']}")
                if c4.button("Del", key=f"plan_del_{p['id']}", use_container_width=True):
                    delete_study_plan(token, p["id"])
                    st.rerun()

    _sub_label("Generated Daily Timetable")
    if schedule:
        df         = pd.DataFrame(schedule)
        df.columns = ["Start Time", "End Time", "Task"]

        def _color(val):
            if val == "Break":          return "background-color:#2e7d32"
            if val == "Daily Revision": return "background-color:#1565c0"
            return ""

        st.table(df.style.map(_color, subset=["Task"]))
    else:
        st.info("Add active subjects to see your timetable.")



# ── STUDY TRACKER ─────────────────────────────────────────────────────────────
def render_tracker():
    _section_header("Study Tracker", "Log sessions and visualise your progress")

    token = st.session_state.token

    with st.expander("+ Add New Task", expanded=False):
        with st.form("new_task_form"):
            c1, c2, c3 = st.columns(3)
            with c1: subject  = st.text_input("Subject")
            with c2: topic    = st.text_input("Topic")
            with c3: duration = st.number_input("Duration (min)", min_value=10, value=60, step=10)

            if st.form_submit_button("Add Task", use_container_width=True):
                if subject and topic:
                    if create_task(token, subject, topic, duration):
                        st.success("Task added!")
                        st.rerun()
                else:
                    st.error("Subject and Topic are required.")

    _sub_label("Your Tasks")
    tasks = get_tasks(token)

    if not tasks:
        st.info("No tasks yet. Create your first one above.")
    else:
        for task in tasks:
            is_done = task["is_completed"]
            opacity = "0.55" if is_done else "1"
            st.markdown(
                f'<div style="padding:.7rem 1rem;border-radius:12px;'
                f'background:rgba(99,102,241,.05);margin:.35rem 0;'
                f'border:1px solid rgba(255,255,255,.05);opacity:{opacity};'
                f'transition:opacity .3s;">',
                unsafe_allow_html=True,
            )
            col1, col2, col3, col4 = st.columns([0.5, 3, 1, 1])

            with col1:
                checked = st.checkbox(
                    "", value=is_done,
                    key=f"task_chk_{task['id']}", label_visibility="collapsed"
                )
                if checked != is_done:
                    toggle_task(token, task["id"])
                    st.rerun()

            with col2:
                label = f"~~**{task['subject']}** — {task['topic']}~~" if is_done \
                        else f"**{task['subject']}** — {task['topic']}"
                st.markdown(label)
                st.caption(f"⏱ {task['duration_minutes']} min")

            with col3:
                st.caption(task["date"][:10])

            with col4:
                if st.button("Delete", key=f"task_del_{task['id']}", use_container_width=True):
                    delete_task(token, task["id"])
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)



# ── POMODORO ─────────────────────────────────────────────────────────────────
def render_pomodoro():
    _section_header("Pomodoro Timer", "Stay focused with timed deep-work sessions")

    _ss("pomodoro_time",    25 * 60)
    _ss("pomodoro_running", False)
    _ss("pomodoro_break",   False)

    mode_col, _ = st.columns([2, 1])
    with mode_col:
        mode = st.radio(
            "Session Mode",
            ["Focus (25 min)", "Short Break (5 min)", "Long Break (15 min)"],
            horizontal=True,
        )

    duration_map = {"Focus (25 min)": 25, "Short Break (5 min)": 5, "Long Break (15 min)": 15}
    total_secs   = duration_map[mode] * 60

    minutes = st.session_state.pomodoro_time // 60
    seconds = st.session_state.pomodoro_time % 60
    mode_label = "Break Time" if st.session_state.pomodoro_break else "Focus Mode"

    _, tc, _ = st.columns([1, 2, 1])
    with tc:
        st.markdown(f"""
<div class="section-enter" style="text-align:center;padding:2.5rem 0;">
    <p style="font-family:'Poppins',sans-serif;color:rgba(255,255,255,.55);
              font-size:1rem;letter-spacing:1px;text-transform:uppercase;margin:0 0 .5rem;">{mode_label}</p>
    <div style="font-family:'Poppins',sans-serif;font-size:7rem;font-weight:700;line-height:1;
                background:linear-gradient(135deg,#6366f1,#8b5cf6,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;">{minutes:02d}:{seconds:02d}</div>
</div>""", unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        if b1.button("Start",  use_container_width=True, key="pomo_start"):
            st.session_state.pomodoro_running = True
            st.session_state.pomodoro_time    = total_secs
            st.rerun()
        if b2.button("Pause",  use_container_width=True, key="pomo_pause"):
            st.session_state.pomodoro_running = False
        if b3.button("Reset",  use_container_width=True, key="pomo_reset"):
            st.session_state.pomodoro_time    = total_secs
            st.session_state.pomodoro_running = False
            st.session_state.pomodoro_break   = False
            st.rerun()

    if st.session_state.pomodoro_running and st.session_state.pomodoro_time > 0:
        time.sleep(1)
        st.session_state.pomodoro_time -= 1
        st.rerun()
    elif st.session_state.pomodoro_time == 0:
        if not st.session_state.pomodoro_break:
            st.session_state.pomodoro_break = True
            st.session_state.pomodoro_time  = 5 * 60
            st.success("Focus session complete! Time for a break.")
        else:
            st.session_state.pomodoro_break   = False
            st.session_state.pomodoro_time    = 25 * 60
            st.session_state.pomodoro_running = False
            st.success("Break over! Ready for another focus session.")
        st.rerun()


# ── FOCUS MODE ────────────────────────────────────────────────────────────────
def render_focus_mode():
    # Ensure focus mode state is set correctly
    if "pomodoro_time" not in st.session_state:
        st.session_state.pomodoro_time = 25 * 60
    
    st.session_state.pomodoro_running = True
    st.session_state.pomodoro_break = False

    minutes  = st.session_state.pomodoro_time // 60
    seconds  = st.session_state.pomodoro_time % 60
    time_str = f"{minutes:02d}:{seconds:02d}"
    mode_text = t("focus_mode_title") if not st.session_state.pomodoro_break else t("break_time")

    st.markdown(f"""
<style>
.focus-overlay {{
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: #04050f;
    z-index: 888888;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0;
}}
.focus-time {{
    font-family: 'Poppins', sans-serif;
    font-size: clamp(6rem, 15vw, 11rem);
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
    animation: timePulse 2s ease-in-out infinite;
}}
@keyframes timePulse {{
    0%, 100% {{ opacity: 1; }} 50% {{ opacity: .85; }}
}}
.focus-label {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,.45);
    margin-bottom: 1rem;
}}
.focus-exit {{
    margin-top: 3rem;
    padding: .8rem 2.5rem;
    border-radius: 50px;
    background: rgba(99,102,241,.2);
    border: 1px solid rgba(129,140,248,.3);
    color: rgba(255,255,255,.75);
    font-family: 'Poppins', sans-serif;
    font-size: .9rem;
    font-weight: 600;
    cursor: pointer;
    transition: all .25s ease;
}}
.focus-exit:hover {{
    background: rgba(99,102,241,.35);
    color: #fff;
    transform: scale(1.03);
}}
</style>
<div class="focus-overlay">
    <div class="focus-label">{mode_text}</div>
    <div class="focus-time">{time_str}</div>
    <p style="color:rgba(255,255,255,0.3); font-size:0.8rem; margin-top:2rem;">Use the top menu to exit</p>
</div>
""", unsafe_allow_html=True)

    if st.session_state.pomodoro_running and st.session_state.pomodoro_time > 0:
        time.sleep(1)
        st.session_state.pomodoro_time -= 1
        st.rerun()
    elif st.session_state.pomodoro_time == 0:
        if not st.session_state.pomodoro_break:
            st.session_state.pomodoro_break = True
            st.session_state.pomodoro_time  = 5 * 60
        else:
            st.session_state.pomodoro_break   = False
            st.session_state.pomodoro_time    = 25 * 60
            st.session_state.pomodoro_running = False
        st.rerun()


# ── PROFILE ───────────────────────────────────────────────────────────────────
def render_profile():
    _section_header("My Profile", "Your study stats and account settings")

    token = st.session_state.token
    user  = st.session_state.user_data
    name  = user.get("full_name") or user.get("email", "User")
    email = user.get("email", "—")
    initials = st.session_state.user_initials

    stats_res = get_user_stats(token)
    stats     = stats_res.json() if stats_res.status_code == 200 else {}

    pc1, pc2 = st.columns([1, 2])
    with pc1:
        st.markdown(f"""
<div class="glass-card section-enter" style="text-align:center;">
    <div style="width:90px;height:90px;border-radius:50%;margin:0 auto 1rem;
                background:linear-gradient(135deg,#6366f1,#8b5cf6,#a78bfa);
                display:flex;align-items:center;justify-content:center;
                font-family:'Poppins',sans-serif;font-size:2rem;font-weight:700;color:#fff;
                box-shadow:0 0 28px rgba(99,102,241,.45);">
        {initials}
    </div>
    <h3 style="margin:0 0 .3rem;">{name}</h3>
    <p style="color:rgba(148,163,184,.75);font-size:.85rem;margin:0;">{email}</p>
</div>""", unsafe_allow_html=True)

    with pc2:
        s1, s2, s3 = st.columns(3)
        s1.metric("Total XP",      stats.get("total_xp", 0))
        s2.metric("Level",         stats.get("level",    1))
        s3.metric("Streak",        f"{stats.get('streak', 0)}d")

        st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
        s4, s5 = st.columns(2)
        s4.metric("Tasks Completed", stats.get("tasks_completed", 0))
        s5.metric("Plans Created",   stats.get("plans_created",   0))

    # Danger zone
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    with st.expander("Account Actions"):
        if st.button("Sign Out", key="profile_logout_btn"):
            _logout()


# ══════════════════════════════════════════════════════════════════════════════
# AUTH — Login / Sign-up (shown when not logged in)
# ══════════════════════════════════════════════════════════════════════════════
def render_auth():
    import base64, re
    from api_client import signup_user, login_user

    def _b64(path):
        try:
            if os.path.exists(path):
                return base64.b64encode(open(path,"rb").read()).decode()
        except Exception: pass
        return ""

    def _pw_score(pw):
        s = 0
        if len(pw) >= 8:              s += 1
        if re.search(r"[A-Z]", pw):   s += 1
        if re.search(r"[0-9]", pw):   s += 1
        if re.search(r"[!@#$%^&*]",pw): s += 1
        return s

    ILLUS = os.path.join(os.path.dirname(__file__), "assets", "premium_study_illustration.png")
    b64   = _b64(ILLUS)
    illus_html = (
        f'<img src="data:image/png;base64,{b64}" class="illus-img" alt="SmartStudy AI"/>'
        if b64 else '<div class="illus-img illus-fallback"></div>'
    )

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-deep: #05070a;
    --bg-accent: #0f172a;
    --glass-bg: rgba(15, 23, 42, 0.65);
    --glass-border: rgba(255, 255, 255, 0.08);
    --accent-primary: #6366f1;
    --accent-secondary: #a78bfa;
    --text-main: #f8fafc;
    --text-dim: #94a3b8;
}

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #1e1b4b 0%, #05070a 45%, #000 100%) !important;
    background-attachment: fixed !important;
    color: var(--text-main) !important;
    font-family: 'Inter', sans-serif !important;
}

.main .block-container {
    max-width: 1200px !important;
    padding: 1rem 2rem 2rem !important;
}

/* Elegant Typography */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(135deg, #fff 30%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Premium Glassmorphism */
.glass-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 24px !important;
    padding: 2rem !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.3) !important;
    transform: translateY(-4px) !important;
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.1) !important;
}

/* Animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.section-enter {
    animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Hide scrollbars but keep functionality */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }

[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHorizontalBlock"] {
    height:100vh !important; padding:0 !important; gap:0 !important; align-items:center;
}
[data-testid="stHorizontalBlock"]>[data-testid="column"]:nth-of-type(1) {
    display:flex !important; flex-direction:column !important;
    justify-content:center !important; align-items:center !important;
    padding:2.5rem !important; background:#000 !important; height:100vh !important;
}
[data-testid="stHorizontalBlock"]>[data-testid="column"]:nth-of-type(2) {
    display:flex !important; flex-direction:column !important;
    justify-content:center !important; align-items:center !important;
    padding:0 6% !important; background:#000 !important;
    height:100vh !important; overflow-y:auto;
}
.brand-logo { font-size:3rem; font-weight:800; color:#fff; margin-bottom:2.5rem; text-align:center; }
.brand-logo .accent { background:linear-gradient(135deg,#1e40af,#3b82f6,#60a5fa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.illus-img { width:70%; max-width:300px; border-radius:20px;
    animation:floatHQ 6s ease-in-out infinite alternate;
    box-shadow:0 30px 70px rgba(0,0,0,.6); }
.illus-fallback { width:240px; height:240px; border-radius:50%;
    background:radial-gradient(circle,rgba(30,64,175,.15) 0%,transparent 70%); }
@keyframes floatHQ {
    0%   { transform:translateY(0);    box-shadow:0 20px 40px rgba(0,0,0,.5); }
    100% { transform:translateY(-18px);box-shadow:0 40px 60px rgba(0,0,0,.3); }
}
[data-testid="stForm"] {
    background:rgba(255,255,255,.05) !important;
    border:1px solid rgba(255,255,255,.08) !important;
    backdrop-filter:blur(20px) !important;
    border-radius:18px !important; padding:40px !important;
    box-shadow:0 24px 60px rgba(0,0,0,.5) !important;
    animation:fadeScaleUp .55s cubic-bezier(.16,1,.3,1) forwards;
    width:100%; max-width:430px; margin:0 auto;
}
.auth-heading { font-size:2.1rem; font-weight:700; color:#fff; margin-bottom:.4rem; line-height:1.2; }
.auth-subtext  { font-size:1rem; color:rgba(255,255,255,.65); margin-bottom:0; }
.stTextInput>label,[data-testid="stTextInput"]>label {
    color:rgba(255,255,255,.75) !important; font-size:13px !important; font-weight:500 !important; }
.stTextInput>div>div>input,[data-testid="stTextInput"] input {
    background:#111 !important; color:#fff !important;
    border:1px solid rgba(255,255,255,.15) !important; border-radius:12px !important;
    padding:15px 16px !important; font-size:14px !important; }
.stTextInput>div>div>input:focus,[data-testid="stTextInput"] input:focus {
    border-color:rgba(59,130,246,.7) !important;
    box-shadow:0 0 0 3px rgba(59,130,246,.18) !important; outline:none !important; }
[data-testid="stFormSubmitButton"]>button {
    background:linear-gradient(135deg,#1e3a8a,#1e40af,#1d4ed8) !important;
    color:#fff !important; border-radius:12px !important; padding:15px !important;
    font-weight:600 !important; font-size:15px !important; border:none !important;
    width:100% !important; transition:transform .25s ease,box-shadow .25s ease !important;
    box-shadow:0 6px 20px rgba(29,78,216,.35) !important; }
[data-testid="stFormSubmitButton"]>button:hover {
    transform:translateY(-3px) !important; box-shadow:0 12px 30px rgba(29,78,216,.5) !important; }
.stButton>button {
    background:rgba(255,255,255,.05) !important; color:rgba(255,255,255,.7) !important;
    border:1px solid rgba(255,255,255,.1) !important; border-radius:10px !important;
    font-weight:600 !important; padding:10px !important; width:100% !important;
    transition:all .25s ease !important; }
.stButton>button:hover {
    background:rgba(59,130,246,.12) !important; border-color:rgba(59,130,246,.4) !important;
    color:#60a5fa !important; transform:translateY(-1px) !important; }
@keyframes fadeScaleUp { from{opacity:0;transform:scale(.96) translateY(16px)} to{opacity:1;transform:scale(1) translateY(0)} }
[data-testid="stSidebar"] { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
</style>""", unsafe_allow_html=True)

    lc, rc = st.columns([1.1, 1])

    with lc:
        st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;width:100%;">
    <div class="brand-logo">SmartStudy<span class="accent">AI</span></div>
    <div style="position:relative;z-index:10;display:flex;justify-content:center;">
        {illus_html}
    </div>
    <p style="margin-top:2rem;color:rgba(255,255,255,.4);font-family:'Poppins',sans-serif;
              font-size:.85rem;text-align:center;">Your AI-powered study companion</p>
</div>""", unsafe_allow_html=True)

    with rc:
        st.markdown('<div style="max-width:430px;margin:0 auto;width:100%;position:relative;z-index:10;">', unsafe_allow_html=True)

        mode = st.session_state.auth_mode
        if mode == "login":
            st.markdown('<div class="auth-heading">Welcome Back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtext">Sign in to continue your learning journey</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="auth-heading">Create Account</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtext">Start your smart study experience today</div>', unsafe_allow_html=True)

        st.markdown('<div style="max-width:240px;margin:.8rem 0 1rem;">', unsafe_allow_html=True)
        tc1, tc2 = st.columns(2)
        with tc1:
            if st.button("Login",   use_container_width=True, key="btn_to_login"):
                st.session_state.auth_mode = "login"; st.rerun()
        with tc2:
            if st.button("Sign Up", use_container_width=True, key="btn_to_signup"):
                st.session_state.auth_mode = "signup"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if mode == "login":
            with st.form("login_form", clear_on_submit=False):
                email_in = st.text_input("Email",    placeholder="you@example.com")
                pass_in  = st.text_input("Password", type="password", placeholder="Enter your password")
                st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Log In →", use_container_width=True)
                if submitted:
                    if not email_in or not pass_in:
                        st.error("Please fill in all fields.")
                    else:
                        with st.spinner("Authenticating…"):
                            res = login_user(email_in, pass_in)
                            if res.status_code == 200:
                                data = res.json()
                                token = data.get("access_token")
                                st.session_state.token = token
                                st.query_params["token"] = token  # Persist for refresh
                                st.rerun()
                            else:
                                st.error(res.json().get("detail", "Invalid credentials."))
        else:
            with st.form("signup_form", clear_on_submit=False):
                name_in  = st.text_input("Full Name", placeholder="Jane Doe")
                email_in = st.text_input("Email",     placeholder="you@example.com")
                pass_in  = st.text_input("Password",  type="password", placeholder="Minimum 6 characters")
                st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Create Account →", use_container_width=True)
                if submitted:
                    if not name_in or not email_in or not pass_in:
                        st.error("Please fill in all fields.")
                    elif _pw_score(pass_in) < 2:
                        st.error("Weak password. Add uppercase letters and numbers.")
                    elif len(pass_in) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        with st.spinner("Creating account…"):
                            res = signup_user(email_in, name_in, pass_in)
                            if res.status_code in [200, 201]:
                                st.success("Account created! Please log in.")
                                st.session_state.auth_mode = "login"
                                st.rerun()
                            else:
                                st.error(res.json().get("detail", "Sign-up failed."))

        # Google OAuth
        st.markdown("""
<div style="display:flex;align-items:center;gap:14px;margin:22px 0 14px;">
    <div style="flex:1;height:1px;background:rgba(255,255,255,.1);"></div>
    <span style="font-size:11px;color:rgba(255,255,255,.4);letter-spacing:1px;
                 text-transform:uppercase;">Or continue with</span>
    <div style="flex:1;height:1px;background:rgba(255,255,255,.1);"></div>
</div>
<a href="http://127.0.0.1:8042/auth/google/login"
   style="display:flex;align-items:center;justify-content:center;gap:12px;
          background:rgba(255,255,255,.07);color:#fff;font-weight:600;font-size:14px;
          text-decoration:none;padding:14px 24px;border-radius:12px;
          border:1px solid rgba(255,255,255,.12);transition:all .25s ease;
          width:100%;margin-top:6px;">
    <svg viewBox="0 0 24 24" width="20" height="20">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
    </svg>
    Continue with Google
</a>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN — entry point
# ══════════════════════════════════════════════════════════════════════════════
def main():
    # ── Ensure Session State is Initialized ──────────────────────────────────
    init_session_state()
    # ── Restore Token from URL (Persistent Login) ──────────────────────────
    if "token" in st.query_params:
        st.session_state.token = st.query_params["token"]
        # We DON'T clear it now to keep it persistent on refresh
        try:
            res = get_me(st.session_state.token)
            if res.status_code == 200:
                ud = res.json()
                st.session_state.user_data = ud
                name = ud.get("full_name") or ud.get("email","User").split("@")[0]
                st.session_state.user_name = name
                if ud.get("full_name"):
                    st.session_state.user_initials = "".join(p[0].upper() for p in name.split() if p)[:2]
                else:
                    email = ud.get("email","JD")
                    st.session_state.user_initials = "".join(p[0].upper() for p in email.split("@")[0].split(".") if p)[:2]
        except Exception:
            pass

    # ── Logout via query param ───────────────────────────────────────────────
    if "logout" in st.query_params:
        st.query_params.clear()
        _logout()

    # ── Not authenticated — show auth page ───────────────────────────────────
    if not st.session_state.token:
        inject_custom_css()
        render_auth()
        return

    # ── Fetch user profile once per session ──────────────────────────────────
    if not st.session_state.user_data:
        res = get_me(st.session_state.token)
        if res.status_code != 200:
            st.session_state.token = None
            st.rerun()
            return
        ud   = res.json()
        name = ud.get("full_name") or ud.get("email","User").split("@")[0]
        st.session_state.user_data    = ud
        st.session_state.user_name    = name
        if ud.get("full_name"):
            st.session_state.user_initials = "".join(p[0].upper() for p in name.split() if p)[:2]
        else:
            email = ud.get("email","JD")
            st.session_state.user_initials = "".join(p[0].upper() for p in email.split("@")[0].split(".") if p)[:2]

    # ── Inject base CSS ──────────────────────────────────────────────────────
    inject_custom_css()

    # ── Render navbar ────────────────────────────────────────────────────────
    render_navbar()

    # ── Content container ────────────────────────────────────────────────────
    active_page = st.session_state.active_page
    content_container = st.container()

    with content_container:
        if   active_page == "Home":          render_home()
        elif active_page == "Study Planner": render_planner()
        elif active_page == "Study Tracker": render_tracker()
        elif active_page == "Pomodoro":      render_pomodoro()
        elif active_page == "Focus Mode":    render_focus_mode()
        elif active_page == "Profile":       render_profile()
        else:                                render_home()


if __name__ == "__main__":
    main()
