import streamlit as st
from translations import language_names

def inject_custom_css():
    """Inject premium custom CSS into all pages"""
    # ── Immediately hide all default Streamlit chrome ────────────────────────
    st.markdown(
        "<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} "
        "[data-testid=\"stSidebar\"] {display: none !important;} "
        "[data-testid=\"stToolbar\"] {display: none !important;} "
        "[data-testid=\"collapsedControl\"] {display: none !important;}</style>",
        unsafe_allow_html=True
    )
    # Inject floating blurred circles
    st.markdown("""
    <div class="floating-circles">
        <div class="float-circle"></div>
        <div class="float-circle"></div>
        <div class="float-circle"></div>
        <div class="float-circle"></div>
    </div>
    """, unsafe_allow_html=True)

    # Inject CSS
    st.markdown("""
    <style>
    /* ── Global Imports ── */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    /* ── Premium SaaS Design System ── */
    :root {
        /* Core Colors */
        --primary-50: #eef2ff;
        --primary-100: #e0e7ff;
        --primary-200: #c7d2fe;
        --primary-300: #a5b4fc;
        --primary-400: #818cf8;
        --primary-500: #6366f1;
        --primary-600: #4f46e5;
        --primary-700: #4338ca;
        --primary-800: #3730a3;
        --primary-900: #312e81;

        /* Semantic Colors */
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --info: #3b82f6;

        /* Gradients */
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        --glow-gradient: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899, #6366f1);
        --bg-gradient: radial-gradient(ellipse at top, #0f172a 0%, #020617 50%, #000000 100%);
        --glass-gradient: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.03) 100%);

        /* Glass Effect */
        --glass-bg: rgba(13, 18, 48, 0.72);
        --glass-border: rgba(255, 255, 255, 0.09);
        --glass-border-hover: rgba(99, 102, 241, 0.4);

        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.35);
        --shadow-lg: 0 12px 32px rgba(0,0,0,0.4);
        --shadow-xl: 0 24px 48px rgba(0,0,0,0.5);
        --shadow-glow: 0 0 28px rgba(99,102,241,0.25);
        --shadow-glow-strong: 0 0 48px rgba(139,92,246,0.35);

        /* Typography — Poppins only */
        --font-sans: 'Poppins', ui-sans-serif, system-ui, -apple-system, sans-serif;
        --text-xs: 0.75rem;
        --text-sm: 0.875rem;
        --text-base: 1rem;
        --text-lg: 1.125rem;
        --text-xl: 1.25rem;
        --text-2xl: 1.5rem;
        --text-3xl: 1.875rem;
        --text-4xl: 2.25rem;

        /* Spacing System */
        --spacing-0: 0;
        --spacing-1: 0.25rem;
        --spacing-2: 0.5rem;
        --spacing-3: 0.75rem;
        --spacing-4: 1rem;
        --spacing-5: 1.25rem;
        --spacing-6: 1.5rem;
        --spacing-8: 2rem;
        --spacing-10: 2.5rem;
        --spacing-12: 3rem;
        --spacing-16: 4rem;

        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.25rem;
        --radius-card: 18px;
        --radius-full: 9999px;

        /* Transitions */
        --transition-fast: 180ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-medium: 320ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 520ms cubic-bezier(0.4, 0, 0.2, 1);

        /* Text Colors */
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --text-disabled: #475569;

        /* Backgrounds */
        --bg-primary: #020617;
        --bg-secondary: #0f172a;
        --bg-tertiary: #1e293b;

        /* Card Design */
        --card-radius: var(--radius-card);
        --card-padding: 1.75rem;
    }

    /* ── Force Poppins everywhere ── */
    *, *::before, *::after {
        font-family: var(--font-sans) !important;
        box-sizing: border-box;
    }

    /* ── Soft glowing gradient background ── */
    html, body,
    [class*="css"],
    .stApp,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > section,
    [data-testid="stAppViewContainer"] > section > div,
    .main, main {
        background: var(--bg-gradient) !important;
        background-attachment: fixed !important;
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }

    /* Subtle animated floating blurred circles */
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

    /* Smooth page transitions */
    .page-transition {
        animation: pageIn var(--transition-medium) ease-out;
    }
    @keyframes pageIn {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Typography System ── */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600 !important;
        line-height: 1.2 !important;
        color: var(--text-primary) !important;
        margin: 0 0 var(--spacing-2) 0 !important;
        letter-spacing: -0.3px;
    }
    h1 { font-size: var(--text-3xl) !important; font-weight: 700 !important; }
    h2 { font-size: var(--text-2xl) !important; font-weight: 600 !important; }
    h3 { font-size: var(--text-xl)  !important; font-weight: 600 !important; }
    h4 { font-size: var(--text-lg)  !important; font-weight: 600 !important; }

    p, span, div {
        color: var(--text-primary);
        line-height: 1.6;
        font-weight: 400;
    }
    .text-muted  { color: var(--text-muted)  !important; }
    .text-small  { font-size: var(--text-sm) !important; }

    /* ── Remove Streamlit Default UI Completely ── */
    #MainMenu { visibility: hidden; display: none !important; }
    footer { visibility: hidden; display: none !important; }
    header { visibility: hidden; display: none !important; height: 0 !important; }
    .stDeployButton               { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .stSidebar                    { display: none !important; }
    .st-emotion-cache-18ni7ap     { display: none !important; }
    .st-emotion-cache-1wrcr25     { margin-top: 0 !important; }
    [data-testid="stToolbar"]     { display: none !important; }
    [data-testid="stStatusWidget"]{ display: none !important; }
    [data-testid="stBaseButton-header"] { display: none !important; }
    [data-testid="collapsedControl"]    { display: none !important; }

    .block-container {
        padding-top: 88px !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 100% !important;
    }

    /* Remove default dividers/borders from Streamlit containers */
    hr { display: none !important; }
    section.main > div                          { border: none !important; }
    .stHorizontalBlock, .stVerticalBlock        { border: none !important; }
    div[data-testid="stVerticalBlock"] > div:not(:last-child) { border-bottom: none !important; }
    div[data-testid="stAppViewContainer"] > section > div     { border: none !important; box-shadow: none !important; }
    .main > .block-container                    { border: none !important; border-top: none !important; }
    .appview-container > section                { border: none !important; }
    div[data-testid="stExpander"]               { border: none !important; box-shadow: none !important; }
    div[data-testid="stForm"]                   { border: none !important; }
    .main                                       { border: none !important; border-top: none !important; }

    /* ── Glassmorphism Card System ── */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow-lg);
        padding: var(--card-padding);
        transition: transform var(--transition-medium), box-shadow var(--transition-medium), border-color var(--transition-medium);
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
    }
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--primary-gradient);
        opacity: 0;
        transition: opacity var(--transition-fast);
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl), var(--shadow-glow);
        border-color: var(--glass-border-hover);
    }
    .glass-card:hover::before { opacity: 1; }

    /* Card sub-elements */
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--spacing-5);
        padding-bottom: var(--spacing-4);
        border-bottom: 1px solid var(--glass-border);
    }
    .card-title {
        font-size: var(--text-lg);
        font-weight: 600;
        margin: 0;
        color: var(--text-primary);
    }
    .card-body  { padding: var(--spacing-4) 0; }
    .card-footer {
        margin-top: var(--spacing-5);
        padding-top: var(--spacing-4);
        border-top: 1px solid var(--glass-border);
        display: flex;
        gap: var(--spacing-3);
        justify-content: flex-end;
    }

    /* ── Quick Action Buttons — animated scale + glow ── */
    .quick-action-btn {
        background: var(--glass-bg);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-card);
        padding: 1.5rem 1.25rem;
        text-align: center;
        cursor: pointer;
        transition:
            transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1),
            box-shadow 200ms ease,
            border-color 200ms ease,
            background 200ms ease;
        text-decoration: none;
        color: var(--text-primary);
        display: block;
        position: relative;
        overflow: hidden;
    }
    .quick-action-btn::before {
        content: '';
        position: absolute;
        inset: 0;
        background: var(--primary-gradient);
        opacity: 0;
        transition: opacity 200ms ease;
        border-radius: inherit;
    }
    .quick-action-btn:hover {
        transform: scale(1.05) translateY(-3px);
        box-shadow: 0 8px 32px rgba(99,102,241,0.35), 0 0 0 1px rgba(99,102,241,0.3);
        border-color: rgba(99,102,241,0.45);
        background: rgba(99,102,241,0.1);
    }
    .quick-action-btn:active {
        transform: scale(1.01) translateY(-1px);
    }
    .quick-action-icon {
        font-size: 1.5rem;
        margin-bottom: 0.6rem;
        display: block;
        position: relative;
        z-index: 1;
    }
    .quick-action-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        position: relative;
        z-index: 1;
        letter-spacing: 0.1px;
    }

    /* Streamlit built-in buttons — premium gradient */
    div[data-testid="stButton"] > button {
        background: var(--primary-gradient) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--spacing-3) var(--spacing-6) !important;
        font-weight: 600 !important;
        font-size: var(--text-sm) !important;
        transition:
            transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1),
            box-shadow 200ms ease !important;
        box-shadow: var(--shadow-md) !important;
        letter-spacing: 0.1px;
    }
    div[data-testid="stButton"] > button:hover {
        transform: scale(1.05) translateY(-2px) !important;
        box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
    }
    div[data-testid="stButton"] > button:active {
        transform: scale(1.01) translateY(0) !important;
        box-shadow: var(--shadow-md) !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(10px);
        color: var(--text-primary) !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: rgba(99,102,241,0.1) !important;
        border-color: var(--glass-border-hover) !important;
        transform: scale(1.04) translateY(-1px) !important;
    }

    /* ── Metric Cards ── */
    div[data-testid="stMetric"] {
        background: var(--glass-bg);
        backdrop-filter: blur(18px);
        padding: 1.5rem;
        border-radius: var(--radius-card);
        border: 1px solid var(--glass-border);
        transition: transform var(--transition-fast), box-shadow var(--transition-fast);
        box-shadow: var(--shadow-md);
        margin-bottom: 1rem;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
        border-color: var(--glass-border-hover);
    }
    div[data-testid="stMetric"] label {
        color: var(--text-secondary) !important;
        font-size: var(--text-sm) !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: var(--text-3xl) !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
    }

    /* ── Form Inputs ── */
    div[data-testid="stTextInput"] > div > input,
    div[data-testid="stNumberInput"] > div > input,
    div[data-testid="stTextArea"] > div > textarea,
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--spacing-3) var(--spacing-4) !important;
        font-size: var(--text-sm) !important;
        transition: all var(--transition-fast) !important;
        color: var(--text-primary) !important;
    }
    div[data-testid="stTextInput"] > div > input:focus,
    div[data-testid="stNumberInput"] > div > input:focus,
    div[data-testid="stTextArea"] > div > textarea:focus,
    div[data-testid="stSelectbox"] > div > div:focus {
        border-color: var(--primary-400) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
        outline: none !important;
    }

    /* ── Form Labels ── */
    label {
        font-weight: 500 !important;
        font-size: var(--text-sm) !important;
        color: var(--text-secondary) !important;
        margin-bottom: var(--spacing-2) !important;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(255,255,255,0.04);
        padding: 6px;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: var(--text-sm) !important;
        color: var(--text-secondary) !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: #fff !important;
        box-shadow: var(--shadow-glow) !important;
    }



    /* ── Loading Spinner ── */
    .spinner {
        width: 40px; height: 40px;
        border: 3px solid rgba(99,102,241,0.12);
        border-top-color: var(--primary-500);
        border-radius: 50%;
        animation: spin 0.9s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ── Professional Learning Cards ── */
    .learning-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-card);
        padding: 1.75rem;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
        transition: all var(--transition-medium);
        margin-bottom: 1.75rem;
    }
    .learning-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    .learning-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--shadow-xl), var(--shadow-glow);
        border-color: var(--glass-border-hover);
    }

    /* ── Dashboard Components ── */
    .level-badge {
        display: inline-block;
        background: var(--primary-gradient);
        color: #fff;
        padding: 0.4rem 1.2rem;
        border-radius: var(--radius-full);
        font-weight: 700;
        font-size: 1rem;
        box-shadow: var(--shadow-glow);
        animation: badgeGlow 2.5s ease-in-out infinite;
    }
    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(99,102,241,0.35); }
        50%       { box-shadow: 0 0 40px rgba(139,92,246,0.55); }
    }

    /* ── Leaderboard Top 3 Cards ── */
    .leaderboard-top-card {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: var(--radius-card);
        padding: 1.75rem;
        text-align: center;
        transition: all var(--transition-medium);
        border: 1px solid var(--glass-border);
    }
    .leaderboard-top-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-glow-strong);
    }
    .leaderboard-top-card.first {
        background: linear-gradient(135deg, rgba(255,215,0,0.12), rgba(255,165,0,0.07));
        animation: topCardPulse 2.5s ease-in-out infinite;
    }
    @keyframes topCardPulse {
        0%, 100% { box-shadow: 0 8px 32px rgba(255,215,0,0.15); }
        50%       { box-shadow: 0 16px 56px rgba(255,215,0,0.28); }
    }

    /* ── Quick Action (native Streamlit buttons on dashboard) ── */
    /* Targets buttons that act as quick actions via st.button */
    div[data-testid="column"] div[data-testid="stButton"] > button {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(18px) !important;
        border-radius: var(--radius-card) !important;
        padding: 1.25rem 0.75rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        color: var(--text-primary) !important;
        width: 100% !important;
        transition:
            transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1),
            box-shadow 200ms ease,
            border-color 200ms ease,
            background 200ms ease !important;
        box-shadow: var(--shadow-sm) !important;
        letter-spacing: 0.1px;
    }
    div[data-testid="column"] div[data-testid="stButton"] > button:hover {
        transform: scale(1.05) translateY(-3px) !important;
        box-shadow: 0 8px 32px rgba(99,102,241,0.30), 0 0 0 1px rgba(99,102,241,0.3) !important;
        border-color: rgba(99,102,241,0.45) !important;
        background: rgba(99,102,241,0.08) !important;
    }
    div[data-testid="column"] div[data-testid="stButton"] > button:active {
        transform: scale(1.01) translateY(-1px) !important;
    }

    /* ── Circular XP Progress Indicator ── */
    .circular-progress {
        position: relative;
        width: 150px; height: 150px;
        margin: 0 auto;
    }
    .circular-progress svg { transform: rotate(-90deg); }
    .circular-progress circle {
        fill: none;
        stroke-width: 12;
        stroke-linecap: round;
    }
    .circular-progress .bg      { stroke: rgba(255,255,255,0.06); }
    .circular-progress .progress {
        stroke: url(#gradient);
        stroke-dasharray: 377;
        stroke-dashoffset: 377;
        animation: circularProgress 2s ease-out forwards;
    }
    @keyframes circularProgress {
        to { stroke-dashoffset: var(--progress-offset); }
    }
    .circular-progress .value {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ── Study Heatmap ── */
    .heatmap-container {
        display: grid;
        grid-template-columns: repeat(53, 12px);
        gap: 3px;
        padding: 1rem;
        overflow-x: auto;
    }
    .heatmap-day {
        width: 12px; height: 12px;
        border-radius: 3px;
        transition: transform 0.15s ease;
    }
    .heatmap-day:hover { transform: scale(1.5); }
    .heatmap-day.level-0 { background: rgba(255,255,255,0.05); }
    .heatmap-day.level-1 { background: rgba(99,102,241,0.3); }
    .heatmap-day.level-2 { background: rgba(99,102,241,0.5); }
    .heatmap-day.level-3 { background: rgba(99,102,241,0.7); }
    .heatmap-day.level-4 { background: rgba(99,102,241,1); }

    /* ── Motivational Quote ── */
    .motivational-quote {
        font-style: italic;
        font-size: 1.05rem;
        font-weight: 400;
        color: var(--text-secondary);
        text-align: center;
        padding: 1.5rem 2rem;
        border-left: 3px solid transparent;
        border-image: var(--primary-gradient) 1;
        margin: 0.5rem 0;
        animation: quoteFadeIn 1s ease-out;
        line-height: 1.7;
    }
    @keyframes quoteFadeIn {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Smart Greeting ── */
    .greeting-text {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f1f5f9 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: greetingFade 0.8s ease-out;
        margin-bottom: 0.5rem;
    }
    @keyframes greetingFade {
        from { opacity: 0; transform: translateY(-16px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── AI Insights card ── */
    .insights-card {
        background: var(--glass-bg);
        backdrop-filter: blur(18px);
        border-radius: var(--radius-card);
        padding: 1.75rem;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.75rem;
    }
    .insights-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    .insight-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.9rem 1rem;
        margin: 0.4rem 0;
        background: rgba(99,102,241,0.05);
        border-radius: 12px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    .insight-item:hover {
        background: rgba(99,102,241,0.1);
        border-color: rgba(99,102,241,0.15);
        transform: translateX(4px);
    }

    /* ── Focus Mode ── */
    .focus-mode {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 99999;
        background: #05060f;
        transition: all 0.5s ease;
    }
    .focus-mode .pomodoro-timer {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    .pomodoro-time {
        font-size: 8rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }
    .pomodoro-controls {
        margin-top: 2rem;
        display: flex;
        gap: 1rem;
        justify-content: center;
    }
    .focus-btn {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.15);
        color: #fff;
        padding: 0.9rem 2rem;
        border-radius: var(--radius-full);
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 600;
        transition: all 0.25s ease;
        font-family: var(--font-sans);
    }
    .focus-btn:hover {
        background: rgba(99,102,241,0.2);
        border-color: rgba(99,102,241,0.5);
        transform: scale(1.05);
        box-shadow: var(--shadow-glow);
    }

    /* ── Achievement Popup ── */
    .achievement-popup {
        position: fixed;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%) scale(0.5);
        background: rgba(13,18,48,0.95);
        backdrop-filter: blur(30px);
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        z-index: 999999;
        border: 2px solid rgba(255,215,0,0.35);
        box-shadow: 0 0 60px rgba(255,215,0,0.25);
        animation: achievementUnlock 0.8s ease-out forwards;
    }
    @keyframes achievementUnlock {
        0%   { opacity: 0; transform: translate(-50%,-50%) scale(0.3) rotate(-10deg); }
        50%  {             transform: translate(-50%,-50%) scale(1.1) rotate(4deg); }
        100% { opacity: 1; transform: translate(-50%,-50%) scale(1) rotate(0deg); }
    }
    .achievement-icon  { font-size: 4.5rem; display: block; }
    .achievement-title {
        font-size: 1.75rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem;
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ── Confetti ── */
    .confetti-container {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 99999;
        overflow: hidden;
    }
    .confetti {
        position: absolute;
        width: 10px; height: 10px;
        top: -10px;
        animation: confettiFall 3s ease-out forwards;
    }
    @keyframes confettiFall {
        0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }

    /* ── Section spacing ── */
    div[data-testid="stVerticalBlock"] > div {
        margin-bottom: 0.5rem;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 1.25rem !important;
    }

    /* ── Mobile Responsiveness ── */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        .glass-card { padding: 1.25rem; }
        .pomodoro-time { font-size: 4.5rem; }
        .achievement-popup { width: 90%; padding: 2rem; }
        .greeting-text { font-size: 1.5rem; }
        .heatmap-container { grid-template-columns: repeat(28, 12px); }
    }
    </style>
    """, unsafe_allow_html=True)

