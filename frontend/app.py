import streamlit as st
import time
import os
import re
from api_client import login_user, signup_user, get_me

st.set_page_config(
    page_title="SmartStudy AI - Login",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def init_session_state():
    defaults = {
        "token": None,
        "user_data": None,
        "user_name": "User",
        "auth_mode": "login"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_query_param(key: str) -> str:
    try:
        return st.query_params.get(key, "")
    except AttributeError:
        params = st.experimental_get_query_params()
        return params.get(key, [""])[0]

def set_query_param(key: str, val: str):
    try:
        st.query_params[key] = val
    except AttributeError:
        st.experimental_set_query_params(**{key: val})

def _logout():
    st.session_state.token = None
    st.session_state.user_data = None
    try:
        st.query_params.clear()
    except AttributeError:
        st.experimental_set_query_params()
    st.rerun()

def render_auth():
    def _pw_score(pw):
        s = 0
        if len(pw) >= 8:              s += 1
        if re.search(r"[A-Z]", pw):   s += 1
        if re.search(r"[0-9]", pw):   s += 1
        if re.search(r"[!@#$%^&*]",pw): s += 1
        return s

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #1e1b4b 0%, #05070a 45%, #000 100%) !important;
    background-attachment: fixed !important;
    color: #f8fafc !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }

[data-testid="stHorizontalBlock"] {
    height: 100vh !important; padding: 0 !important; gap: 0 !important; align-items: center;
}
[data-testid="stHorizontalBlock"]>[data-testid="column"]:nth-of-type(1) {
    display: flex !important; flex-direction: column !important;
    justify-content: center !important; align-items: center !important;
    padding: 2.5rem !important; background: #000 !important; height: 100vh !important;
}
[data-testid="stHorizontalBlock"]>[data-testid="column"]:nth-of-type(2) {
    display: flex !important; flex-direction: column !important;
    justify-content: center !important; align-items: center !important;
    padding: 0 6% !important; background: #000 !important;
    height: 100vh !important; overflow-y: auto;
}
.brand-logo { font-size: 3rem; font-weight: 800; color: #fff; margin-bottom: 2.5rem; text-align: center; font-family: 'Outfit', sans-serif;}
.brand-logo .accent { background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }

[data-testid="stForm"] {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 18px !important; padding: 40px !important;
    box-shadow: 0 24px 60px rgba(0,0,0,.5) !important;
    width: 100%; max-width: 430px; margin: 0 auto;
}
.auth-heading { font-size: 2.1rem; font-weight: 700; color: #fff; margin-bottom: .4rem; line-height: 1.2; font-family: 'Outfit', sans-serif; }
.auth-subtext  { font-size: 1rem; color: rgba(255,255,255,.65); margin-bottom: 0; }
.stTextInput>label,[data-testid="stTextInput"]>label {
    color: rgba(255,255,255,.75) !important; font-size: 13px !important; font-weight: 500 !important; }
.stTextInput>div>div>input,[data-testid="stTextInput"] input {
    background: #111 !important; color: #fff !important;
    border: 1px solid rgba(255,255,255,.15) !important; border-radius: 12px !important;
    padding: 15px 16px !important; font-size: 14px !important; }
.stTextInput>div>div>input:focus,[data-testid="stTextInput"] input:focus {
    border-color: rgba(59,130,246,.7) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.18) !important; outline: none !important; }
[data-testid="stFormSubmitButton"]>button {
    background: linear-gradient(135deg, #1e3a8a, #1e40af, #1d4ed8) !important;
    color: #fff !important; border-radius: 12px !important; padding: 15px !important;
    font-weight: 600 !important; font-size: 15px !important; border: none !important;
    width: 100% !important; transition: transform .25s ease, box-shadow .25s ease !important;
    box-shadow: 0 6px 20px rgba(29,78,216,.35) !important; }
[data-testid="stFormSubmitButton"]>button:hover {
    transform: translateY(-3px) !important; box-shadow: 0 12px 30px rgba(29,78,216,.5) !important; }
.stButton>button {
    background: rgba(255,255,255,.05) !important; color: rgba(255,255,255,.7) !important;
    border: 1px solid rgba(255,255,255,.1) !important; border-radius: 10px !important;
    font-weight: 600 !important; padding: 10px !important; width: 100% !important;
    transition: all .25s ease !important; }
.stButton>button:hover {
    background: rgba(59,130,246,.12) !important; border-color: rgba(59,130,246,.4) !important;
    color: #60a5fa !important; transform: translateY(-1px) !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
</style>""", unsafe_allow_html=True)

    lc, rc = st.columns([1.1, 1])

    with lc:
        st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;width:100%;">
    <div class="brand-logo">SmartStudy<span class="accent">AI</span></div>
    <p style="margin-top:2rem;color:rgba(255,255,255,.4);font-family:'Inter',sans-serif;
              font-size:.85rem;text-align:center;">Your AI-powered study companion</p>
</div>""", unsafe_allow_html=True)

    with rc:
        st.markdown('<div style="max-width:430px;margin:0 auto;width:100%;position:relative;z-index:10;">', unsafe_allow_html=True)

        mode = st.session_state.auth_mode
        if mode == "login":
            st.markdown('<div class="auth-heading">Welcome Back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtext">Sign in to continue</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="auth-heading">Create Account</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtext">Start your experience today</div>', unsafe_allow_html=True)

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
                                set_query_param("token", token)
                                st.success("Login Successful!")
                                time.sleep(1.0)
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
                                st.success("Account Created!")
                                time.sleep(1.5)
                                st.session_state.auth_mode = "login"
                                st.rerun()
                            else:
                                st.error(res.json().get("detail", "Sign-up failed."))

        st.markdown('</div>', unsafe_allow_html=True)

def render_home():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #05070a 45%, #000 100%) !important;
        background-attachment: fixed !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }
    .brand-logo { font-size: 3rem; font-weight: 800; color: #fff; margin-bottom: 2rem; font-family: 'Outfit', sans-serif;}
    .brand-logo .accent { background: linear-gradient(135deg, #1e40af, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .welcome-text { font-size: 1.5rem; color: #94a3b8; font-family: 'Inter', sans-serif;}
    .logout-btn {
        margin-top: 2rem;
        padding: 10px 20px;
        background: rgba(255,255,255,.05);
        color: #f8fafc;
        border: 1px solid rgba(255,255,255,.1);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .logout-btn:hover {
        background: rgba(239,68,68,.15);
        border-color: rgba(239,68,68,.4);
        color: #fca5a5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    st.markdown('<div class="brand-logo">SmartStudy<span class="accent">AI</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="welcome-text">Welcome back, {st.session_state.user_name}!</div>', unsafe_allow_html=True)
    
    if st.button("Log Out", type="secondary"):
        _logout()
        
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    init_session_state()
    
    qp_token = get_query_param("token")
    if qp_token:
        st.session_state.token = qp_token
        try:
            res = get_me(st.session_state.token)
            if res.status_code == 200:
                ud = res.json()
                st.session_state.user_data = ud
                name = ud.get("full_name") or ud.get("email","User").split("@")[0]
                st.session_state.user_name = name
        except Exception:
            pass

    if get_query_param("logout"):
        try:
            st.query_params.clear()
        except AttributeError:
            st.experimental_set_query_params()
        _logout()

    if not st.session_state.token:
        render_auth()
        return

    if not st.session_state.user_data:
        res = get_me(st.session_state.token)
        if res.status_code != 200:
            st.session_state.token = None
            st.rerun()
            return
        ud = res.json()
        name = ud.get("full_name") or ud.get("email","User").split("@")[0]
        st.session_state.user_data = ud
        st.session_state.user_name = name

    render_home()

if __name__ == "__main__":
    main()
