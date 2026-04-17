import streamlit as st
<<<<<<< HEAD
import pandas as pd
from api_client import get_me, get_user_stats, create_study_plan, get_my_plans, delete_study_plan, toggle_complete
import sys
import random
import time
from datetime import datetime, timedelta, date
sys.path.append('C:\\Users\\Admin\\Desktop\\smartstudyAI\\smartstudyAI-main\\frontend')
from style_utils import inject_custom_css, add_language_selector, create_quick_action_button, create_navbar
from translations import t

st.set_page_config(page_title="SmartStudyAI – Dashboard", page_icon="📚", layout="wide")


# ─────────────────────────────────────────────
# Function Definitions
# ─────────────────────────────────────────────
def get_smart_greeting(username):
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = t("good_morning")
    elif 12 <= hour < 17:
        greeting = t("good_afternoon")
    elif 17 <= hour < 21:
        greeting = t("good_evening")
    else:
        greeting = t("good_night")
    
    return f'<div class="greeting-text">{greeting}, {username}! 👋</div>'

def focus_mode():
    """Display focus mode with Pomodoro timer"""
    if "focus_mode" not in st.session_state:
        st.session_state.focus_mode = False
    if "pomodoro_time" not in st.session_state:
        st.session_state.pomodoro_time = 25 * 60
    if "pomodoro_running" not in st.session_state:
        st.session_state.pomodoro_running = False
    if "pomodoro_break" not in st.session_state:
        st.session_state.pomodoro_break = False

    if st.session_state.focus_mode:
        minutes = st.session_state.pomodoro_time // 60
        seconds = st.session_state.pomodoro_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        mode_text = t("focus_mode_title") if not st.session_state.pomodoro_break else t("break_time")
        
        st.markdown(f"""
        <div class="focus-mode">
            <div class="pomodoro-timer">
                <p style="color: rgba(255,255,255,0.6); font-size: 1.2rem; margin-bottom: 1rem;">{mode_text}</p>
                <div class="pomodoro-time">{time_str}</div>
                <div class="pomodoro-controls">
                    <button class="focus-btn" onclick="window.location.reload()">{t("exit_focus")}</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.pomodoro_running and st.session_state.pomodoro_time > 0:
            time.sleep(1)
            st.session_state.pomodoro_time -= 1
            st.rerun()
        elif st.session_state.pomodoro_time == 0:
            if not st.session_state.pomodoro_break:
                st.session_state.pomodoro_break = True
                st.session_state.pomodoro_time = 5 * 60
            else:
                st.session_state.pomodoro_break = False
                st.session_state.pomodoro_time = 25 * 60
                st.session_state.pomodoro_running = False

def achievement_popup(icon, title, description):
    """Display achievement unlock animation"""
    if "achievement_shown" not in st.session_state:
        st.session_state.achievement_shown = False
    
    if not st.session_state.achievement_shown:
        st.session_state.achievement_shown = True
        st.markdown(f"""
        <div class="achievement-popup">
            <span class="achievement-icon">{icon}</span>
            <div class="achievement-title">{title}</div>
            <p style="color: var(--text-secondary); margin: 0;">{description}</p>
            <button onclick="this.parentElement.style.display='none'" 
                    style="margin-top: 1.5rem; padding: 0.75rem 2rem; border-radius: 50px; 
                           background: var(--primary-gradient); color: white; border: none; 
                           cursor: pointer; font-weight: 600;">
                Awesome! 🎉
            </button>
        </div>
        """, unsafe_allow_html=True)

def show_confetti():
    """Display confetti animation"""
    colors = ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4ecdc4", "#ffd93d"]
    confetti_html = """
    <div class="confetti-container">
    """
    for i in range(50):
        color = random.choice(colors)
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        duration = random.uniform(2, 4)
        confetti_html += f"""
        <div class="confetti" style="
            left: {left}%;
            background: {color};
            animation-delay: {delay}s;
            animation-duration: {duration}s;
            border-radius: {random.randint(0, 50)}%;
            width: {random.randint(6, 12)}px;
            height: {random.randint(6, 12)}px;
        "></div>
        """
    confetti_html += "</div>"
    st.markdown(confetti_html, unsafe_allow_html=True)

def create_circular_progress(percentage, label="XP Progress"):
    """Create animated circular progress indicator"""
    offset = 377 - (377 * percentage / 100)
    return f"""
    <div class="circular-progress">
        <svg width="150" height="150" viewBox="0 0 150 150">
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                </linearGradient>
            </defs>
            <circle class="bg" cx="75" cy="75" r="60"/>
            <circle class="progress" cx="75" cy="75" r="60" style="--progress-offset: {offset};"/>
        </svg>
        <div class="value">{int(percentage)}%</div>
    </div>
    <p style="text-align: center; margin-top: 0.5rem; font-weight: 500;">{label}</p>
    """

def get_daily_quote():
    """Get random motivational quote for the day"""
    quotes = [
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
        ("Education is the passport to the future, for tomorrow belongs to those who prepare for it today.", "Malcolm X"),
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("Your limitation—it's only your imagination.", "Unknown"),
        ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
        ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
        ("Learning is not attained by chance, it must be sought for with ardor and attended to with diligence.", "Abigail Adams"),
        ("The beautiful thing about learning is that no one can take it away from you.", "B.B. King")
    ]
    # Use date to get consistent quote per day
    day_seed = int(datetime.now().strftime("%Y%m%d"))
    random.seed(day_seed)
    return random.choice(quotes)

def create_study_heatmap():
    """Create GitHub-style study heatmap"""
    heatmap_html = '<div class="heatmap-container">'
    today = datetime.now()
    for week in range(52):
        for day in range(7):
            date = today - timedelta(days=(51 - week) * 7 + (6 - day))
            # Generate random activity level for demo
            level = random.randint(0, 4) if random.random() > 0.3 else 0
            heatmap_html += f'<div class="heatmap-day level-{level}" title="{date.strftime("%Y-%m-%d")}: {level * 2} hours"></div>'
    heatmap_html += "</div>"
    return heatmap_html

def create_ai_insights():
    """Create AI study insights card"""
    insights = [
        ("📈", "Weekly Performance", "Your study hours increased by 15% this week. Keep up the great work!"),
        ("💪", "Strength Detected", "You excel at mathematics problems. Continue challenging yourself!"),
        ("🎯", "Growth Opportunity", "Try spending more time on theoretical concepts to improve retention."),
        ("⏰", "Optimal Time", "Your most productive hours are between 7 PM - 9 PM. Schedule focused study then.")
    ]
    
    return f"""
    <div class="insights-card">
        <h3 style="margin-bottom: 1.5rem;">🧠 AI Study Insights</h3>
        <div class="insight-item">
            <span style="font-size: 1.5rem;">📈</span>
            <div>
                <h4 style="margin: 0 0 0.25rem 0;">Weekly Performance</h4>
                <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">Your study hours increased by 15% this week. Keep up the great work!</p>
            </div>
        </div>
        <div class="insight-item">
            <span style="font-size: 1.5rem;">💪</span>
            <div>
                <h4 style="margin: 0 0 0.25rem 0;">Strength Detected</h4>
                <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">You excel at mathematics problems. Continue challenging yourself!</p>
            </div>
        </div>
        <div class="insight-item">
            <span style="font-size: 1.5rem;">🎯</span>
            <div>
                <h4 style="margin: 0 0 0.25rem 0;">Growth Opportunity</h4>
                <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">Try spending more time on theoretical concepts to improve retention.</p>
            </div>
        </div>
        <div class="insight-item">
            <span style="font-size: 1.5rem;">⏰</span>
            <div>
                <h4 style="margin: 0 0 0.25rem 0;">Optimal Time</h4>
                <p style="margin: 0; color: var(--text-secondary); font-size: 0.9rem;">Your most productive hours are between 7 PM - 9 PM. Schedule focused study then.</p>
            </div>
        </div>
    </div>
    """

# Inject custom CSS
inject_custom_css()
add_language_selector()

# ── Handle logout from navbar (query-param approach) ──────────────────────────
if "logout" in st.query_params:
    st.query_params.clear()
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("app.py")

# ── Auth guard: redirect immediately, never show warning text ─────────────────
if "token" not in st.session_state or st.session_state.token is None:
    st.switch_page("app.py")

with st.spinner("Loading profile..."):
    res = get_me(st.session_state.token)
    stats_res = get_user_stats(st.session_state.token)
    
    if res.status_code == 200 and stats_res.status_code == 200:
        user_data = res.json()
        stats = stats_res.json()
=======
from frontend.api_client import get_me

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Please login first on the Home page to view this dashboard.")
    st.stop()

with st.spinner("Loading profile..."):
    res = get_me(st.session_state.token)
    if res.status_code == 200:
        user_data = res.json()
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    else:
        st.error("Session expired or invalid. Please login again.")
        st.session_state.token = None
        st.stop()

<<<<<<< HEAD
# Store user data in session state
if "user_data" not in st.session_state:
    st.session_state.user_data = user_data

# Get user name for greeting and avatar
user_full_name = user_data.get('full_name') or user_data.get('email', 'User').split('@')[0]
# Get user initials for avatar
if user_data.get('full_name'):
    initials = ''.join([part[0].upper() for part in user_full_name.split() if part])[:2]
else:
    user_email = user_data.get('email', 'JD')
    initials = ''.join([part[0].upper() for part in user_email.split('@')[0].split('.') if part])[:2]

# Render navbar
st.markdown(create_navbar("Dashboard", initials), unsafe_allow_html=True)


# Dynamic Time Based Greeting
st.markdown(get_smart_greeting(user_full_name), unsafe_allow_html=True)

# Badges and XP removed as per request

# Initialize current view if not exists
if "current_view" not in st.session_state:
    st.session_state.current_view = "dashboard"

# Quick Actions
st.subheader("⚡ Quick Actions")
action_col1, action_col2, action_col3, action_col4, action_col5 = st.columns(5)

with action_col1:
    if st.button("📚 " + t("study_planner"), use_container_width=True, key="planner_btn", 
                type="secondary" if st.session_state.current_view != "planner" else "primary"):
        st.session_state.current_view = "planner"
        st.rerun()
with action_col2:
    if st.button("✅ " + t("study_tracker"), use_container_width=True, key="tracker_btn",
                type="secondary" if st.session_state.current_view != "tracker" else "primary"):
        st.session_state.current_view = "tracker"
        st.rerun()
with action_col3:
    if st.button("❓ " + t("doubt_explainer"), use_container_width=True, key="doubt_btn",
                type="secondary" if st.session_state.current_view != "doubt" else "primary"):
        st.session_state.current_view = "doubt"
        st.rerun()
with action_col4:
    if st.button("⏱️ " + t("pomodoro"), use_container_width=True, key="pomodoro_btn",
                type="secondary" if st.session_state.current_view != "pomodoro" else "primary"):
        st.session_state.current_view = "pomodoro"
        st.rerun()
with action_col5:
    if st.button(f"🎯 {t('focus_mode')}", use_container_width=True, type="secondary"):
        st.session_state.focus_mode = True
        st.session_state.pomodoro_running = True
        st.rerun()

# Back button for non-dashboard views
if st.session_state.current_view != "dashboard":
    if st.button("← Back to Dashboard", use_container_width=False, key="back_btn"):
        st.session_state.current_view = "dashboard"
        st.rerun()
    st.markdown("---")

# Activate focus mode if enabled
if st.session_state.get("focus_mode", False):
    focus_mode()

# Dynamic view rendering based on current_view
if st.session_state.current_view == "dashboard":
    # Show regular dashboard content
    pass

elif st.session_state.current_view == "planner":
    # Study Planner Component
    st.markdown("""
    <div class="page-transition" style="margin-bottom: 2rem;">
        <h1>📅 Smart Study Planner</h1>
        <p class="text-muted">Create your personalized study schedule</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load existing plans
    
    with st.spinner("Loading your schedule..."):
        res = get_my_plans(st.session_state.token)
        if res.status_code == 200:
            data = res.json()
            plans = data.get("plans", [])
            schedule = data.get("schedule", [])
            progress_percentage = data.get("progress_percentage", 0.0)
        else:
            st.error("Failed to load study plans.")
            plans = []
            schedule = []
            progress_percentage = 0.0
            
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Subject")
        with st.form("create_plan_form"):
            subject = st.text_input("Subject Name (e.g., Mathematics)")
            exam_date = st.date_input("Exam Date", min_value=date.today())
            daily_hours = st.number_input("Total Daily Available Hours", min_value=0.5, value=4.0, step=0.5, help="We use the maximum entered here to distribute time proportionally across subjects.")
            is_weak = st.checkbox("I am weak in this subject (allocates 40% extra time)")
            
            submitted = st.form_submit_button("Add to Schedule")
            if submitted:
                if not subject:
                    st.error("Please enter a subject name.")
                else:
                    resp = create_study_plan(st.session_state.token, subject, exam_date, daily_hours, is_weak)
                    if resp.status_code == 200:
                        st.success("Added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add plan.")
    
    with col2:
        st.subheader(f"Overall Progress: {progress_percentage:.1f}%")
        st.progress(progress_percentage / 100.0)
        
        st.subheader("Your Subjects")
        if not plans:
            st.info("No subjects added yet. Add one from the left panel.")
        else:
            for p in plans:
                c1, c2, c3, c4 = st.columns([0.1, 0.5, 0.3, 0.1])
                is_checked = p["is_completed"]
                
                with c1:
                    if st.checkbox("Done", value=is_checked, key=f"check_{p['id']}", label_visibility="collapsed"):
                        if not is_checked:
                            toggle_complete(st.session_state.token, p["id"])
                            st.rerun()
                    else:
                        if is_checked:
                            toggle_complete(st.session_state.token, p["id"])
                            st.rerun()
                            
                with c2:
                    st.write(f"**{p['subject']}** {'(Weak)' if p['is_weak_subject'] else ''}")
                with c3:
                    st.write(f"Exam: {p['exam_date']}")
                with c4:
                    if st.button("❌", key=f"del_{p['id']}", help="Delete Subject"):
                        delete_study_plan(st.session_state.token, p["id"])
                        st.rerun()
    
    st.markdown("---")
    st.subheader("Generated Daily Timetable")
    if schedule:
        df = pd.DataFrame(schedule)
        df.columns = ["Start Time", "End Time", "Task"]
        
        def color_breaks(val):
            color = 'background-color: #2e7d32' if val == "Break" else ('background-color: #1565c0' if val == "Daily Revision" else '')
            return color

        st.table(df.style.map(color_breaks, subset=['Task']))
    else:
        st.info("Add active subjects to see your generated timetable here. If all subjects are completed, you have free time!")

elif st.session_state.current_view == "pomodoro":
    # Pomodoro Component
    st.markdown("""
    <div class="page-transition" style="margin-bottom: 2rem;">
        <h1>⏱️ Pomodoro Timer</h1>
        <p class="text-muted">Stay focused with the Pomodoro Technique</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize pomodoro state
    if "pomodoro_time" not in st.session_state:
        st.session_state.pomodoro_time = 25 * 60
    if "pomodoro_running" not in st.session_state:
        st.session_state.pomodoro_running = False
    if "pomodoro_break" not in st.session_state:
        st.session_state.pomodoro_break = False
    
    minutes = st.session_state.pomodoro_time // 60
    seconds = st.session_state.pomodoro_time % 60
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    mode_text = "🍅 Focus Mode" if not st.session_state.pomodoro_break else "☕ Break Time"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem;">
        <p style="color: rgba(255,255,255,0.6); font-size: 1.5rem; margin-bottom: 1rem;">{mode_text}</p>
        <div style="font-size: 8rem; font-weight: 700; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{time_str}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶ Start", use_container_width=True):
            st.session_state.pomodoro_running = True
            st.rerun()
    with col2:
        if st.button("⏸ Pause", use_container_width=True):
            st.session_state.pomodoro_running = False
    with col3:
        if st.button("↺ Reset", use_container_width=True):
            st.session_state.pomodoro_time = 25 * 60
            st.session_state.pomodoro_running = False
            st.session_state.pomodoro_break = False
            st.rerun()
    
    if st.session_state.pomodoro_running and st.session_state.pomodoro_time > 0:
        time.sleep(1)
        st.session_state.pomodoro_time -= 1
        st.rerun()
    elif st.session_state.pomodoro_time == 0:
        if not st.session_state.pomodoro_break:
            st.session_state.pomodoro_break = True
            st.session_state.pomodoro_time = 5 * 60
            st.success("🎉 Focus session complete! Time for a break.")
        else:
            st.session_state.pomodoro_break = False
            st.session_state.pomodoro_time = 25 * 60
            st.session_state.pomodoro_running = False
            st.success("Break over! Ready for another focus session.")
        st.rerun()

elif st.session_state.current_view == "doubt":
    # Doubt Explainer Component
    st.markdown("""
    <div class="page-transition" style="margin-bottom: 2rem;">
        <h1>💡 Smart Doubt Explainer</h1>
        <p class="text-muted">Get AI-powered explanations for your doubts</p>
    </div>
    """, unsafe_allow_html=True)
    
    from api_client import explain_doubt, get_history
    
    with st.form("doubt_form"):
        question = st.text_area("Enter your doubt:", height=100)
        difficulty = st.selectbox("Explain like:", ["like I'm 10", "intermediate", "technical"])
        submitted = st.form_submit_button("Explain Doubt", use_container_width=True)
        
        if submitted and question:
            with st.spinner("AI is thinking..."):
                result = explain_doubt(st.session_state.token, question, difficulty)
                if result:
                    st.markdown("### Explanation:")
                    st.markdown(result.get("explanation", "No explanation available."))
    
    st.markdown("---")
    st.subheader("📜 Your Doubt History")
    history = get_history(st.session_state.token)
    if not history:
        st.info("No doubt history yet. Ask your first doubt above!")
    else:
        for item in history[:5]:
            with st.expander(f"📝 {item['question'][:50]}..."):
                st.write(f"**Question:** {item['question']}")
                st.write(f"**Difficulty:** {item['difficulty']}")
                st.write(f"**Answer:** {item['answer']}")

# Leaderboard removed

elif st.session_state.current_view == "tracker":
    # Study Tracker Component
    st.markdown("""
    <div class="page-transition" style="margin-bottom: 2rem;">
        <h1>✅ Study Tracker</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">Track your tasks and progress.</p>
    </div>
    """, unsafe_allow_html=True)
    
    import api_client
    
    # Add New Task Section
    st.markdown('<div class="glass-card" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
    with st.form("new_task"):
        st.subheader("➕ Add New Task")
        c1, c2, c3 = st.columns(3)
        with c1:
            subject = st.text_input("Subject")
        with c2:
            topic = st.text_input("Topic")
        with c3:
            duration = st.number_input("Duration (minutes)", min_value=10, value=60, step=10)
        
        if st.form_submit_button("Add Task", use_container_width=True):
            if subject and topic:
                success = api_client.create_task(st.session_state.token, subject, topic, duration)
                if success:
                    st.success("Task added successfully!")
                    st.rerun()
            else:
                st.error("Subject and Topic are required.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tasks List Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📋 Your Tasks")
    tasks = api_client.get_tasks(st.session_state.token)
    
    if not tasks:
        st.info("No tasks added yet. Create your first task above!")
    else:
        for task in tasks:
            is_done = task["is_completed"]
            
            task_style = "opacity: 0.6; text-decoration: line-through;" if is_done else ""
            
            st.markdown(f"""
            <div style="padding: 1rem; border-radius: 12px; background: rgba(102, 126, 234, 0.05); margin: 0.5rem 0; {task_style}">
                <div style="display: flex; align-items: center; gap: 1rem;">
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([0.5, 3, 1, 1])
            
            with col1:
                if st.checkbox("", value=is_done, key=f"check_{task['id']}", label_visibility="collapsed"):
                    if not is_done:
                        api_client.toggle_task(st.session_state.token, task["id"])
                        st.rerun()
                else:
                    if is_done:
                        api_client.toggle_task(st.session_state.token, task["id"])
                        st.rerun()
                        
            with col2:
                st.markdown(f"**{task['subject']}** - {task['topic']}")
                st.caption(f"⏱️ {task['duration_minutes']} minutes")
            with col3:
                st.caption(f"📅 {task['date'][:10]}")
            with col4:
                if st.button("🗑️", key=f"del_{task['id']}", use_container_width=True):
                    api_client.delete_task(st.session_state.token, task["id"])
                    st.rerun()
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# My Learning section removed

# Daily Motivational Quote
st.markdown('<div class="glass-card" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
quote, author = get_daily_quote()
st.markdown(f"""
<div class="motivational-quote">
    "{quote}"
    <p style="text-align: right; margin-top: 1rem; font-weight: 500;">— {author}</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Circular stats and heatmap removed

# ─────────────────────────────────────────────
# Render Advanced Components
# ─────────────────────────────────────────────

# Confetti removed
=======
st.title(f"Dashboard - Welcome, {user_data.get('email')}!")

st.write("---")
st.subheader("Your Progress Overview")
st.info("The AI Study Planner will display your personalized tasks and analytics here.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Subjects Completed", value="0")
with col2:
    st.metric(label="Doubts Solved", value="0")
with col3:
    st.metric(label="Study Hours", value="0")

if st.button("Log out"):
    st.session_state.token = None
    st.success("Logged out successfully.")
    st.rerun()
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
