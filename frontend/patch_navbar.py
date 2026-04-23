"""
One-shot script: replace create_navbar() in style_utils.py with the
upgraded SaaS-grade design.  Run once then delete this file.
"""
import re, pathlib, sys

target = pathlib.Path(__file__).parent / "style_utils.py"
content = target.read_text(encoding="utf-8")

NEW_FUNC = r'''
def create_navbar(current_page="Home", user_initials="JD"):
    """Premium SaaS-grade sticky horizontal navbar.

    Items  : Home | Study Planner | Study Tracker | Pomodoro | Focus Mode
    Design : deep dark glass, Poppins 600, rounded pill active highlight,
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
<!-- ══ SmartStudy AI — Premium Navbar ══ -->
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Kill ALL Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],[data-testid="stHeader"],
[data-testid="stStatusWidget"],[data-testid="stBaseButton-header"],
[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton {{ display:none!important; visibility:hidden!important; }}

/* ── Shell ─────────────────────────────────────────────────── */
.smartnav {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 66px;
    background: linear-gradient(180deg,
        rgba(5,7,18,.97) 0%,
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

/* Animated shimmer bottom glow */
.smartnav::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        #4f46e5 22%,
        #818cf8 45%,
        #a78bfa 55%,
        #818cf8 72%,
        #4f46e5 82%,
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

/* ── Menu row ──────────────────────────────────────────────── */
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

/* ── Nav items ─────────────────────────────────────────────── */
.nb-item {{
    font-family: 'Poppins', sans-serif;
    font-size: .855rem;
    font-weight: 600;          /* SemiBold */
    color: rgba(255,255,255,.46);
    text-decoration: none;
    padding: .42rem 1.1rem;
    border-radius: 50px;       /* pill */
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

/* Active pill */
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

/* ── Right zone & avatar ───────────────────────────────────── */
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
'''

# Locate the start of the old create_navbar function
match = re.search(r'\ndef create_navbar\(', content)
if not match:
    print("ERROR: 'create_navbar' definition not found in file")
    sys.exit(1)

new_content = content[:match.start()] + NEW_FUNC
target.write_text(new_content, encoding="utf-8")
print(f"SUCCESS — wrote {len(new_content):,} bytes to {target}")
