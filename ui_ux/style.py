from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from ui_ux.chart_factory import set_chart_theme


NAV_ITEMS = [
    {"label": "Story Mode", "path": "pages/00_Story_Mode.py", "icon": ":material/play_circle:"},
    {"label": "Dashboard", "path": "pages/01_Dashboard.py", "icon": ":material/dashboard:"},
    {"label": "Global Map", "path": "pages/02_Global_Climate_Map.py", "icon": ":material/public:"},
    {"label": "Climate Signals", "path": "pages/03_Climate_Signals.py", "icon": ":material/query_stats:"},
    {"label": "Risk Intelligence", "path": "pages/04_Risk_Intelligence.py", "icon": ":material/warning:"},
    {"label": "Predictions", "path": "pages/05_AI_Predictions.py", "icon": ":material/auto_graph:"},
    {"label": "Data Explorer", "path": "pages/06_Data_Explorer.py", "icon": ":material/travel_explore:"},
    {"label": "Research Lab", "path": "pages/07_Research_Lab.py", "icon": ":material/science:"},
    {"label": "Reports", "path": "pages/08_Reports.py", "icon": ":material/description:"},
    {"label": "Settings", "path": "pages/09_Settings.py", "icon": ":material/settings:"},
]


ATLAS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --atlas-bg-primary: #060a14;
        --atlas-bg-secondary: #0c1123;
        --atlas-card-bg: rgba(10, 16, 38, 0.42);
        --atlas-card-glass: rgba(8, 14, 32, 0.55);
        --atlas-card-border: rgba(255,255,255,0.10);
        --atlas-glass-shine: rgba(255,255,255,0.07);
        --atlas-glass-highlight: rgba(0,229,255,0.06);
        --atlas-glass-edge: rgba(255,255,255,0.12);
        --atlas-cyan: #00E5FF;
        --atlas-yellow: #FFD84D;
        --atlas-green: #6EFF9A;
        --atlas-pink: #FF5C8A;
        --atlas-purple: #A78BFA;
        --atlas-text: #FFFFFF;
        --atlas-text-secondary: #E2E8F0;
        --atlas-muted: #94A3B8;
        --atlas-subtle: #64748B;
        --atlas-shadow-glass: 0 4px 16px rgba(0,0,0,0.25), 0 12px 40px rgba(0,0,0,0.18), inset 0 1px 0 rgba(255,255,255,0.06);
        --atlas-shadow-hover: 0 8px 32px rgba(0,0,0,0.3), 0 20px 60px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.1);
        --atlas-shadow-liquid: 0 2px 8px rgba(0,0,0,0.2), 0 8px 32px rgba(0,0,0,0.15), inset 0 1px 0 rgba(255,255,255,0.08), inset 0 -1px 0 rgba(0,0,0,0.12);
        --atlas-radius-sm: 16px;
        --atlas-radius-md: 22px;
        --atlas-radius-lg: 28px;
        --atlas-radius-xl: 36px;
        --atlas-space-xs: 0.25rem;
        --atlas-space-sm: 0.5rem;
        --atlas-space-md: 1rem;
        --atlas-space-lg: 1.75rem;
        --atlas-space-xl: 2.5rem;
        --atlas-glass-blur: 28px;
        --atlas-color-success: #6EFF9A;
        --atlas-color-warning: #FFD84D;
        --atlas-color-error: #FF5C8A;
        --atlas-color-info: #00E5FF;
        --atlas-focus-ring: 0 0 0 3px rgba(0,229,255,0.35);
        --atlas-font-mono: 'Fira Code', 'JetBrains Mono', monospace;
        --atlas-font-body: 'Fira Sans', 'Inter', sans-serif;
        --atlas-font-heading: 'Space Grotesk', sans-serif;
        --atlas-transition: 350ms cubic-bezier(0.22, 1, 0.36, 1);
        --atlas-transition-fast: 200ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    html, body, [class*="css"] {
        font-family: var(--atlas-font-body);
    }

    .stApp {
        background:
            linear-gradient(rgba(4, 8, 18, 0.55), rgba(4, 8, 18, 0.75));
        background-color: #060a14;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse at 20% 30%, rgba(0,229,255,0.06), transparent 35%),
            radial-gradient(ellipse at 80% 70%, rgba(167,139,250,0.05), transparent 35%);
        pointer-events: none;
        animation: atlasBlob 20s ease-in-out infinite alternate;
    }

    @keyframes atlasBlob {
        0% { transform: scale(1) rotate(0deg); opacity: 0.6; }
        50% { transform: scale(1.1) rotate(2deg); opacity: 0.8; }
        100% { transform: scale(0.95) rotate(-1deg); opacity: 0.5; }
    }

    @keyframes atlasCaustics {
        0% { background-position: 0% 0%, 100% 100%; }
        33% { background-position: 30% 60%, 70% 40%; }
        66% { background-position: 60% 20%, 40% 80%; }
        100% { background-position: 0% 0%, 100% 100%; }
    }

    @keyframes atlasShimmer {
        0% { transform: translateX(-100%) skewX(-15deg); }
        100% { transform: translateX(200%) skewX(-15deg); }
    }

    @keyframes atlasLiquidGlass {
        0% { border-radius: 22px 28px 24px 30px; }
        25% { border-radius: 28px 22px 30px 24px; }
        50% { border-radius: 24px 30px 22px 28px; }
        75% { border-radius: 30px 24px 28px 22px; }
        100% { border-radius: 22px 28px 24px 30px; }
    }

    @keyframes atlasRefract {
        0% { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
        25% { clip-path: polygon(0 2%, 98% 0, 100% 97%, 2% 100%); }
        50% { clip-path: polygon(1% 0, 100% 1%, 99% 100%, 0 99%); }
        75% { clip-path: polygon(0 1%, 99% 0, 100% 99%, 1% 100%); }
        100% { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%); }
    }

    @keyframes atlasPulseGlow {
        0%, 100% { box-shadow: var(--atlas-shadow-liquid), 0 0 20px rgba(0,229,255,0.0); }
        50% { box-shadow: var(--atlas-shadow-liquid), 0 0 30px rgba(0,229,255,0.08); }
    }

    #MainMenu {
        display: none;
    }

    footer {
        visibility: hidden;
    }

    button[data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        background: rgba(0,229,255,0.1) !important;
        border: 1px solid rgba(0,229,255,0.3) !important;
        border-radius: 8px !important;
        color: var(--atlas-cyan) !important;
        padding: 0.4rem !important;
        min-width: 2.2rem !important;
        min-height: 2.2rem !important;
        backdrop-filter: blur(12px) !important;
    }

    button[data-testid="stSidebarCollapsedControl"]:hover,
    button[data-testid="stSidebarCollapseButton"]:hover {
        background: rgba(0,229,255,0.2) !important;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    [data-testid="stAppViewContainer"] > .main {
        color: var(--atlas-text);
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 1.2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: var(--atlas-font-heading);
        color: var(--atlas-text);
        letter-spacing: -0.02em;
        font-weight: 600;
        text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    }

    p, li, label, div[data-testid="stMarkdownContainer"], span {
        color: var(--atlas-text-secondary);
    }

    code, pre, .atlas-data-font {
        font-family: var(--atlas-font-mono) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(8, 13, 28, 0.75) 0%, rgba(6, 10, 20, 0.85) 100%) !important;
        backdrop-filter: blur(36px) saturate(1.6) !important;
        -webkit-backdrop-filter: blur(36px) saturate(1.6) !important;
        border-right: 1px solid var(--atlas-glass-edge) !important;
        box-shadow: 4px 0 32px rgba(0,0,0,0.35), inset -1px 0 0 rgba(255,255,255,0.05), inset 0 0 80px rgba(0,229,255,0.02) !important;
    }

    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child,
    section[data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(8, 13, 28, 0.75) 0%, rgba(6, 10, 20, 0.85) 100%) !important;
        backdrop-filter: blur(36px) saturate(1.6) !important;
        -webkit-backdrop-filter: blur(36px) saturate(1.6) !important;
    }

    [data-testid="stSidebar"] > div:first-child::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 1px;
        height: 100%;
        background: linear-gradient(180deg, transparent 10%, rgba(0,229,255,0.15) 50%, transparent 90%);
        pointer-events: none;
        z-index: 1;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 0.8rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    [data-testid="stSidebar"] a {
        color: var(--atlas-text-secondary) !important;
        text-decoration: none !important;
        transition: color var(--atlas-transition);
    }

    [data-testid="stSidebar"] a:hover {
        color: var(--atlas-text) !important;
    }

    .atlas-shell-topbar {
        display: grid;
        grid-template-columns: 1.1fr 1.0fr 0.6fr;
        gap: 0.75rem;
        margin-bottom: 1.2rem;
        animation: atlasFadeUp 0.5s ease-out;
    }

    .atlas-topbar-card,
    .atlas-hero,
    .atlas-panel,
    .atlas-feature-card,
    .atlas-info-banner,
    .atlas-metric-card,
    .atlas-source-card,
    .atlas-section-head,
    .atlas-story-panel,
    .atlas-nav-panel,
    .atlas-stat-card,
    .atlas-source-mini {
        background: var(--atlas-card-bg);
        border: 1px solid var(--atlas-card-border);
        border-radius: var(--atlas-radius-md);
        box-shadow: var(--atlas-shadow-liquid);
        backdrop-filter: blur(var(--atlas-glass-blur)) saturate(1.6);
        -webkit-backdrop-filter: blur(var(--atlas-glass-blur)) saturate(1.6);
        transition: box-shadow var(--atlas-transition), border-color var(--atlas-transition), transform var(--atlas-transition);
        position: relative;
        overflow: hidden;
    }

    .atlas-topbar-card::before,
    .atlas-hero::before,
    .atlas-feature-card::before,
    .atlas-source-card::before,
    .atlas-metric-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            radial-gradient(ellipse at 20% 15%, var(--atlas-glass-shine), transparent 50%),
            radial-gradient(ellipse at 80% 85%, rgba(0,229,255,0.03), transparent 50%);
        pointer-events: none;
        opacity: 1;
        z-index: 1;
    }

    .atlas-topbar-card::after,
    .atlas-feature-card::after,
    .atlas-source-card::after,
    .atlas-metric-card::after {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 60%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
        pointer-events: none;
        z-index: 2;
        transition: none;
        transform: skewX(-15deg);
    }

    .atlas-feature-card:hover::after,
    .atlas-source-card:hover::after,
    .atlas-metric-card:hover::after {
        animation: atlasShimmer 0.8s ease-out;
    }

    .atlas-feature-card:hover,
    .atlas-source-card:hover,
    .atlas-metric-card:hover {
        border-color: var(--atlas-glass-edge);
        box-shadow: var(--atlas-shadow-hover), 0 0 40px rgba(0,229,255,0.06);
        transform: translateY(-3px) scale(1.005);
    }

    .atlas-topbar-card {
        padding: 0.85rem 1rem;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .atlas-topbar-card h2 {
        margin: 0;
        font-size: 1.15rem;
        font-weight: 600;
    }

    .atlas-topbar-card p {
        margin: 0.2rem 0 0 0;
        color: var(--atlas-muted);
        font-size: 0.85rem;
        line-height: 1.4;
    }

    .atlas-chip-row {
        display: flex;
        gap: 0.45rem;
        flex-wrap: wrap;
        align-items: center;
    }

    .atlas-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.3rem 0.6rem;
        border-radius: 12px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        color: var(--atlas-text-secondary);
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        line-height: 1;
        backdrop-filter: blur(12px) saturate(1.3);
        -webkit-backdrop-filter: blur(12px) saturate(1.3);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 2px 8px rgba(0,0,0,0.15);
    }

    .atlas-chip.cyan { color: var(--atlas-cyan); background: rgba(0,229,255,0.10); border-color: rgba(0,229,255,0.18); }
    .atlas-chip.yellow { color: var(--atlas-yellow); background: rgba(255,216,77,0.10); border-color: rgba(255,216,77,0.18); }
    .atlas-chip.green { color: var(--atlas-green); background: rgba(110,255,154,0.10); border-color: rgba(110,255,154,0.18); }
    .atlas-chip.pink { color: var(--atlas-pink); background: rgba(255,92,138,0.10); border-color: rgba(255,92,138,0.18); }

    .atlas-side-brand {
        padding: 0.85rem;
        margin-bottom: 0.75rem;
        border: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-md);
        background: linear-gradient(135deg, rgba(0,229,255,0.08) 0%, var(--atlas-card-bg) 100%);
        backdrop-filter: blur(20px) saturate(1.4);
        -webkit-backdrop-filter: blur(20px) saturate(1.4);
        box-shadow: var(--atlas-shadow-liquid);
        position: relative;
        overflow: hidden;
    }

    .atlas-side-brand::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,229,255,0.2), transparent);
        pointer-events: none;
    }

    .atlas-sidebar-logo-wrap {
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-lg);
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, var(--atlas-card-bg) 100%);
        backdrop-filter: blur(24px) saturate(1.5);
        -webkit-backdrop-filter: blur(24px) saturate(1.5);
        box-shadow: var(--atlas-shadow-liquid);
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .atlas-sidebar-logo-wrap::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.04), transparent 60%);
        pointer-events: none;
    }

    .atlas-sidebar-logo-wrap::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0,229,255,0.15), rgba(167,139,250,0.1), transparent);
        pointer-events: none;
    }

    .atlas-sidebar-logo-wrap img {
        display: block;
        max-width: 100%;
        height: auto;
        mix-blend-mode: screen;
        filter: drop-shadow(0 2px 8px rgba(0,229,255,0.15)) drop-shadow(0 4px 16px rgba(0,0,0,0.3));
    }

    html[data-theme="light"] .atlas-sidebar-logo-wrap img {
        mix-blend-mode: multiply;
        filter: drop-shadow(0 2px 8px rgba(0,229,255,0.1)) drop-shadow(0 4px 16px rgba(0,0,0,0.08));
    }

    .atlas-side-brand .atlas-kicker {
        margin-bottom: 0.3rem;
        font-size: 0.65rem;
    }

    .atlas-side-section {
        margin: 0.75rem 0 0.4rem 0;
        padding: 0 0.3rem;
        font-size: 0.65rem;
        color: var(--atlas-subtle);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
    }

    .atlas-active-page {
        padding: 0.45rem 0.65rem;
        border: 1px solid rgba(0,229,255,0.25);
        border-radius: var(--atlas-radius-sm);
        background: linear-gradient(135deg, rgba(0,229,255,0.10) 0%, rgba(167,139,250,0.08) 100%);
        font-family: var(--atlas-font-mono);
        font-size: 0.72rem;
        color: var(--atlas-cyan);
        margin-bottom: 0.5rem;
        backdrop-filter: blur(14px) saturate(1.3);
        -webkit-backdrop-filter: blur(14px) saturate(1.3);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 2px 8px rgba(0,229,255,0.08);
    }

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a,
    .stFormSubmitButton > button {
        border: none !important;
        border-radius: var(--atlas-radius-sm) !important;
        background: linear-gradient(135deg, rgba(0,229,255,0.9) 0%, rgba(167,139,250,0.9) 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-family: var(--atlas-font-body) !important;
        box-shadow: var(--atlas-shadow-liquid) !important;
        min-height: 2.5rem !important;
        backdrop-filter: blur(12px) saturate(1.5) !important;
        -webkit-backdrop-filter: blur(12px) saturate(1.5) !important;
        transition: transform var(--atlas-transition-fast), box-shadow var(--atlas-transition-fast), background var(--atlas-transition-fast) !important;
        letter-spacing: 0.02em;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::after,
    .stDownloadButton > button::after,
    .stFormSubmitButton > button::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: var(--atlas-shadow-hover), 0 0 30px rgba(0,229,255,0.12) !important;
        background: linear-gradient(135deg, rgba(0,229,255,1) 0%, rgba(167,139,250,1) 100%) !important;
    }

    .stButton > button:active,
    .stDownloadButton > button:active {
        transform: translateY(0) !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stDateInput input,
    .stSelectbox [data-baseweb="select"],
    .stMultiSelect [data-baseweb="select"] {
        color: var(--atlas-text) !important;
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--atlas-glass-edge) !important;
        border-radius: var(--atlas-radius-sm) !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.15), 0 1px 0 rgba(255,255,255,0.04) !important;
        backdrop-filter: blur(12px) saturate(1.3) !important;
        -webkit-backdrop-filter: blur(12px) saturate(1.3) !important;
        transition: border-color var(--atlas-transition-fast), box-shadow var(--atlas-transition-fast);
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--atlas-cyan) !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.15), 0 0 0 3px rgba(0,229,255,0.15), 0 0 20px rgba(0,229,255,0.08) !important;
    }

    .stSlider [data-baseweb="slider"] {
        padding-top: 0.5rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: 0;
        box-shadow: none;
        color: var(--atlas-muted);
        padding: 0.5rem 0.75rem;
        border-bottom: 2px solid transparent;
        transition: color var(--atlas-transition), border-color var(--atlas-transition);
        margin-bottom: -1px;
        font-size: 0.85rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--atlas-text);
        background: transparent;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--atlas-cyan);
        background: transparent;
        border-bottom-color: var(--atlas-cyan);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, var(--atlas-card-glass) 0%, var(--atlas-card-bg) 100%);
        border: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-md);
        box-shadow: var(--atlas-shadow-liquid);
        backdrop-filter: blur(var(--atlas-glass-blur)) saturate(1.5);
        -webkit-backdrop-filter: blur(var(--atlas-glass-blur)) saturate(1.5);
        padding: 0.7rem 0.85rem;
        transition: border-color var(--atlas-transition), transform var(--atlas-transition), box-shadow var(--atlas-transition);
        position: relative;
        overflow: hidden;
    }

    [data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 20% 15%, rgba(255,255,255,0.05), transparent 50%);
        pointer-events: none;
    }

    [data-testid="stMetric"]:hover {
        border-color: var(--atlas-glass-edge);
        box-shadow: var(--atlas-shadow-hover), 0 0 30px rgba(0,229,255,0.06);
        transform: translateY(-2px);
    }

    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"],
    [data-testid="stImage"],
    [data-testid="stExpander"] {
        background: transparent;
        border-radius: var(--atlas-radius-sm);
        animation: atlasFadeUp 0.5s ease-out;
    }

    .atlas-hero {
        padding: 2.5rem 2.5rem 2rem;
        margin-bottom: 1.5rem;
        background:
            radial-gradient(ellipse at 100% 0%, rgba(0,229,255,0.10), transparent 40%),
            radial-gradient(ellipse at 0% 100%, rgba(167,139,250,0.07), transparent 40%),
            linear-gradient(135deg, var(--atlas-card-glass) 0%, var(--atlas-card-bg) 100%);
        border: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-xl);
        position: relative;
        overflow: hidden;
        box-shadow: var(--atlas-shadow-liquid), inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .atlas-hero::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--atlas-cyan), var(--atlas-purple), transparent);
        opacity: 0.4;
    }

    .atlas-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.25rem 0.6rem;
        border-radius: 8px;
        background: rgba(0,229,255,0.08);
        border: 1px solid rgba(0,229,255,0.15);
        color: var(--atlas-cyan);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        line-height: 1;
        backdrop-filter: blur(6px);
    }

    .atlas-hero h1 {
        margin: 0.8rem 0 0.3rem 0;
        font-size: clamp(2.5rem, 4.5vw, 4.5rem);
        line-height: 1;
        font-weight: 700;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .atlas-tagline {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--atlas-cyan);
    }

    .atlas-subtitle {
        margin-top: 0.75rem;
        max-width: 720px;
        color: var(--atlas-muted);
        font-size: 0.95rem;
        line-height: 1.7;
    }

    .atlas-section-head,
    .atlas-feature-card,
    .atlas-panel,
    .atlas-info-banner,
    .atlas-story-panel,
    .atlas-source-card,
    .atlas-metric-card,
    .atlas-stat-card,
    .atlas-source-mini {
        padding: 1rem 1.15rem;
        margin-bottom: 0.75rem;
    }

    .atlas-section-head {
        border-left: 3px solid var(--atlas-cyan);
        border-radius: 0 var(--atlas-radius-sm) var(--atlas-radius-sm) 0;
        padding: 0.6rem 1rem;
        margin-bottom: 0.65rem;
        background: rgba(0,229,255,0.03);
    }

    .atlas-section-head h3 {
        margin: 0 0 0.2rem 0;
        font-size: 1rem;
        font-weight: 600;
    }

    .atlas-section-head p {
        margin: 0;
        color: var(--atlas-muted);
        font-size: 0.82rem;
        line-height: 1.5;
    }

    .atlas-feature-card h4,
    .atlas-panel h4,
    .atlas-story-panel h4,
    .atlas-source-card h4 {
        margin: 0 0 0.3rem 0;
        font-size: 0.92rem;
        font-weight: 600;
    }

    .atlas-feature-card p,
    .atlas-panel p,
    .atlas-info-banner p,
    .atlas-story-panel p,
    .atlas-source-card p {
        margin: 0;
        color: var(--atlas-muted);
        font-size: 0.82rem;
        line-height: 1.55;
    }

    .atlas-info-banner {
        background: linear-gradient(135deg, rgba(0,229,255,0.08) 0%, var(--atlas-card-bg) 100%);
        border-left: 3px solid var(--atlas-cyan);
        border-color: var(--atlas-glass-edge);
        backdrop-filter: blur(var(--atlas-glass-blur)) saturate(1.4);
        -webkit-backdrop-filter: blur(var(--atlas-glass-blur)) saturate(1.4);
        box-shadow: var(--atlas-shadow-liquid);
    }

    .atlas-card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.75rem;
    }

    .atlas-stat-label,
    .atlas-source-label,
    .atlas-metric-label {
        display: block;
        font-size: 0.7rem;
        color: var(--atlas-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }

    .atlas-stat-value,
    .atlas-source-value,
    .atlas-metric-value {
        display: block;
        color: var(--atlas-text);
        font-family: var(--atlas-font-heading);
        font-weight: 700;
    }

    .atlas-metric-value {
        font-size: 1.65rem;
        line-height: 1.1;
    }

    .atlas-metric-sub {
        margin-top: 0.3rem;
        color: var(--atlas-muted);
        font-size: 0.78rem;
        line-height: 1.4;
    }

    .atlas-story-label {
        color: var(--atlas-pink);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .atlas-stepper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 0.6rem;
        margin: 0.2rem 0 1rem 0;
    }

    .atlas-step-chip {
        padding: 0.75rem;
        border: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-sm);
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, var(--atlas-card-bg) 100%);
        backdrop-filter: blur(16px) saturate(1.3);
        -webkit-backdrop-filter: blur(16px) saturate(1.3);
        box-shadow: var(--atlas-shadow-liquid);
        transition: border-color var(--atlas-transition), background var(--atlas-transition), box-shadow var(--atlas-transition);
    }

    .atlas-step-chip:hover {
        border-color: var(--atlas-glass-edge);
        box-shadow: var(--atlas-shadow-hover), 0 0 20px rgba(0,229,255,0.05);
    }

    .atlas-step-chip.active {
        background: rgba(0,229,255,0.06);
        border-color: rgba(0,229,255,0.2);
    }

    .atlas-step-chip strong {
        font-size: 0.85rem;
        font-weight: 600;
    }

    .atlas-step-chip span {
        display: block;
        color: var(--atlas-muted);
        font-size: 0.78rem;
        margin-top: 0.15rem;
    }

    .atlas-story-panel {
        border-left: 3px solid var(--atlas-cyan);
        border-radius: 0 var(--atlas-radius-sm) var(--atlas-radius-sm) 0;
    }

    .atlas-status {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        background: rgba(110,255,154,0.08);
        border: 1px solid rgba(110,255,154,0.15);
        color: var(--atlas-green);
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        line-height: 1;
        backdrop-filter: blur(4px);
    }

    .atlas-status.warning {
        color: var(--atlas-yellow);
        background: rgba(255,216,77,0.08);
        border-color: rgba(255,216,77,0.15);
    }

    .atlas-status.neutral {
        color: var(--atlas-muted);
        background: rgba(255,255,255,0.04);
        border-color: rgba(255,255,255,0.08);
    }

    .atlas-nav-caption {
        color: var(--atlas-muted);
        font-size: 0.78rem;
        line-height: 1.4;
    }

    @keyframes atlasFadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes atlasSkeleton {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    @keyframes atlasLiquid {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 20%; }
        50% { background-position: 50% 100%; }
        75% { background-position: 0% 60%; }
        100% { background-position: 0% 0%; }
    }

    .atlas-skeleton {
        background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.06) 50%, rgba(255,255,255,0.03) 75%);
        background-size: 200% 100%;
        animation: atlasSkeleton 1.5s ease-in-out infinite;
        border-radius: var(--atlas-radius-sm);
        min-height: 1rem;
    }

    .atlas-focusable:focus-visible,
    .atlas-card-focus:focus-visible,
    [tabindex]:focus-visible,
    button:focus-visible,
    a:focus-visible,
    [role="button"]:focus-visible {
        outline: none;
        box-shadow: var(--atlas-focus-ring) !important;
    }

    .atlas-blob {
        position: fixed;
        border-radius: 50%;
        filter: blur(80px);
        pointer-events: none;
        opacity: 0.15;
        animation: atlasBlob 18s ease-in-out infinite alternate;
    }

    @keyframes atlasBlob {
        0% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, -20px) scale(1.1); }
        66% { transform: translate(-20px, 10px) scale(0.9); }
        100% { transform: translate(10px, -30px) scale(1.05); }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
        .atlas-skeleton { animation: none; }
        .stApp { animation: none; }
        .stApp::before { animation: none; }
    }

    @media (max-width: 1200px) {
        .atlas-hero h1 { font-size: clamp(2rem, 4vw, 3.5rem); }
        .atlas-metric-value { font-size: 1.35rem; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    }

    @media (max-width: 1100px) {
        .atlas-shell-topbar { grid-template-columns: 1fr 1fr; }
        .main .block-container { padding-top: 1rem; }
    }

    @media (max-width: 900px) {
        .atlas-card-grid { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); }
        .atlas-stepper { grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); }
        .atlas-shell-topbar { grid-template-columns: 1fr; }
    }

    @media (max-width: 800px) {
        .atlas-hero { padding: 1.5rem; }
        .atlas-hero h1 { font-size: 2.2rem; }
        .atlas-topbar-card { min-height: 60px; padding: 0.6rem 0.85rem; }
    }

    @media (max-width: 640px) {
        .atlas-hero { padding: 1.2rem; }
        .atlas-hero h1 { font-size: 1.8rem; }
        .atlas-tagline { font-size: 0.85rem; }
        .atlas-subtitle { font-size: 0.82rem; }
        .atlas-metric-value { font-size: 1.15rem; }
        .atlas-section-head,
        .atlas-feature-card,
        .atlas-panel,
        .atlas-metric-card { padding: 0.7rem 0.85rem; }
        [data-testid="stSidebar"] { min-width: 200px; }
    }

    @media (max-width: 480px) {
        .atlas-hero h1 { font-size: 1.5rem; }
        .atlas-tagline { font-size: 0.78rem; }
        .atlas-chips-row { flex-direction: column; align-items: stretch; }
        .atlas-chip { justify-content: center; }
        [data-testid="stSidebar"] { min-width: 160px; }
    }