def add_language_selector():
    """Add language selector (deprecated - now in navbar profile dropdown)"""
    pass


def create_quick_action_button(icon, label, view_name=None):
    """Create a styled quick action button"""
    return f"""
    <div class="quick-action-btn" style="cursor: pointer;">
        <span class="quick-action-icon"></span>
        <span class="quick-action-label">{label}</span>
    </div>
    """

def create_navbar(current_page="Home", user_initials="JD"):
    """Premium SaaS-grade sticky horizontal navbar.

    Items  : Home | Study Planner | Study Tracker | Pomodoro | Focus Mode
    Design : deep dark glass, Poppins SemiBold (600), rounded pill active,
             animated glowing underline, 0.3s transitions, no Streamlit chrome.
    """
    pages = [
        ("Home",          "pages/1_Dashboard.py"),
        ("Study Planner", "pages/2_Study_Planner.py"),
        ("Study Tracker", "pages/4_Study_Tracker.py"),
        ("Pomodoro",      "pages/5_Pomodoro.py"),
        ("Focus Mode",    "pages/5_Pomodoro.py"),
    ]

    nav_items_html = ""
    for label, page in pages:
        is_active = (
            current_page == label
            or (current_page == "Dashboard" and label == "Home")
        )
        cls = " nav-active" if is_active else ""
        nav_items_html += f'<a class="nb-item{cls}" href="{page}">{label}</a>'

    html = f"""
<!-- SmartStudy AI — Premium SaaS Navbar -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Kill ALL Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],[data-testid="stHeader"],
[data-testid="stStatusWidget"],[data-testid="stBaseButton-header"],
[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton {{ display:none!important; visibility:hidden!important; }}

/* ── Shell — deep dark glass ───────────────────────────────── */
.smartnav {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 66px;
    background: linear-gradient(180deg,
        rgba(5,7,18,.97)  0%,
        rgba(8,11,28,.95) 100%);
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

/* Animated shimmer bottom-border glow */
.smartnav::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        #4f46e5 22%, #818cf8 45%, #a78bfa 55%,
        #818cf8 72%, #4f46e5 82%,
        transparent 100%);
    background-size: 250% 100%;
    animation: navShimmer 4s ease-in-out infinite;
    opacity: .75;
}}
@keyframes navShimmer {{
    0%   {{ background-position: -250% 0; }}
    100% {{ background-position:  250% 0; }}
}}

/* ── Logo ──────────────────────────────────────────────────── */
.nb-logo {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -.3px;
    background: linear-gradient(135deg, #a5b4fc 0%, #818cf8 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    white-space: nowrap;
    flex-shrink: 0;
    text-decoration: none;
    transition: opacity .3s ease;
}}
.nb-logo:hover {{ opacity: .82; }}

/* ── Menu row — always single horizontal line ──────────────── */
.nb-menu {{
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: center;
    gap: .2rem;
    flex: 1;
    padding: 0 1.5rem;
}}

/* ── Nav items — Poppins SemiBold pill ─────────────────────── */
.nb-item {{
    font-family: 'Poppins', sans-serif;
    font-size: .855rem;
    font-weight: 600;
    color: rgba(255,255,255,.46);
    text-decoration: none;
    padding: .42rem 1.1rem;
    border-radius: 50px;
    white-space: nowrap;
    cursor: pointer;
    position: relative;
    letter-spacing: .06px;
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
.nb-item:active {{
    transform: translateY(1px);
    transition-duration: .1s;
}}

/* Active / selected pill + glow */
.nb-item.nav-active {{
    color: #fff;
    background: rgba(99,102,241,.22);
    box-shadow:
        0 0 0 1px rgba(129,140,248,.32),
        0 4px 18px rgba(99,102,241,.28),
        0 0 28px rgba(99,102,241,.13);
}}

/* Animated glowing underline on active tab */
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

/* ── Right zone ────────────────────────────────────────────── */
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
    transition:
        transform  .3s cubic-bezier(.34,1.56,.64,1),
        box-shadow .3s ease;
    user-select: none;
}}
.nb-avatar:hover {{
    transform: scale(1.1);
    box-shadow:
        0 0 0 2.5px rgba(129,140,248,.55),
        0 0 22px rgba(99,102,241,.42);
}}

/* ── Dropdown ──────────────────────────────────────────────── */
.nb-dropdown {{
    display: none;
    position: fixed;
    top: 70px; right: 2rem;
    background: linear-gradient(160deg,
        rgba(9,12,32,.98) 0%,
        rgba(13,17,44,.96) 100%);
    border: 1px solid rgba(129,140,248,.17);
    border-radius: 16px;
    min-width: 202px;
    padding: .5rem 0;
    box-shadow:
        0 20px 60px rgba(0,0,0,.7),
        0 0 0 1px rgba(255,255,255,.04) inset;
    backdrop-filter: blur(24px);
    z-index: 9999999;
}}
.nb-dropdown.open {{
    display: block;
    animation: ddSlide .28s cubic-bezier(.16,1,.3,1) forwards;
}}
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
.nb-dd-item:hover {{
    background: rgba(99,102,241,.16);
    color: #fff;
    padding-left: 1.55rem;
}}
.nb-dd-sep {{
    height: 1px;
    background: rgba(255,255,255,.06);
    margin: .35rem .75rem;
    border-radius: 1px;
}}

/* ── Responsive ────────────────────────────────────────────── */
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
    <a class="nb-logo" href="pages/1_Dashboard.py">SmartStudy<span style="font-weight:400;opacity:.7;">AI</span></a>
    <div class="nb-menu" role="menubar">{nav_items_html}</div>
    <div class="nb-right">
        <div class="nb-avatar" id="nbAvatar" onclick="nbToggle()" role="button" aria-haspopup="true" aria-expanded="false">{user_initials}</div>
    </div>
</nav>

<div class="nb-dropdown" id="nbDropdown" role="menu">
    <span class="nb-dd-item">My Profile</span>
    <span class="nb-dd-item">Settings</span>
    <div class="nb-dd-sep"></div>
    <a class="nb-dd-item" href="?lang=en">English</a>
    <a class="nb-dd-item" href="?lang=hi">Hindi</a>
    <a class="nb-dd-item" href="?lang=kn">Kannada</a>
    <a class="nb-dd-item" href="?lang=ta">Tamil</a>
    <a class="nb-dd-item" href="?lang=te">Telugu</a>
    <div class="nb-dd-sep"></div>
    <a class="nb-dd-item" href="?logout=true">Sign Out</a>
</div>

<script>
function nbToggle() {{
    var dd = document.getElementById('nbDropdown');
    var av = document.getElementById('nbAvatar');
    var open = dd.classList.toggle('open');
    av.setAttribute('aria-expanded', open ? 'true' : 'false');
}}
document.addEventListener('click', function(e) {{
    var dd = document.getElementById('nbDropdown');
    var av = document.getElementById('nbAvatar');
    if (dd && av && !av.contains(e.target) && !dd.contains(e.target)) {{
        dd.classList.remove('open');
        av.setAttribute('aria-expanded', 'false');
    }}
}});
</script>
"""
    return " ".join(line.strip() for line in html.splitlines())

