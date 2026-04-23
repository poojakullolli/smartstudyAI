import os
import time
import base64
import shutil
import streamlit as st
import sys
import re

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api_client import signup_user, login_user

from translations import t

# ── Assets ────────────────────────────────────────────────────────────────────
_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartStudyAI – Study Smarter",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
if "language" not in st.session_state:
    st.session_state.language = "en"
# Force dark theme always – remove light mode entirely
st.session_state.theme = "dark"

# ── Helpers ───────────────────────────────────────────────────────────────────
def check_password_strength(password: str) -> int:
    score = 0
    if len(password) >= 8:                          score += 1
    if re.search(r"[A-Z]", password):              score += 1
    if re.search(r"[0-9]", password):              score += 1
    if re.search(r"[!@#$%^&*]", password):         score += 1
    return score

def img_to_b64(path: str) -> str:
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return ""

# ── OAuth token from URL ───────────────────────────────────────────────────────
if "token" in st.query_params:
    st.session_state.token = st.query_params["token"]
    st.query_params.clear()
    try:
        from api_client import get_me
        user_res = get_me(st.session_state.token)
        if user_res.status_code == 200:
            user_data = user_res.json()
            st.session_state["authenticated"] = True
            st.session_state["user_name"]     = user_data.get("full_name", "User")
            st.session_state["user_email"]    = user_data.get("email", "")
            st.session_state["profile_pic"]   = ""
    except Exception:
        st.session_state["authenticated"] = True
    st.rerun()

# ── Language from URL ───────────────────────────────────────────────────────
if "lang" in st.query_params:
    lang = st.query_params["lang"]
    if lang in ["en", "hi", "kn", "ta", "te"]:
        st.session_state.language = lang
    st.query_params.clear()
    st.rerun()

# ── Already logged in ──────────────────────────────────────────────────────────
if st.session_state.token is not None:
    import dashboard
    dashboard.main()
    st.stop()


# ── Image HTML ─────────────────────────────────────────────────────────────────
ILLUS_PATH = os.path.join(_ASSETS_DIR, "study_illustration.png")
illus_b64  = img_to_b64(ILLUS_PATH)
illus_html = (
    f'<img src="data:image/png;base64,{illus_b64}" class="illus-img" alt="SmartStudy AI Mascot" />'
    if illus_b64
    else '<div class="illus-img illus-fallback"></div>'
)

# ── Google OAuth button ────────────────────────────────────────────────────────
google_btn_html = """
<a href="http://127.0.0.1:8042/auth/google/login" class="google-btn" target="_self">
    <svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
    </svg>
    Continue with Google
</a>
"""

# ── Success animation ──────────────────────────────────────────────────────────
success_animation = """
<div class="success-animation">
    <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
        <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
        <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
    </svg>
    <p>Authentication Successful. Redirecting…</p>
</div>
"""

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS  –  Pure black (#000000) locked dark theme
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* ── 1. Radial gradient background – every possible Streamlit container ── */
html,
body,
#root,
.stApp,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] > section > div,
main,
.main,
.block-container {
    background: radial-gradient(ellipse at top, #0f172a 0%, #020617 50%, #000000 100%) !important;
    background-attachment: fixed !important;
}

/* Prevent white flash on rerun */
*, *::before, *::after {
    box-sizing: border-box;
}
html { background: #000000 !important; }

/* ── 2. Global font & color ── */
html, body, .stApp, [data-testid="stApp"] {
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff;
    overflow-x: hidden;
    min-height: 100vh;
}

/* ── 3. Hide Streamlit chrome ── */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
footer,
#MainMenu {
    display: none !important;
    visibility: hidden !important;
}

/* ── 4. Remove block-container padding ── */
[data-testid="stAppViewContainer"] > section > div.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── 5. Two-column layout fills viewport ── */
[data-testid="stHorizontalBlock"] {
    height: 100vh !important;
    padding: 0 !important;
    gap: 0 !important;
    position: relative;
    z-index: 10;
    align-items: center;
}

/* Left column – black + radial blue glow */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 2.5rem !important;
    background: #000000 !important;
    height: 100vh !important;
    position: relative;
    overflow: hidden;
}

/* Right column – transparent (card handles the look) */
[data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 0 6% !important;
    background: #000000 !important;
    height: 100vh !important;
    overflow-y: auto;
}

