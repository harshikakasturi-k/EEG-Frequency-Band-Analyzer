"""
ui/theme.py
-----------
Injects the global dark / glassmorphism / gradient CSS theme used across
every page of the EEG Frequency Band Analyzer. Import `inject_theme()`
once at the top of app.py.
"""

import streamlit as st

# Central color palette — used by both CSS below and Plotly chart theming
# (see utils/plotting.py) so the whole app stays visually consistent.
PALETTE = {
    "bg_gradient_1": "#0B0E14",
    "bg_gradient_2": "#141a2b",
    "bg_gradient_3": "#1a1030",
    "accent": "#7C4DFF",
    "accent_soft": "#9B7BFF",
    "cyan": "#22D3EE",
    "teal": "#2DD4BF",
    "pink": "#F472B6",
    "amber": "#FBBF24",
    "danger": "#F87171",
    "success": "#34D399",
    "text": "#E8ECF4",
    "text_dim": "#9AA4B8",
    "card_bg": "rgba(255, 255, 255, 0.045)",
    "card_border": "rgba(255, 255, 255, 0.09)",
}

# Distinct color per frequency band — reused in Frequency Bands + Band Power pages
BAND_COLORS = {
    "Delta": "#7C4DFF",
    "Theta": "#22D3EE",
    "Alpha": "#2DD4BF",
    "Beta": "#FBBF24",
    "Gamma": "#F472B6",
}

BAND_RANGES = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 13),
    "Beta": (13, 30),
    "Gamma": (30, 45),
}

BAND_DESCRIPTIONS = {
    "Delta": "Dominant during deep, dreamless sleep and unconscious states. High delta power while awake can indicate drowsiness or certain neurological conditions.",
    "Theta": "Linked to light sleep, deep relaxation, meditation, and memory encoding. Often prominent in children and during creative, drowsy states.",
    "Alpha": "Associated with relaxed wakefulness, typically strongest with eyes closed. A drop in alpha power usually accompanies visual attention or eye opening.",
    "Beta": "Reflects active, alert thinking, concentration, and problem solving. Elevated beta can also relate to anxiety or muscle tension artifacts.",
    "Gamma": "Linked to high-level cognitive processing, sensory binding, and focused attention. Often the smallest-amplitude, most artifact-sensitive band.",
}


def inject_theme():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* ---------- App background: animated gradient mesh ---------- */
        .stApp {{
            background: radial-gradient(circle at 15% 20%, {PALETTE['bg_gradient_3']} 0%, transparent 45%),
                        radial-gradient(circle at 85% 10%, #0d2b3a 0%, transparent 40%),
                        radial-gradient(circle at 50% 100%, #1a1030 0%, transparent 50%),
                        linear-gradient(160deg, {PALETTE['bg_gradient_1']} 0%, {PALETTE['bg_gradient_2']} 100%);
            background-attachment: fixed;
        }}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(19,24,38,0.98) 0%, rgba(11,14,20,0.98) 100%);
            border-right: 1px solid {PALETTE['card_border']};
        }}
        section[data-testid="stSidebar"] .stRadio label {{
            font-size: 0.95rem;
        }}

        /* ---------- Headings ---------- */
        h1, h2, h3 {{
            font-weight: 800 !important;
            letter-spacing: -0.02em;
        }}
        h1 {{
            background: linear-gradient(90deg, #ffffff 0%, {PALETTE['accent_soft']} 60%, {PALETTE['cyan']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* ---------- Glassmorphism card ---------- */
        .glass-card {{
            background: {PALETTE['card_bg']};
            border: 1px solid {PALETTE['card_border']};
            border-radius: 18px;
            padding: 1.4rem 1.6rem;
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            margin-bottom: 1rem;
        }}
        .glass-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(124, 77, 255, 0.5);
            box-shadow: 0 14px 40px rgba(124, 77, 255, 0.18);
        }}

        /* ---------- Hero section ---------- */
        .hero-wrap {{
            text-align: center;
            padding: 3.2rem 1rem 2.2rem 1rem;
        }}
        .hero-badge {{
            display: inline-block;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            background: rgba(124, 77, 255, 0.12);
            border: 1px solid rgba(124, 77, 255, 0.35);
            color: {PALETTE['accent_soft']};
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 1.2rem;
        }}
        .hero-title {{
            font-size: 3.1rem;
            font-weight: 800;
            line-height: 1.08;
            margin-bottom: 0.6rem;
            background: linear-gradient(90deg, #ffffff 0%, {PALETTE['accent_soft']} 55%, {PALETTE['cyan']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero-subtitle {{
            color: {PALETTE['text_dim']};
            font-size: 1.15rem;
            max-width: 720px;
            margin: 0 auto 1.6rem auto;
            line-height: 1.6;
        }}

        /* ---------- Feature card grid ---------- */
        .feature-card {{
            background: {PALETTE['card_bg']};
            border: 1px solid {PALETTE['card_border']};
            border-radius: 16px;
            padding: 1.3rem;
            height: 100%;
            transition: all 0.25s ease;
        }}
        .feature-card:hover {{
            border-color: rgba(124, 77, 255, 0.45);
            transform: translateY(-3px);
        }}
        .feature-icon {{
            font-size: 1.6rem;
            margin-bottom: 0.5rem;
        }}
        .feature-title {{
            font-weight: 700;
            font-size: 1.02rem;
            margin-bottom: 0.3rem;
            color: {PALETTE['text']};
        }}
        .feature-desc {{
            color: {PALETTE['text_dim']};
            font-size: 0.88rem;
            line-height: 1.5;
        }}

        /* ---------- Buttons ---------- */
        .stButton > button {{
            background: linear-gradient(135deg, {PALETTE['accent']} 0%, #5B2EFF 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            letter-spacing: 0.01em;
            box-shadow: 0 4px 18px rgba(124, 77, 255, 0.35);
            transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.015);
            box-shadow: 0 8px 26px rgba(124, 77, 255, 0.5);
            filter: brightness(1.08);
        }}
        .stButton > button:active {{
            transform: translateY(0px) scale(0.99);
        }}

        /* ---------- Metric-style stat pill ---------- */
        .stat-pill {{
            background: rgba(255,255,255,0.04);
            border: 1px solid {PALETTE['card_border']};
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            text-align: center;
        }}
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 800;
            color: {PALETTE['text']};
        }}
        .stat-label {{
            font-size: 0.78rem;
            color: {PALETTE['text_dim']};
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        /* ---------- Band pill badges ---------- */
        .band-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
            color: #0B0E14;
        }}

        /* ---------- Section divider ---------- */
        .section-label {{
            color: {PALETTE['text_dim']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }}

        /* ---------- Footer ---------- */
        .app-footer {{
            text-align: center;
            color: {PALETTE['text_dim']};
            font-size: 0.8rem;
            padding: 2rem 0 1rem 0;
            opacity: 0.7;
        }}

        /* Hide default streamlit chrome we don't want */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Tooltip icon */
        .info-tip {{
            color: {PALETTE['text_dim']};
            cursor: help;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