</style>
"""

ATLAS_CSS_LIGHT_OVERRIDES = """
<style>
    html[data-theme="light"] {
        --atlas-bg-primary: #f0f4f8;
        --atlas-bg-secondary: #e2e8f0;
        --atlas-card-bg: rgba(255, 255, 255, 0.55);
        --atlas-card-glass: rgba(255, 255, 255, 0.65);
        --atlas-card-border: rgba(0, 0, 0, 0.08);
        --atlas-glass-shine: rgba(255,255,255,0.6);
        --atlas-glass-highlight: rgba(255,255,255,0.4);
        --atlas-glass-edge: rgba(0, 0, 0, 0.10);
        --atlas-text: #0f172a;
        --atlas-text-secondary: #1e293b;
        --atlas-muted: #475569;
        --atlas-subtle: #64748b;
        --atlas-shadow-glass: 0 4px 16px rgba(0,0,0,0.06), 0 12px 40px rgba(0,0,0,0.04), inset 0 1px 0 rgba(255,255,255,0.8);
        --atlas-shadow-hover: 0 8px 32px rgba(0,0,0,0.08), 0 20px 60px rgba(0,0,0,0.06), inset 0 1px 0 rgba(255,255,255,0.9);
        --atlas-shadow-liquid: 0 2px 8px rgba(0,0,0,0.05), 0 8px 32px rgba(0,0,0,0.04), inset 0 1px 0 rgba(255,255,255,0.8), inset 0 -1px 0 rgba(0,0,0,0.03);
        --atlas-color-success: #16a34a;
        --atlas-color-warning: #ca8a04;
        --atlas-color-error: #dc2626;
        --atlas-color-info: #0891b2;
        --atlas-focus-ring: 0 0 0 3px rgba(0,229,255,0.3);
    }

    html[data-theme="light"] .stApp {
        background:
            linear-gradient(rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.55));
        background-color: #f0f4f8;
    }

    html[data-theme="light"] .stApp::before {
        opacity: 0;
        animation: none;
    }

    html[data-theme="light"] h1, html[data-theme="light"] h2, html[data-theme="light"] h3,
    html[data-theme="light"] h4, html[data-theme="light"] h5, html[data-theme="light"] h6 {
        text-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }

    html[data-theme="light"] [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.85) 0%, rgba(240, 244, 248, 0.9) 100%) !important;
        backdrop-filter: blur(36px) saturate(1.6) !important;
        -webkit-backdrop-filter: blur(36px) saturate(1.6) !important;
        border-right: 1px solid rgba(0,0,0,0.08) !important;
        box-shadow: 4px 0 32px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.9) !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"][aria-expanded="true"] > div:first-child,
    html[data-theme="light"] section[data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.85) 0%, rgba(240, 244, 248, 0.9) 100%) !important;
        backdrop-filter: blur(36px) saturate(1.6) !important;
        -webkit-backdrop-filter: blur(36px) saturate(1.6) !important;
    }

    html[data-theme="light"] h1, html[data-theme="light"] h2, html[data-theme="light"] h3,
    html[data-theme="light"] h4, html[data-theme="light"] h5, html[data-theme="light"] h6 {
        color: #0f172a !important;
        text-shadow: none !important;
    }

    html[data-theme="light"] p,
    html[data-theme="light"] li,
    html[data-theme="light"] label,
    html[data-theme="light"] span,
    html[data-theme="light"] div[data-testid="stMarkdownContainer"] {
        color: #1e293b !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"] a {
        color: #334155 !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"] a:hover {
        color: #0f172a !important;
    }

    html[data-theme="light"] .atlas-side-section {
        color: #64748b !important;
    }

    html[data-theme="light"] .atlas-kicker {
        color: #0891b2 !important;
        background: rgba(8,145,178,0.08) !important;
        border-color: rgba(8,145,178,0.15) !important;
    }

    html[data-theme="light"] .atlas-active-page {
        color: #0891b2 !important;
        background: linear-gradient(135deg, rgba(8,145,178,0.10) 0%, rgba(8,145,178,0.05) 100%) !important;
        border-color: rgba(8,145,178,0.25) !important;
    }

    html[data-theme="light"] .atlas-hero {
        background:
            radial-gradient(ellipse at 100% 0%, rgba(0,229,255,0.06), transparent 40%),
            radial-gradient(ellipse at 0% 100%, rgba(167,139,250,0.04), transparent 40%);
        background-color: rgba(255,255,255,0.8);
    }

    html[data-theme="light"] .atlas-hero h1 {
        background: linear-gradient(135deg, #0f172a 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    html[data-theme="light"] .stButton > button,
    html[data-theme="light"] .stDownloadButton > button,
    html[data-theme="light"] .stLinkButton > a,
    html[data-theme="light"] .stFormSubmitButton > button {
        background: linear-gradient(135deg, rgba(0,229,255,0.9) 0%, rgba(167,139,250,0.9) 100%) !important;
        color: #FFFFFF !important;
        box-shadow: var(--atlas-shadow-liquid) !important;
    }

    html[data-theme="light"] .stTextInput input,
    html[data-theme="light"] .stNumberInput input,
    html[data-theme="light"] .stTextArea textarea,
    html[data-theme="light"] .stDateInput input,
    html[data-theme="light"] .stSelectbox [data-baseweb="select"],
    html[data-theme="light"] .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.7) !important;
        border-color: var(--atlas-glass-edge) !important;
        color: #0f172a !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.8) !important;
        backdrop-filter: blur(16px) saturate(1.4) !important;
        -webkit-backdrop-filter: blur(16px) saturate(1.4) !important;
    }

    html[data-theme="light"] .atlas-chip {
        background: rgba(0,0,0,0.04);
        border-color: var(--atlas-glass-edge);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.8), 0 2px 8px rgba(0,0,0,0.06);
    }

    html[data-theme="light"] .atlas-section-head {
        background: rgba(0,229,255,0.04);
    }

    html[data-theme="light"] .atlas-info-banner {
        background: linear-gradient(135deg, rgba(0,229,255,0.04) 0%, transparent 100%);
    }

    html[data-theme="light"] .atlas-kicker {
        background: rgba(0,229,255,0.06);
        border-color: rgba(0,229,255,0.15);
    }

    html[data-theme="light"] .atlas-active-page {
        background: linear-gradient(135deg, rgba(0,229,255,0.06) 0%, rgba(167,139,250,0.04) 100%);
    }

    html[data-theme="light"] .atlas-step-chip {
        background: rgba(0,0,0,0.02);
        border-color: rgba(0,0,0,0.06);
    }

    html[data-theme="light"] .atlas-step-chip.active {
        background: rgba(0,229,255,0.06);
        border-color: rgba(0,229,255,0.2);
    }

    html[data-theme="light"] .atlas-status {
        background: rgba(22,163,74,0.08);
        border-color: rgba(22,163,74,0.15);
        color: #16a34a;
    }

    html[data-theme="light"] .atlas-status.warning {
        color: #ca8a04;
        background: rgba(202,138,4,0.08);
        border-color: rgba(202,138,4,0.15);
    }

    html[data-theme="light"] .atlas-status.neutral {
        color: #64748b;
        background: rgba(0,0,0,0.03);
        border-color: rgba(0,0,0,0.06);
    }

    html[data-theme="light"] .atlas-feature-card:hover,
    html[data-theme="light"] .atlas-source-card:hover,
    html[data-theme="light"] .atlas-metric-card:hover {
        border-color: rgba(0,229,255,0.25);
        box-shadow: var(--atlas-shadow-hover), 0 0 30px rgba(0,229,255,0.06);
    }

    html[data-theme="light"] [data-testid="stMetric"]:hover {
        border-color: rgba(0,229,255,0.25);
        box-shadow: var(--atlas-shadow-hover), 0 0 20px rgba(0,229,255,0.06);
    }

    html[data-theme="light"] .atlas-side-brand {
        background: linear-gradient(135deg, rgba(0,229,255,0.06) 0%, var(--atlas-card-glass) 100%);
        box-shadow: var(--atlas-shadow-liquid);
    }

    html[data-theme="light"] .atlas-sidebar-logo-wrap {
        background: linear-gradient(135deg, rgba(255,255,255,0.6) 0%, var(--atlas-card-glass) 100%);
        border-color: rgba(0,0,0,0.08);
        box-shadow: var(--atlas-shadow-liquid);
    }

    html[data-theme="light"] .atlas-sidebar-logo-wrap::before {
        background: radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.5), transparent 60%);
    }

    html[data-theme="light"] .atlas-sidebar-logo-wrap img {
        filter: drop-shadow(0 2px 8px rgba(0,229,255,0.1)) drop-shadow(0 4px 16px rgba(0,0,0,0.08));
    }

    html[data-theme="light"] [data-testid="stSidebar"] a {
        color: #475569 !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"] a:hover {
        color: #0f172a !important;
    }

    html[data-theme="light"] .stTabs [data-baseweb="tab-list"] {
        border-bottom-color: rgba(0,0,0,0.06);
    }
