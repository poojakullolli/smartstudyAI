import streamlit as st
import pandas as pd
from datetime import date
<<<<<<< HEAD
from api_client import create_study_plan, get_my_plans, delete_study_plan, toggle_complete
import sys
sys.path.append('C:\\Users\\Admin\\Desktop\\smartstudyAI\\smartstudyAI-main\\frontend')
from style_utils import inject_custom_css, add_language_selector, create_navbar

st.set_page_config(page_title="SmartStudyAI – Study Planner", page_icon="📚", layout="wide")

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
st.markdown(create_navbar("Study Planner", initials), unsafe_allow_html=True)

st.markdown("""
<div class="page-transition" style="margin-bottom: 2rem;">
    <h1>📅 Smart Study Planner</h1>
    <p class="text-muted">Create your personalized study schedule</p>
</div>
""", unsafe_allow_html=True)

=======
from frontend.api_client import create_study_plan, get_my_plans, delete_study_plan, toggle_complete

st.set_page_config(page_title="Study Planner", page_icon="📅", layout="wide")

if "token" not in st.session_state or st.session_state.token is None:
    st.warning("Please login first on the Home page to view your Study Planner.")
    st.stop()

st.title("Smart Study Planner")

# Load existing plans
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
with st.spinner("Loading your schedule..."):
    res = get_my_plans(st.session_state.token)
    if res.status_code == 200:
        data = res.json()
        plans = data.get("plans", [])
        schedule = data.get("schedule", [])
        progress_percentage = data.get("progress_percentage", 0.0)
    else:
        st.error("Failed to load study plans.")
        st.stop()
<<<<<<< HEAD

=======
        
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
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
    
<<<<<<< HEAD
    st.subheader("Your Subjects")
=======
    st.write("### Your Subjects")
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    if not plans:
        st.info("No subjects added yet. Add one from the left panel.")
    else:
        for p in plans:
            c1, c2, c3, c4 = st.columns([0.1, 0.5, 0.3, 0.1])
            is_checked = p["is_completed"]
            
            with c1:
<<<<<<< HEAD
=======
                # We use session state modification to trigger toggling efficiently
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
                if st.checkbox("Done", value=is_checked, key=f"check_{p['id']}", label_visibility="collapsed"):
                    if not is_checked:
                        toggle_complete(st.session_state.token, p["id"])
                        st.rerun()
                else:
                    if is_checked:
                        toggle_complete(st.session_state.token, p["id"])
                        st.rerun()
<<<<<<< HEAD
            
=======
                        
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
            with c2:
                st.write(f"**{p['subject']}** {'(Weak)' if p['is_weak_subject'] else ''}")
            with c3:
                st.write(f"Exam: {p['exam_date']}")
            with c4:
                if st.button("❌", key=f"del_{p['id']}", help="Delete Subject"):
                    delete_study_plan(st.session_state.token, p["id"])
                    st.rerun()

<<<<<<< HEAD
st.markdown("---")
=======
st.write("---")
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
st.subheader("Generated Daily Timetable")
if schedule:
    df = pd.DataFrame(schedule)
    df.columns = ["Start Time", "End Time", "Task"]
    
<<<<<<< HEAD
=======
    # We display a styled dataframe or table
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    def color_breaks(val):
        color = 'background-color: #2e7d32' if val == "Break" else ('background-color: #1565c0' if val == "Daily Revision" else '')
        return color

    st.table(df.style.map(color_breaks, subset=['Task']))
else:
<<<<<<< HEAD
    st.info("Add active subjects to see your generated timetable here. If all subjects are completed, you have free time!")
=======
    st.info("Add active subjects to see your generated timetable here. If all subjects are completed, you have free time!")
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
