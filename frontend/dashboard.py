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
/* ── Kill Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stHeader"],
[data-testid="stStatusWidget"], [data-testid="stBaseButton-header"],
[data-testid="collapsedControl"], section[data-testid="stSidebar"],
.stDeployButton { display:none!important; visibility:hidden!important; }

/* ── Dark radial background ── */
html, body, #root, .stApp,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] > section > div,
.main, main {
    background: radial-gradient(ellipse at top, #0f172a 0%, #020617 55%, #000 100%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
    margin: 0; padding: 0;
}
html { background: #000 !important; }

/* ── Block container — leave room for fixed navbar ── */
[data-testid="stAppViewContainer"] > section > div.block-container {
    padding-top: 88px !important;
    padding-left: 2.4rem !important;
    padding-right: 2.4rem !important;
    max-width: 100% !important;
}

/* ── Section fade-in transition ── */
.section-enter {
    animation: sectionFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes sectionFadeIn {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Hide hr dividers ── */
hr { display: none !important; }

/* ── Streamlit button resets inside navbar ── */
div[data-testid="stButton"] > button[data-testid^="nb_"] {
    all: unset !important;
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
def _ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

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
_ss("messages",         [])           # doubt chat history

# ── Force dark theme
st.session_state.theme = "dark"

# ══════════════════════════════════════════════════════════════════════════════
# NAV CALLBACKS — update active_page WITHOUT page reload
# ══════════════════════════════════════════════════════════════════════════════
def _nav(page: str):
    st.session_state.active_page = page
    # exit focus mode if leaving that section
    if page != "Focus Mode":
        st.session_state.focus_mode   = False
        st.session_state.pomodoro_running = False

def _logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# NAVBAR — renders as HTML+CSS; 5 invisible st.buttons drive session_state
# ══════════════════════════════════════════════════════════════════════════════
def render_navbar():
    ap      = st.session_state.active_page
    initials = st.session_state.user_initials

    pages = ["Home", "Study Planner", "Study Tracker", "Pomodoro", "Focus Mode"]

    # Build nav items HTML (purely visual — real clicks come from hidden buttons)
    items_html = ""
    for p in pages:
        active_cls = " nav-active" if ap == p else ""
        items_html += (
            f'<span class="nb-item{active_cls}" '
            f'onclick="document.getElementById(\'nb_btn_{p.replace(" ", "_")}\').click()">'
            f'{p}</span>'
        )

    st.markdown(f"""
<!-- SmartStudy AI Navbar -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.smartnav {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 66px;
    background: linear-gradient(180deg, rgba(5,7,18,.97) 0%, rgba(8,11,28,.95) 100%);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2.5rem;
    border-bottom: 1px solid rgba(99,102,241,.14);
    box-shadow:
        0 1px 0 rgba(255,255,255,.04) inset,
        0 8px 40px rgba(0,0,0,.65),
        0 1px 16px rgba(99,102,241,.09);
}}
.smartnav::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, #4f46e5 22%, #818cf8 45%,
        #a78bfa 55%, #818cf8 72%, #4f46e5 82%, transparent 100%);
    background-size: 250% 100%;
    animation: navShimmer 4s ease-in-out infinite;
    opacity: .75;
}}
@keyframes navShimmer {{
    0%   {{ background-position: -250% 0; }}
    100% {{ background-position:  250% 0; }}
}}
.nb-logo {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.22rem;
    font-weight: 700;
    letter-spacing: -.3px;
    background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    white-space: nowrap;
    flex-shrink: 0;
    cursor: pointer;
    user-select: none;
}}
.nb-menu {{
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: center;
    gap: .25rem;
    flex: 1;
    padding: 0 1.5rem;
}}
.nb-item {{
    font-family: 'Poppins', sans-serif;
    font-size: .855rem;
    font-weight: 600;
    color: rgba(255,255,255,.46);
    padding: .42rem 1.1rem;
    border-radius: 50px;
    white-space: nowrap;
    cursor: pointer;
    position: relative;
    user-select: none;
    transition:
        color      .3s ease,
        background .3s ease,
        box-shadow .3s ease,
        transform  .3s cubic-bezier(.34,1.56,.64,1);
}}
.nb-item:hover {{
    color: rgba(255,255,255,.9);
    background: rgba(99,102,241,.13);
    transform: translateY(-1px);
}}
.nb-item:active {{ transform: translateY(1px); transition-duration: .1s; }}
.nb-item.nav-active {{
    color: #fff;
    background: rgba(99,102,241,.22);
    box-shadow:
        0 0 0 1px rgba(129,140,248,.32),
        0 4px 18px rgba(99,102,241,.28),
        0 0 28px rgba(99,102,241,.13);
}}
.nb-item.nav-active::after {{
    content: '';
    position: absolute;
    bottom: -1px; left: 50%;
    transform: translateX(-50%);
    width: 58%; height: 2.5px;
    border-radius: 99px;
    background: linear-gradient(90deg, #6366f1, #a78bfa, #6366f1);
    background-size: 200% 100%;
    animation: activeGlow 2.2s ease-in-out infinite;
}}
@keyframes activeGlow {{
    0%   {{ background-position: 0%   50%; opacity: .88; }}
    50%  {{ background-position: 100% 50%; opacity: 1.00; }}
    100% {{ background-position: 0%   50%; opacity: .88; }}
}}
.nb-right {{
    display: flex;
    align-items: center;
    gap: .75rem;
    flex-shrink: 0;
}}
.nb-avatar {{
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 60%, #a78bfa 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-family: 'Poppins', sans-serif;
    font-weight: 700;
    font-size: .78rem;
    letter-spacing: .5px;
    cursor: pointer;
    box-shadow: 0 0 0 2px rgba(99,102,241,0);
    transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s ease;
    user-select: none;
}}
.nb-avatar:hover {{
    transform: scale(1.1);
    box-shadow: 0 0 0 2.5px rgba(129,140,248,.55), 0 0 22px rgba(99,102,241,.42);
}}
.nb-dropdown {{
    display: none;
    position: fixed;
    top: 70px; right: 2rem;
    background: linear-gradient(160deg, rgba(9,12,32,.98) 0%, rgba(13,17,44,.96) 100%);
    border: 1px solid rgba(129,140,248,.17);
    border-radius: 16px;
    min-width: 202px;
    padding: .5rem 0;
    box-shadow: 0 20px 60px rgba(0,0,0,.7), 0 0 0 1px rgba(255,255,255,.04) inset;
    backdrop-filter: blur(24px);
    z-index: 9999999;
}}
.nb-dropdown.open {{ display: block; animation: ddSlide .28s cubic-bezier(.16,1,.3,1) forwards; }}
@keyframes ddSlide {{
    from {{ opacity: 0; transform: translateY(-10px) scale(.96); }}
    to   {{ opacity: 1; transform: translateY(0)     scale(1);   }}
}}
.nb-dd-item {{
    display: block;
    padding: .68rem 1.25rem;
    font-family: 'Poppins', sans-serif;
    font-size: .84rem;
    font-weight: 500;
    color: rgba(255,255,255,.62);
    text-decoration: none;
    cursor: pointer;
    transition: background .25s ease, color .25s ease, padding-left .25s ease;
}}
.nb-dd-item:hover {{ background: rgba(99,102,241,.16); color: #fff; padding-left: 1.55rem; }}
.nb-dd-sep {{ height: 1px; background: rgba(255,255,255,.06); margin: .35rem .75rem; }}

/* ── Hidden Streamlit nav buttons ── */
div.nb-btn-row {{
    position: fixed;
    top: -9999px;
    left: -9999px;
    visibility: hidden;
    pointer-events: none;
    height: 0; width: 0; overflow: hidden;
}}

@media (max-width: 900px) {{
    .smartnav {{ padding: 0 1.2rem; }}
    .nb-item  {{ padding: .38rem .75rem; font-size: .8rem; }}
    .nb-logo  {{ font-size: 1.05rem; }}
    .nb-menu  {{ gap: .1rem; }}
}}
@media (max-width: 640px) {{
    .nb-logo  {{ display: none; }}
    .nb-item  {{ padding: .35rem .52rem; font-size: .71rem; }}
    .smartnav {{ height: 56px; }}
}}
</style>

<nav class="smartnav" role="navigation" aria-label="Main navigation">
    <span class="nb-logo"
          onclick="document.getElementById('nb_btn_Home').click()">
        SmartStudy<span style="font-weight:400;opacity:.7;">AI</span>
    </span>
    <div class="nb-menu" role="menubar">{items_html}</div>
    <div class="nb-right">
        <div class="nb-avatar" id="nbAvatar" onclick="nbDD()" role="button"
             aria-haspopup="true" aria-expanded="false">{initials}</div>
    </div>
</nav>

<div class="nb-dropdown" id="nbDropdown" role="menu">
    <span class="nb-dd-item"
          onclick="document.getElementById('nb_btn_Profile').click()">My Profile</span>
    <div class="nb-dd-sep"></div>
    <span class="nb-dd-item" onclick="document.getElementById('nb_btn_logout').click()">Sign Out</span>
</div>

<script>
function nbDD() {{
    var dd = document.getElementById('nbDropdown');
    var av = document.getElementById('nbAvatar');
    var open = dd.classList.toggle('open');
    av.setAttribute('aria-expanded', open ? 'true' : 'false');
}}
document.addEventListener('click', function(e) {{
    var dd = document.getElementById('nbDropdown');
    var av = document.getElementById('nbAvatar');
    if (dd && av && !av.contains(e.target) && !dd.contains(e.target))
        dd.classList.remove('open');
}});
</script>
""", unsafe_allow_html=True)

    # ── Invisible Streamlit buttons that actually change session_state ──────────
    st.markdown('<div class="nb-btn-row">', unsafe_allow_html=True)
    c = st.columns(7)
    with c[0]: st.button("Home",          key="nb_btn_Home",          on_click=_nav, args=("Home",))
    with c[1]: st.button("Study Planner", key="nb_btn_Study_Planner", on_click=_nav, args=("Study Planner",))
    with c[2]: st.button("Study Tracker", key="nb_btn_Study_Tracker", on_click=_nav, args=("Study Tracker",))
    with c[3]: st.button("Pomodoro",      key="nb_btn_Pomodoro",      on_click=_nav, args=("Pomodoro",))
    with c[4]: st.button("Focus Mode",    key="nb_btn_Focus_Mode",    on_click=_nav, args=("Focus Mode",))
    with c[5]: st.button("Profile",       key="nb_btn_Profile",       on_click=_nav, args=("Profile",))
    with c[6]: st.button("Logout",        key="nb_btn_logout",        on_click=_logout)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _section_header(title: str, subtitle: str = ""):
    """Single styled heading + optional subtitle. Used once per page section."""
    sub_html = (
        f'<p style="font-family:\'Poppins\',sans-serif;color:rgba(148,163,184,.8);'
        f'font-size:.9rem;margin:.3rem 0 0;font-weight:400;">{subtitle}</p>'
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
        f'letter-spacing:.8px;text-transform:uppercase;color:rgba(148,163,184,.6);'
        f'margin:1.4rem 0 .6rem;">{text}</p>',
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
    name = st.session_state.user_name
    hour = datetime.now().hour
    if   5  <= hour < 12: greeting = t("good_morning")
    elif 12 <= hour < 17: greeting = t("good_afternoon")
    elif 17 <= hour < 21: greeting = t("good_evening")
    else:                  greeting = t("good_night")

    # ── Single branded greeting (one heading, one subtitle) ────────────────
    _section_header(f"{greeting}, {name}!", "Your AI-powered study companion is ready.")

    # Stats row
    token     = st.session_state.token
    stats_res = get_user_stats(token)
    stats     = stats_res.json() if stats_res.status_code == 200 else {}

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total XP",      stats.get("total_xp",        0))
    s2.metric("Level",         stats.get("level",           1))
    s3.metric("Study Streak",  f"{stats.get('streak', 0)}d")
    s4.metric("Tasks Done",    stats.get("tasks_completed", 0))

    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    # ── Quick-action cards ─────────────────────────────────────────────────
    qa_items = [
        ("Study Planner", "📗", "Build your AI-powered schedule"),
        ("Study Tracker", "✅", "Log sessions and track progress"),
        ("Pomodoro",      "⏱",  "Timed deep-focus sessions"),
        ("Focus Mode",    "🎯", "Enter distraction-free zone"),
        ("Profile",       "👤", "Your stats and achievements"),
    ]

    st.markdown("""
<style>
.qa-grid {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:1rem;
    margin-bottom:2rem;
}
@media(max-width:1024px){ .qa-grid{ grid-template-columns:repeat(3,1fr); } }
@media(max-width:640px) { .qa-grid{ grid-template-columns:repeat(2,1fr); } }
.qa-card {
    background:rgba(13,18,48,.72);
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.07);
    border-radius:16px;
    padding:1.5rem 1rem 1.3rem;
    cursor:pointer;
    text-align:center;
    transition:
        transform 220ms cubic-bezier(.34,1.56,.64,1),
        box-shadow 220ms ease,
        border-color 220ms ease;
    animation:cardPop .5s cubic-bezier(.16,1,.3,1) both;
}
.qa-card:hover {
    transform:translateY(-5px) scale(1.04);
    box-shadow:0 8px 32px rgba(99,102,241,.3),0 0 0 1px rgba(99,102,241,.32);
    border-color:rgba(99,102,241,.4);
}
@keyframes cardPop {
    from { opacity:0; transform:translateY(22px) scale(.97); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
.qa-icon  { font-size:1.85rem; margin-bottom:.5rem; }
.qa-title {
    font-family:'Poppins',sans-serif;
    font-size:.88rem;
    font-weight:600;
    color:#f1f5f9;
    margin:.3rem 0 .25rem;
}
.qa-desc {
    font-family:'Poppins',sans-serif;
    font-size:.75rem;
    color:rgba(148,163,184,.75);
    margin:0;
    line-height:1.4;
}
</style>
""", unsafe_allow_html=True)

    cards_html = '<div class="qa-grid">'
    for label, icon, desc in qa_items:
        btn_id = f"nb_btn_{label.replace(' ', '_')}"
        cards_html += (
            f'<div class="qa-card" onclick="document.getElementById(\'{btn_id}\').click()">'
            f'<div class="qa-icon">{icon}</div>'
            f'<div class="qa-title">{label}</div>'
            f'<p class="qa-desc">{desc}</p></div>'
        )
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── Daily quote ────────────────────────────────────────────────────────
    quote, author = _get_daily_quote()
    st.markdown(f"""
<div class="glass-card section-enter">
    <p class="motivational-quote">“{quote}”
        <span style="display:block;text-align:right;margin-top:.75rem;
                     font-weight:500;font-style:normal;font-size:.85rem;
                     color:rgba(148,163,184,.75);">— {author}</span>
    </p>
</div>""", unsafe_allow_html=True)



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
    _ss("pomodoro_time",    25 * 60)
    _ss("pomodoro_running", True)
    _ss("pomodoro_break",   False)

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
    <button class="focus-exit"
            onclick="document.getElementById('nb_btn_Home').click()">
        Exit Focus Mode
    </button>
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

    ILLUS = os.path.join(os.path.dirname(__file__), "assets", "study_illustration.png")
    b64   = _b64(ILLUS)
    illus_html = (
        f'<img src="data:image/png;base64,{b64}" class="illus-img" alt="SmartStudy AI"/>'
        if b64 else '<div class="illus-img illus-fallback"></div>'
    )

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
html,body,.stApp,[data-testid="stApp"],[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"]>section,[data-testid="stAppViewContainer"]>section>div,
.main,main {
    background:radial-gradient(ellipse at top,#0f172a 0%,#020617 50%,#000 100%) !important;
    background-attachment:fixed !important;
    min-height:100vh; margin:0; padding:0;
}
html { background:#000 !important; }
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
                                st.session_state.token = data.get("access_token")
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
    # ── OAuth token from URL ─────────────────────────────────────────────────
    if "token" in st.query_params:
        st.session_state.token = st.query_params["token"]
        st.query_params.clear()
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
        st.rerun()

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
