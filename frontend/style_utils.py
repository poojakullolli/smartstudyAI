import streamlit as st
from translations import language_names

def inject_custom_css():
    """Inject premium custom CSS into all pages"""
    # Always inject particles and CSS - Streamlit handles deduplication
    # Inject floating particles
    st.markdown("""
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 2.5s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 1.5s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inject CSS
    st.markdown("""
    <style>
    /* ── Global Imports ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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
        --glass-gradient: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        
        /* Glass Effect */
        --glass-bg: rgba(17, 24, 39, 0.8);
        --glass-border: rgba(255, 255, 255, 0.1);
        --glass-border-hover: rgba(99, 102, 241, 0.3);
        
        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-glow: 0 0 40px rgba(99, 102, 241, 0.15);
        
        /* Typography */
        --font-sans: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
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
        --radius-2xl: 1.5rem;
        --radius-full: 9999px;
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-medium: 300ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
        
        /* Text Colors */
        --text-primary: #f9fafb;
        --text-secondary: #9ca3af;
        --text-muted: #6b7280;
        --text-disabled: #4b5563;
        
        /* Backgrounds */
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-tertiary: #334155;
        
        /* Card Design */
        --card-radius: 16px;
        --card-padding: 1.5rem;
    }

    /* Light mode override */
    [data-theme="light"] {
        --glass-bg: rgba(255, 255, 255, 0.9);
        --glass-border: rgba(0, 0, 0, 0.05);
        --text-primary: #111827;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --bg-primary: #f8fafc;
        --bg-secondary: #ffffff;
        --bg-tertiary: #f3f4f6;
    }

    * {
        font-family: var(--font-sans) !important;
        box-sizing: border-box;
    }

    /* Smooth page transitions */
    .page-transition {
        animation: pageIn var(--transition-medium) ease-out;
    }

    @keyframes pageIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    html, body, [class*="css"] {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-attachment: fixed;
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        25% { background-position: 50% 50%; }
        50% { background-position: 100% 50%; }
        75% { background-position: 50% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── Typography System ── */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600 !important;
        line-height: 1.2 !important;
        color: var(--text-primary) !important;
        margin: 0 0 var(--spacing-2) 0 !important;
    }

    h1 { font-size: var(--text-3xl) !important; }
    h2 { font-size: var(--text-2xl) !important; }
    h3 { font-size: var(--text-xl) !important; }
    h4 { font-size: var(--text-lg) !important; }

    p, span, div {
        color: var(--text-primary);
        line-height: 1.5;
    }

    .text-muted {
        color: var(--text-muted) !important;
    }

    .text-small {
        font-size: var(--text-sm) !important;
    }

    /* Subtle floating particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }

    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: float 15s infinite;
    }

    @keyframes float {
        0%, 100% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% {
            transform: translateY(-100vh) rotate(720deg);
            opacity: 0;
        }
    }

    /* ── Loading Spinner ── */
    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(99, 102, 241, 0.1);
        border-top-color: var(--primary-500);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-8);
        gap: var(--spacing-4);
    }

    /* ── Micro-interactions ── */
    .hover-lift {
        transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    }

    .hover-lift:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }

    .hover-scale {
        transition: transform var(--transition-fast);
    }

    .hover-scale:hover {
        transform: scale(1.05);
    }

    .hover-glow:hover {
        box-shadow: var(--shadow-glow);
    }

    /* Ripple effect */
    .ripple {
        position: relative;
        overflow: hidden;
    }

    .ripple::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        pointer-events: none;
        background-image: radial-gradient(circle, rgba(255,255,255,0.3) 10%, transparent 10.01%);
        background-repeat: no-repeat;
        background-position: 50%;
        transform: scale(10, 10);
        opacity: 0;
        transition: transform 0.5s, opacity 1s;
    }

    .ripple:active::after {
        transform: scale(0, 0);
        opacity: 0.3;
        transition: 0s;
    }

    /* ── Remove Streamlit Default UI Completely ── */
    #MainMenu { visibility: hidden; display: none !important; }
    footer { visibility: hidden; display: none !important; }
    header { visibility: hidden; display: none !important; height: 0px !important; }
    .stDeployButton { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .stSidebar { display: none !important; }
    .st-emotion-cache-18ni7ap { display: none !important; }
    .st-emotion-cache-1wrcr25 { margin-top: 0px !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="stBaseButton-header"] { display: none !important; }
    .block-container { 
        padding-top: 90px !important; 
        padding-left: 2rem !important; 
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Remove thick white line / border below dashboard */
    hr { display: none !important; }
    section.main > div { border: none !important; }
    .stHorizontalBlock, .stVerticalBlock { border: none !important; }
    div[data-testid="stVerticalBlock"] > div:not(:last-child) { 
        border-bottom: none !important; 
    }
    
    /* Remove all default Streamlit container borders and separators */
    div[data-testid="stAppViewContainer"] > section > div {
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Remove top border that appears after navbar */
    .main > .block-container {
        border: none !important;
        border-top: none !important;
    }
    
    /* Ensure seamless transition from navbar to content */
    .appview-container > section {
        border: none !important;
    }
    
    /* Remove any remaining default Streamlit dividers and borders */
    div[data-testid="stExpander"] {
        border: none !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stForm"] {
        border: none !important;
    }
    
    /* Make sure the main content area has no default borders */
    .main {
        border: none !important;
        border-top: none !important;
    }
    
    /* ── Navbar Styles ── */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: #0f172a;
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        z-index: 99999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .navbar-logo {
        font-size: 1.25rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .navbar-nav {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .nav-item {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        color: white;
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-1px);
    }
    
    .nav-item.active {
        color: white;
        background: rgba(102, 126, 234, 0.2);
    }
    
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nav-icon {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .nav-icon:hover {
        color: white;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .profile-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    
    .profile-avatar:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
    }
    
    .profile-dropdown {
        position: absolute;
        top: 60px;
        right: 2rem;
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        min-width: 200px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        display: none;
        z-index: 100000;
        overflow: hidden;
    }
    
    .profile-dropdown.show {
        display: block;
        animation: dropdownFade 0.2s ease-out;
    }
    
    @keyframes dropdownFade {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .dropdown-item {
        padding: 0.75rem 1rem;
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .dropdown-item:hover {
        background: rgba(102, 126, 234, 0.1);
        color: white;
    }
    
    .dropdown-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.1);
        margin: 0.25rem 0;
    }
    
    /* ── Professional Learning Cards ── */
    .learning-card {
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .learning-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    }
    
    .learning-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        margin: 0 0 0.25rem 0;
    }
    
    .card-subtitle {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 0 1rem 0;
    }
    
    .card-progress-container {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .card-progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: width 1s ease-out;
    }
    
    .card-status {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-bottom: 0.75rem;
    }
    
    .status-active {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
    }
    
    .status-completed {
        background: rgba(59, 130, 246, 0.2);
        color: #3b82f6;
    }
    
    .status-pending {
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
    }
    
    .card-action-btn {
        width: 100%;
        padding: 0.625rem 1rem;
        border-radius: 8px;
        border: none;
        font-weight: 500;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .card-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* ── Mobile Responsive Navbar ── */
    @media (max-width: 1024px) {
        .navbar-nav {
            display: none;
        }
        
        .mobile-menu-btn {
            display: block;
            color: rgba(255, 255, 255, 0.7);
            font-size: 1.5rem;
            cursor: pointer;
        }
        
        .mobile-menu {
            position: fixed;
            top: 64px;
            left: 0;
            right: 0;
            background: #0f172a;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 1rem;
            display: none;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .mobile-menu.show {
            display: flex;
        }
    }
    
    @media (min-width: 1025px) {
        .mobile-menu-btn {
            display: none;
        }
    }

    /* ── Premium Glass Card System ── */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-2xl);
        box-shadow: var(--shadow-lg);
        padding: var(--card-padding);
        transition: all var(--transition-medium);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
        opacity: 0;
        transition: opacity var(--transition-fast);
    }

    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--glass-border-hover);
    }

    .glass-card:hover::before {
        opacity: 1;
    }

    /* Card Header */
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--spacing-4);
        padding-bottom: var(--spacing-3);
        border-bottom: 1px solid var(--glass-border);
    }

    .card-title {
        font-size: var(--text-lg);
        font-weight: 600;
        margin: 0;
    }

    /* Card Body */
    .card-body {
        padding: var(--spacing-4) 0;
    }

    /* Card Footer */
    .card-footer {
        margin-top: var(--spacing-4);
        padding-top: var(--spacing-3);
        border-top: 1px solid var(--glass-border);
        display: flex;
        gap: var(--spacing-3);
        justify-content: flex-end;
    }



    /* ── Dashboard Components ── */
    .level-badge {
        display: inline-block;
        background: var(--primary-gradient);
        color: white;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        animation: badgeGlow 2s ease-in-out infinite;
    }

    @keyframes badgeGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.4); }
        50% { box-shadow: 0 0 35px rgba(118, 75, 162, 0.6); }
    }

    .xp-bar-container {
        height: 12px;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }

    .xp-bar-fill {
        height: 100%;
        background: var(--primary-gradient);
        border-radius: 10px;
        animation: xpFill 1.5s ease-out forwards;
    }

    @keyframes xpFill {
        from { width: 0%; }
    }

    .streak-fire {
        display: inline-block;
        animation: fireFlicker 0.5s ease-in-out infinite alternate;
    }

    @keyframes fireFlicker {
        0% { transform: scale(1) rotate(-5deg); }
        100% { transform: scale(1.15) rotate(5deg); }
    }

    /* ── Leaderboard Top 3 Cards ── */
    .leaderboard-top-card {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        transition: all var(--transition-medium);
        border: 1px solid var(--glass-border);
    }

    .leaderboard-top-card:hover {
        transform: translateY(-8px) scale(1.02);
    }

    .leaderboard-top-card.first {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.1));
        animation: topCardPulse 2s ease-in-out infinite;
    }

    @keyframes topCardPulse {
        0%, 100% { box-shadow: 0 8px 32px rgba(255, 215, 0, 0.2); }
        50% { box-shadow: 0 12px 48px rgba(255, 215, 0, 0.35); }
    }

    .crown-icon {
        font-size: 2.5rem;
        display: block;
        animation: crownBounce 1s ease-in-out infinite;
    }

    @keyframes crownBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    /* ── Quick Action Buttons ── */
    .quick-action-btn {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        cursor: pointer;
        transition: all var(--transition-fast);
        text-decoration: none;
        color: var(--text-primary);
        display: block;
    }

    .quick-action-btn:hover {
        transform: translateY(-4px);
        box-shadow: var(--soft-shadow);
        background: rgba(255, 255, 255, 0.9);
    }

    .quick-action-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }

    /* ── Metric Cards ── */
    div[data-testid="stMetric"] {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--glass-border);
        transition: all var(--transition-fast);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15);
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--soft-shadow);
    }

    /* ── Premium Buttons ── */
    div[data-testid="stButton"] > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--spacing-3) var(--spacing-6) !important;
        font-weight: 600 !important;
        font-size: var(--text-sm) !important;
        transition: all var(--transition-fast) !important;
        box-shadow: var(--shadow-md) !important;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
    }

    div[data-testid="stButton"] > button:active {
        transform: translateY(0) !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Secondary buttons */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(10px);
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: var(--glass-border-hover) !important;
    }

    /* ── Form Inputs ── */
    div[data-testid="stTextInput"] > div > input,
    div[data-testid="stNumberInput"] > div > input,
    div[data-testid="stTextArea"] > div > textarea,
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
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
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        outline: none !important;
    }

    /* ── Form Labels ── */
    label {
        font-weight: 500 !important;
        font-size: var(--text-sm) !important;
        color: var(--text-primary) !important;
        margin-bottom: var(--spacing-2) !important;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.5);
        padding: 8px;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
    }

    /* ── Circular XP Progress Indicator ── */
    .circular-progress {
        position: relative;
        width: 150px;
        height: 150px;
        margin: 0 auto;
    }

    .circular-progress svg {
        transform: rotate(-90deg);
    }

    .circular-progress circle {
        fill: none;
        stroke-width: 12;
        stroke-linecap: round;
    }

    .circular-progress .bg {
        stroke: rgba(0, 0, 0, 0.1);
    }

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
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ── Confetti Animation ── */
    .confetti-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 99999;
        overflow: hidden;
    }

    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        top: -10px;
        animation: confettiFall 3s ease-out forwards;
    }

    @keyframes confettiFall {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
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
        width: 12px;
        height: 12px;
        border-radius: 3px;
        transition: transform 0.2s ease;
    }

    .heatmap-day:hover {
        transform: scale(1.5);
    }

    .heatmap-day.level-0 { background: rgba(0, 0, 0, 0.1); }
    .heatmap-day.level-1 { background: rgba(102, 126, 234, 0.3); }
    .heatmap-day.level-2 { background: rgba(102, 126, 234, 0.5); }
    .heatmap-day.level-3 { background: rgba(102, 126, 234, 0.7); }
    .heatmap-day.level-4 { background: rgba(102, 126, 234, 1); }

    /* ── Typing Animation ── */
    .typing-text {
        overflow: hidden;
        border-right: 3px solid var(--primary-gradient);
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }

    @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
    }

    @keyframes blink-caret {
        from, to { border-color: transparent; }
        50% { border-color: #667eea; }
    }

    /* ── Quote Section ── */
    .motivational-quote {
        font-style: italic;
        font-size: 1.1rem;
        color: var(--text-secondary);
        text-align: center;
        padding: 1.5rem;
        border-left: 4px solid;
        border-image: var(--primary-gradient) 1;
        margin: 1rem 0;
        animation: quoteFadeIn 1s ease-out;
    }

    @keyframes quoteFadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ── Insights Card ── */
    .insights-card {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
    }

    .insights-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }

    .insight-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(102, 126, 234, 0.05);
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    .insight-item:hover {
        background: rgba(102, 126, 234, 0.1);
        transform: translateX(5px);
    }

    /* ── Focus Mode ── */
    .focus-mode {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 99999;
        background: #0a0a0f;
        transition: all 0.5s ease;
    }

    .focus-mode .pomodoro-timer {
        position: absolute;
        top: 50%;
        left: 50%;
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
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .focus-btn:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: scale(1.05);
    }

    /* ── Achievement Popup ── */
    .achievement-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.5);
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        z-index: 999999;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.3);
        animation: achievementUnlock 0.8s ease-out forwards;
    }

    @keyframes achievementUnlock {
        0% {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.3) rotate(-10deg);
        }
        50% {
            transform: translate(-50%, -50%) scale(1.1) rotate(5deg);
        }
        100% {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1) rotate(0deg);
        }
    }

    .achievement-icon {
        font-size: 5rem;
        display: block;
        animation: achievementBounce 0.5s ease-out 0.3s both;
    }

    @keyframes achievementBounce {
        0% { transform: scale(0); }
        50% { transform: scale(1.3); }
        100% { transform: scale(1); }
    }

    .achievement-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
        background: linear-gradient(135deg, #ffd700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ── Smart Greeting ── */
    .greeting-text {
        font-size: 2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #fff 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: greetingFade 1s ease-out;
    }

    @keyframes greetingFade {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ── Mobile Responsiveness ── */
    @media (max-width: 768px) {
        .auth-container {
            margin: 1rem;
            padding: 1rem;
        }
        
        .hero-title {
            font-size: 1.8rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }

        .circular-progress {
            width: 120px;
            height: 120px;
        }

        .heatmap-container {
            grid-template-columns: repeat(30, 12px);
        }

        .pomodoro-time {
            font-size: 4rem;
        }

        .achievement-popup {
            width: 90%;
            padding: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def add_language_selector():
    """Add language selector (deprecated - now in navbar profile dropdown)"""
    pass



def create_quick_action_button(icon, label, view_name=None):
    """Create a styled quick action button (deprecated for session state navigation)"""
    return f"""
    <div class="quick-action-btn" style="cursor: pointer;">
        <span class="quick-action-icon">{icon}</span>
        <strong>{label}</strong>
    </div>
    """

def create_navbar(current_page="Dashboard", user_initials="JD"):
    """Create SaaS-style fixed navigation bar with session state navigation"""
    nav_items = [
        ("Dashboard", "dashboard"),
        ("Study Planner", "planner"),
        ("Profile", "profile"),
    ]
    
    navbar_html = f"""
<div class="navbar">
    <div class="navbar-logo" style="cursor: pointer;" onclick="window.location.href='?page=1_Dashboard'">
        🧠 SmartStudyAI
    </div>
    
    <button class="mobile-menu-btn" onclick="toggleMobileMenu()">☰</button>
    
    <div class="navbar-nav">
"""
    
    for label, view in nav_items:
        active_class = "active" if label == current_page else ""
        page_map = {
            'dashboard': '1_Dashboard',
            'planner': '2_Study_Planner',
            'leaderboard': '6_Leaderboard',
            'challenges': '7_Challenges',
            'profile': '1_Dashboard#profile'
        }
        page = page_map.get(view, '1_Dashboard')
        navbar_html += f"""
        <div class="nav-item {active_class}" onclick="window.location.href='?page={page}'">{label}</div>
"""
    
    navbar_html += f"""
    </div>
    
    <div class="navbar-right">
        <span class="nav-icon">🔔</span>
        <div class="profile-avatar" onclick="toggleProfileDropdown()">{user_initials}</div>
    </div>
    
    <div class="profile-dropdown" id="profileDropdown">
        <div class="dropdown-item">
            <span>👤</span> My Profile
        </div>
        <div class="dropdown-item">
            <span>⚙️</span> Settings
        </div>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item" onclick="window.location.href='?logout=true'">
            <span>🚪</span> Logout
        </div>
    </div>
</div>

<div class="mobile-menu" id="mobileMenu">
"""
    
    for label, view in nav_items:
        active_class = "active" if label == current_page else ""
        page_map = {
            'dashboard': '1_Dashboard',
            'planner': '2_Study_Planner',
            'leaderboard': '6_Leaderboard',
            'challenges': '7_Challenges',
            'profile': '1_Dashboard#profile'
        }
        page = page_map.get(view, '1_Dashboard')
        navbar_html += f"""
    <div class="nav-item {active_class}" onclick="window.location.href='?page={page}'">{label}</div>
"""
    
    navbar_html += """
</div>

<script>
function toggleProfileDropdown() {
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('show');
}

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('show');
}

function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    html.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
}

document.addEventListener('click', function(e) {
    const dropdown = document.getElementById('profileDropdown');
    const avatar = document.querySelector('.profile-avatar');
    if (!avatar.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});
</script>
"""
    
    # Strip newlines to prevent Streamlit's markdown parser from rendering HTML as raw text
    return " ".join([line.strip() for line in navbar_html.splitlines()])