/* ── 6. Brand logo ── */
.brand-logo {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin-bottom: 2.5rem;
    text-align: center;
    font-family: 'Poppins', sans-serif;
}
.brand-logo .accent {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 60%, #60a5fa 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text;
}

/* ── 7. Mascot / illustration container ── */
.illus-container {
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

/* Radial dark-blue glow behind mascot */
.illus-glow {
    position: absolute;
    width: 240px;
    height: 240px;
    background: radial-gradient(circle, rgba(30,64,175,0.35) 0%, rgba(30,64,175,0.08) 60%, transparent 80%);
    filter: blur(60px);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 5;
    border-radius: 50%;
    pointer-events: none;
}

.illus-img {
    width: 70%;
    max-width: 300px;
    border-radius: 20px;
    position: relative;
    z-index: 10;
    animation: floatHQ 6s ease-in-out infinite alternate;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 30px 70px rgba(0,0,0,0.6);
}
.illus-fallback {
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(30,64,175,0.15) 0%, transparent 70%);
}

@keyframes floatHQ {
    0%   { transform: translateY(0px);    box-shadow: 0 20px 40px rgba(0,0,0,0.5); }
    100% { transform: translateY(-18px);  box-shadow: 0 40px 60px rgba(0,0,0,0.3); }
}

/* ── 8. Glass card (form wrapper) ── */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 18px !important;
    padding: 40px !important;
    box-shadow: 0 24px 60px rgba(0,0,0,0.5) !important;
    animation: fadeScaleUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    width: 100%;
    max-width: 430px;
    margin: 0 auto;
}

/* ── 9. Headings & sub-text ── */
.auth-heading {
    font-size: 2.1rem;
    font-weight: 700;
    color: #ffffff;
    font-family: 'Poppins', sans-serif;
    margin-bottom: 0.4rem;
    line-height: 1.2;
}
.auth-subtext {
    font-size: 1rem;
    font-weight: 400;
    color: rgba(255,255,255,0.65);
    font-family: 'Poppins', sans-serif;
    margin-bottom: 0;
}

/* ── 10. Input labels ── */
.stTextInput > label,
[data-testid="stTextInput"] > label {
    color: rgba(255,255,255,0.75) !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* ── 11. Input fields ── */
.stTextInput > div > div > input,
[data-testid="stTextInput"] input {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    padding: 15px 16px !important;
    font-size: 14px !important;
    font-family: 'Poppins', sans-serif !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
.stTextInput > div > div > input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(59,130,246,0.7) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
    outline: none !important;
}
/* Autofill stays dark */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    transition: background-color 9999s ease-in-out 0s;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
}

/* ── 12. Submit button (gradient dark-blue → navy) ── */
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    padding: 15px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    border: none !important;
    width: 100% !important;
    font-family: 'Poppins', sans-serif !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    box-shadow: 0 6px 20px rgba(29,78,216,0.35) !important;
    margin-top: 8px;
    cursor: pointer;
}
[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 30px rgba(29,78,216,0.5) !important;
}
[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.25) !important;
}
[data-testid="stFormSubmitButton"] > button:disabled {
    animation: pulseLoading 1.5s infinite;
    opacity: 0.8;
}

/* ── 13. Toggle mode buttons (Login / Sign Up) ── */
.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: rgba(59,130,246,0.12) !important;
    border-color: rgba(59,130,246,0.4) !important;
    color: #60a5fa !important;
    transform: translateY(-1px) !important;
}

/* ── 14. Divider ── */
.custom-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin: 22px 0 14px 0;
}
.custom-divider div {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.1);
}
.custom-divider span {
    font-size: 11px;
    color: rgba(255,255,255,0.4);
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'Poppins', sans-serif;
}

/* ── 15. Google button ── */
.google-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    background: rgba(255,255,255,0.07);
    color: #ffffff;
    font-weight: 600;
    font-size: 14px;
    font-family: 'Poppins', sans-serif;
    text-decoration: none;
    padding: 14px 24px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
    transition: all 0.25s ease;
    width: 100%;
    margin-top: 6px;
}
.google-btn:hover {
    background: rgba(255,255,255,0.12);
    border-color: rgba(255,255,255,0.25);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}
.google-btn:active {
    transform: translateY(1px);
}

/* ── 16. Alerts ── */
[data-testid="stAlert"] {
    animation: slideDownFade 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    border-radius: 12px !important;
}