</style>
"""


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


@st.cache_data(show_spinner=False)
def _load_bg_b64(mode: str) -> str:
    import base64
    assets_dir = Path(__file__).resolve().parents[1] / "assets"
    filename = "bg-light.jpg" if mode == "light" else "bg-dark.jpg"
    path = assets_dir / filename
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


def apply_atlas_theme() -> None:
    light_mode = st.session_state.get("atlas_light_mode", False)
    theme = "light" if light_mode else "dark"
    b64 = _load_bg_b64(theme)
    st.markdown(ATLAS_CSS, unsafe_allow_html=True)
    if light_mode:
        st.markdown(ATLAS_CSS_LIGHT_OVERRIDES, unsafe_allow_html=True)
    bg_css = ""
    if b64:
        overlay = "rgba(255,255,255,0.30)" if light_mode else "rgba(4,8,18,0.60)"
        bg_css = f"""
        <style>
            .stApp {{
                background:
                    linear-gradient({overlay}, {overlay}),
                    url('data:image/jpeg;base64,{b64}') center/cover no-repeat fixed !important;
            }}
        </style>
        """
    else:
        bg_css = """
        <style>
            .stApp { background-color: #060a14 !important; }
        </style>
        """
    st.markdown(bg_css, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            [data-testid="stAppViewContainer"],
            .main,
            [data-testid="stHeader"] {
                background-color: transparent !important;
                background-image: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if light_mode:
        st.markdown(
            """
            <style>
                [data-testid="stSidebar"],
                [data-testid="stSidebarContent"],
                [data-testid="stSidebar"] > div:first-child {
                    background-color: #ffffff !important;
                    background-image: none !important;
                }
                [data-testid="stSidebar"] > div:first-child {
                    background: rgba(255, 255, 255, 0.95) !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        f"""
        <script>
            document.documentElement.setAttribute("data-theme", "{theme}");
        </script>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_navigation(active_page: str) -> None:
    with st.sidebar:
        logo_path = Path(__file__).resolve().parents[1] / "assets" / "ATLAS LOGO.png"
        if logo_path.exists():
            st.markdown(
                """<div class="atlas-sidebar-logo-wrap">""",
                unsafe_allow_html=True,
            )
            st.image(str(logo_path), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="atlas-side-brand" role="banner" aria-label="ATLAS brand">
                <div class="atlas-kicker">ATLAS</div>
                <p style="color: var(--atlas-muted); font-size: 0.72rem; line-height: 1.4; margin: 0.3rem 0 0 0;">
                    Planetary climate intelligence, real-time monitoring, and research workflows.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div class='atlas-side-section'>Theme</div>", unsafe_allow_html=True)
        st.toggle("Light mode", key="atlas_light_mode")
        st.page_link("app.py", label="Landing", icon=":material/rocket_launch:")
        st.text_input(
            "Sidebar Search",
            key="atlas_sidebar_search",
            placeholder="Search modules",
            label_visibility="collapsed",
        )
        st.markdown("<div class='atlas-side-section'>Workspace</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='atlas-active-page'>Active: {_escape(active_page)}</div>", unsafe_allow_html=True)
        for item in NAV_ITEMS:
            st.page_link(item["path"], label=item["label"], icon=item["icon"])
        st.markdown("<div class='atlas-side-section'>System</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="atlas-nav-panel">
                <p class="atlas-nav-caption">Layout: 12-column responsive shell</p>
                <p class="atlas-nav-caption">UI mix: NASA science + Apple glass + neobrutal cards</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_topbar(active_page: str, subtitle: str, search_placeholder: str = "Search climate signals, regions, or datasets") -> str:
    left, center = st.columns((1.15, 1.0))
    with left:
        st.markdown(
            f"""
            <div class="atlas-topbar-card" role="region" aria-label="Active view: {_escape(active_page)}">
                <div class="atlas-kicker">Active View</div>
                <h2>{_escape(active_page)}</h2>
                <p>{_escape(subtitle)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with center:
        search_value = st.text_input(
            "Global Search",
            placeholder=search_placeholder,
            key=f"atlas_topbar_search_{active_page.lower().replace(' ', '_')}",
            label_visibility="collapsed",
        )
    return search_value


def render_app_shell(active_page: str, subtitle: str, search_placeholder: str = "Search climate signals, regions, or datasets") -> str:
    apply_atlas_theme()
    set_chart_theme(dark=not st.session_state.get("atlas_light_mode", False))
    render_sidebar_navigation(active_page)
    return render_topbar(active_page, subtitle, search_placeholder)


def render_page_hero(kicker: str, title: str, body: str, subtitle: str | None = None) -> None:
    subtitle_html = f"<p class='atlas-tagline'>{_escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <section class="atlas-hero" role="region" aria-label="{_escape(kicker)}: {_escape(title)}">
            <div class="atlas-kicker">{_escape(kicker)}</div>
            <h1>{_escape(title)}</h1>
            {subtitle_html}
            <p class="atlas-subtitle">{_escape(body)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(title: str, body: str, eyebrow: str | None = None) -> None:
    eyebrow_html = f"<div class='atlas-kicker'>{_escape(eyebrow)}</div>" if eyebrow else ""
    st.markdown(
        f"""
        <div class="atlas-section-head" role="heading" aria-level="2" aria-label="{_escape(title)}">
            {eyebrow_html}
            <h3>{_escape(title)}</h3>
            <p>{_escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <article class="atlas-feature-card" tabindex="0" role="article" aria-label="{_escape(title)}">
            <h4>{_escape(title)}</h4>
            <p>{_escape(body)}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_info_banner(message: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-info-banner" role="status" aria-live="polite">
            <p>{_escape(message)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title: str, value: str, subtext: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-metric-card" role="group" aria-label="{_escape(title)}: {_escape(value)}">
            <div class="atlas-metric-label">{_escape(title)}</div>
            <div class="atlas-metric-value">{_escape(value)}</div>
            <div class="atlas-metric-sub">{_escape(subtext)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_story_panel(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="atlas-story-panel" role="article" aria-label="{_escape(title)}">
            <h4>{_escape(title)}</h4>
            <p>{_escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_source_card(title: str, status: str, detail: str) -> None:
    sl = status.lower()
    tone = ("warning" if "missing" in sl or "invalid" in sl or sl == "fail"
            else "neutral" if sl in {"ready", "optional", "deferred"}
            else "")
    status_class = f"atlas-status {tone}".strip()
    st.markdown(
        f"""
        <div class="atlas-source-card" role="region" aria-label="{_escape(title)}: {_escape(status)}">
            <span class="{status_class}" aria-label="Status: {_escape(status)}">{_escape(status)}</span>
            <h4>{_escape(title)}</h4>
            <p>{_escape(detail)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_story_stepper(steps: list[dict[str, str]], active_index: int) -> None:
    chips: list[str] = []
    for idx, step in enumerate(steps):
        active_class = "active" if idx == active_index else ""
        sublabel = step.get("region") or step.get("title") or ""
        chips.append(
            f"""
            <div class="atlas-step-chip {active_class}">
                <strong>{idx + 1}. {_escape(step["slug"])}</strong>
                <span>{_escape(sublabel)}</span>
            </div>
            """
        )
    st.markdown(f"<div class='atlas-stepper'>{''.join(chips)}</div>", unsafe_allow_html=True)