/* ── 17. Success checkmark ── */
.success-animation {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: fadeScaleUp 0.5s ease forwards;
    padding: 1rem;
}
.success-animation p {
    color: rgba(255,255,255,0.8);
    font-family: 'Poppins', sans-serif;
    font-size: 14px;
    margin-top: 8px;
}
.checkmark {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    display: block;
    stroke-width: 2;
    stroke: #4ade80;
    stroke-miterlimit: 10;
    margin: 0 auto 6px auto;
    box-shadow: inset 0px 0px 0px #4ade80;
    animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
}
.checkmark__circle {
    stroke-dasharray: 166;
    stroke-dashoffset: 166;
    stroke-width: 2;
    stroke-miterlimit: 10;
    stroke: #4ade80;
    fill: none;
    animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}
.checkmark__check {
    transform-origin: 50% 50%;
    stroke-dasharray: 48;
    stroke-dashoffset: 48;
    animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

/* ── 18. Password strength meter ── */
.strength-meter-container {
    width: 100%;
    height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    overflow: hidden;
    margin-top: -10px;
    margin-bottom: 12px;
    display: flex;
    gap: 3px;
}
.strength-bar {
    height: 100%;
    flex: 1;
    border-radius: 4px;
    opacity: 0.25;
    transition: opacity 0.35s ease;
}
.strength-bar.active { opacity: 1; }

/* ── 19. Keyframes ── */
@keyframes fadeScaleUp {
    from { opacity: 0; transform: scale(0.96) translateY(16px); }
    to   { opacity: 1; transform: scale(1)    translateY(0);    }
}
@keyframes slideDownFade {
    from { transform: translateY(-8px); opacity: 0; }
    to   { transform: translateY(0);    opacity: 1; }
}
@keyframes pulseLoading {
    0%, 100% { opacity: 1;   transform: scale(1);    }
    50%       { opacity: 0.8; transform: scale(0.98); }
}
@keyframes stroke     { 100% { stroke-dashoffset: 0; } }
@keyframes scale      { 0%, 100% { transform: none; } 50% { transform: scale3d(1.1,1.1,1); } }
@keyframes fill       { 100% { box-shadow: inset 0px 0px 0px 30px rgba(74,222,128,0.1); } }
@keyframes anim-right { from { opacity:0; transform:translateX(-18px); } to { opacity:1; transform:translateX(0); } }
@keyframes anim-left  { from { opacity:0; transform:translateX(18px);  } to { opacity:1; transform:translateX(0); } }
.anim-fade-right { animation: anim-right 0.45s ease-out forwards; }
.anim-fade-left  { animation: anim-left  0.45s ease-out forwards; }

/* ── 20. Sidebar hidden ── */
[data-testid="stSidebar"] { display: none !important; }

/* ── 21. Spinner text color ── */
[data-testid="stSpinner"] p { color: rgba(255,255,255,0.7) !important; font-family: 'Poppins', sans-serif !important; }

/* ── 22. Subtle animated floating blurred circles ── */
.floating-circles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.float-circle {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.08;
    animation: floatCircle 25s ease-in-out infinite;
}
.float-circle:nth-child(1) {
    width: 400px;
    height: 400px;
    background: #1e3a8a;
    top: 10%;
    left: 5%;
    animation-delay: 0s;
}
.float-circle:nth-child(2) {
    width: 300px;
    height: 300px;
    background: #0f172a;
    top: 60%;
    right: 10%;
    animation-delay: 5s;
}
.float-circle:nth-child(3) {
    width: 350px;
    height: 350px;
    background: #1e3a8a;
    bottom: 5%;
    left: 30%;
    animation-delay: 10s;
}
.float-circle:nth-child(4) {
    width: 250px;
    height: 250px;
    background: #0f172a;
    top: 30%;
    right: 30%;
    animation-delay: 15s;
}
@keyframes floatCircle {
    0%, 100% { 
        transform: translate(0, 0) scale(1);
        opacity: 0.06;
    }
    25% { 
        transform: translate(20px, -30px) scale(1.1);
        opacity: 0.10;
    }
    50% { 
        transform: translate(-15px, 20px) scale(0.95);
        opacity: 0.08;
    }
    75% { 
        transform: translate(30px, 10px) scale(1.05);
        opacity: 0.07;
    }
}
</style>

<!-- Inject floating circles -->
<div class="floating-circles">
    <div class="float-circle"></div>
    <div class="float-circle"></div>
    <div class="float-circle"></div>
    <div class="float-circle"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([1.1, 1])

# ── LEFT: brand + mascot ──────────────────────────────────────────────────────
with left_col:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; width:100%;">
        <div class="brand-logo">SmartStudy<span class="accent">AI</span></div>
        <div class="illus-container">
            <div class="illus-glow"></div>
            {illus_html}
        </div>
        <p style="margin-top:2rem; color:rgba(255,255,255,0.4); font-family:'Poppins',sans-serif;
                  font-size:0.85rem; text-align:center; letter-spacing:0.5px;">
            Your AI-powered study companion
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT: auth card ──────────────────────────────────────────────────────────
with right_col:
    st.markdown('<div style="max-width:430px; margin:0 auto; width:100%; position:relative; z-index:10;">', unsafe_allow_html=True)

    # Heading
    heading_anim = "anim-fade-right" if st.session_state.auth_mode == "login" else "anim-fade-left"
    if st.session_state.auth_mode == "login":
        heading_html = """
        <div class="auth-heading">Welcome Back 👋</div>
        <div class="auth-subtext">Sign in to continue your learning journey</div>
        """
    else:
        heading_html = """
        <div class="auth-heading">Create Account ✨</div>
        <div class="auth-subtext">Start your smart study experience today</div>
        """

    st.markdown(f'<div class="{heading_anim}" style="margin-bottom:1.8rem;">{heading_html}</div>',
                unsafe_allow_html=True)

    # Mode toggle
    st.markdown('<div style="max-width:240px; margin-bottom:20px;">', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    with tc1:
        if st.button("Login", use_container_width=True, key="btn_switch_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
    with tc2:
        if st.button("Sign Up", use_container_width=True, key="btn_switch_signup"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Forms ─────────────────────────────────────────────────────────────────
    if st.session_state.auth_mode == "login":
        with st.form("login_form", clear_on_submit=False):
            login_email    = st.text_input("Email",    placeholder="you@example.com")
            login_password = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            submit_login   = st.form_submit_button("Log In →", use_container_width=True)

            if submit_login:
                if not login_email or not login_password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating…"):
                        res = login_user(login_email, login_password)
                        if res.status_code == 200:
                            st.session_state.token = res.json().get("access_token")
                            st.markdown(success_animation, unsafe_allow_html=True)
                            time.sleep(1.2)
                            st.rerun()
                        else:
                            detail = res.json().get("detail", "Invalid email or password.")
                            st.error(detail)
    else:
        with st.form("signup_form", clear_on_submit=False):
            signup_name     = st.text_input("Full Name", placeholder="John Doe")
            signup_email    = st.text_input("Email",     placeholder="you@example.com")
            signup_password = st.text_input("Password",  type="password", placeholder="Minimum 6 characters")
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            submit_signup   = st.form_submit_button("Create Account →", use_container_width=True)

            if submit_signup:
                if not signup_name or not signup_email or not signup_password:
                    st.error("Please fill in all fields.")
                else:
                    score = check_password_strength(signup_password)
                    c1 = "active" if score >= 1 else ""
                    c2 = "active" if score >= 2 else ""
                    c3 = "active" if score >= 3 else ""
                    c4 = "active" if score >= 4 else ""

                    if score < 2:
                        color = "#ef4444"
                        st.markdown(f'''
                        <div class="strength-meter-container">
                            <div class="strength-bar {c1}" style="background:{color};"></div>
                            <div class="strength-bar {c2}" style="background:{color};"></div>
                            <div class="strength-bar {c3}" style="background:{color};"></div>
                            <div class="strength-bar {c4}" style="background:{color};"></div>
                        </div>
                        ''', unsafe_allow_html=True)
                        st.error("Weak password. Add uppercase letters and numbers.")
                    elif len(signup_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        with st.spinner("Creating account…"):
                            res = signup_user(signup_email, signup_name, signup_password)
                            if res.status_code in [200, 201]:
                                st.markdown(
                                    success_animation.replace("Authentication Successful", "Account created!"),
                                    unsafe_allow_html=True
                                )
                                time.sleep(1.2)
                                st.session_state.auth_mode = "login"
                                st.rerun()
                            else:
                                detail = res.json().get("detail", "Failed to sign up.")
                                st.error(detail)

    # Google OAuth divider + button
    st.markdown(f"""
    <div class="custom-divider">
        <div></div>
        <span>Or continue with</span>
        <div></div>
    </div>
    {google_btn_html}
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
