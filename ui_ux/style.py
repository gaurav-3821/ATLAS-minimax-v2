from __future__ import annotations

from datetime import datetime, timezone
import html
from pathlib import Path

import streamlit as st


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
        --atlas-card-bg: rgba(15, 22, 46, 0.55);
        --atlas-card-glass: rgba(12, 18, 38, 0.65);
        --atlas-card-border: rgba(255,255,255,0.07);
        --atlas-glass-shine: rgba(255,255,255,0.04);
        --atlas-cyan: #00E5FF;
        --atlas-yellow: #FFD84D;
        --atlas-green: #6EFF9A;
        --atlas-pink: #FF5C8A;
        --atlas-purple: #A78BFA;
        --atlas-text: #FFFFFF;
        --atlas-text-secondary: #E2E8F0;
        --atlas-muted: #94A3B8;
        --atlas-subtle: #64748B;
        --atlas-shadow-glass: 0 8px 32px rgba(0,0,0,0.35);
        --atlas-shadow-hover: 0 12px 48px rgba(0,0,0,0.45);
        --atlas-radius-sm: 10px;
        --atlas-radius-md: 14px;
        --atlas-radius-lg: 20px;
        --atlas-radius-xl: 24px;
        --atlas-space-xs: 0.25rem;
        --atlas-space-sm: 0.5rem;
        --atlas-space-md: 1rem;
        --atlas-space-lg: 1.75rem;
        --atlas-space-xl: 2.5rem;
        --atlas-glass-blur: 18px;
        --atlas-color-success: #6EFF9A;
        --atlas-color-warning: #FFD84D;
        --atlas-color-error: #FF5C8A;
        --atlas-color-info: #00E5FF;
        --atlas-focus-ring: 0 0 0 3px rgba(0,229,255,0.35);
        --atlas-font-mono: 'Fira Code', 'JetBrains Mono', monospace;
        --atlas-font-body: 'Fira Sans', 'Inter', sans-serif;
        --atlas-font-heading: 'Space Grotesk', sans-serif;
        --atlas-transition: 350ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    html, body, [class*="css"] {
        font-family: var(--atlas-font-body);
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 8%, rgba(0,229,255,0.10), transparent 35%),
            radial-gradient(ellipse at 85% 12%, rgba(167,139,250,0.08), transparent 30%),
            radial-gradient(ellipse at 50% 90%, rgba(110,255,154,0.06), transparent 32%),
            radial-gradient(ellipse at 30% 55%, rgba(255,92,138,0.04), transparent 28%),
            linear-gradient(165deg, #040812 0%, #080e1f 25%, #0c1528 50%, #080e1f 75%, #040812 100%);
        animation: atlasLiquid 24s ease-in-out infinite;
        background-size: 200% 200%;
    }

    @keyframes atlasLiquid {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 20%; }
        50% { background-position: 50% 100%; }
        75% { background-position: 0% 60%; }
        100% { background-position: 0% 0%; }
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

    #MainMenu, footer, header[data-testid="stHeader"] {
        display: none;
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
        background: rgba(8, 13, 28, 0.65);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-right: 1px solid rgba(255,255,255,0.06);
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
        box-shadow: var(--atlas-shadow-glass);
        backdrop-filter: blur(var(--atlas-glass-blur));
        -webkit-backdrop-filter: blur(var(--atlas-glass-blur));
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
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 20%, var(--atlas-glass-shine), transparent 50%);
        pointer-events: none;
        opacity: 0;
        transition: opacity var(--atlas-transition);
    }

    .atlas-feature-card:hover::before,
    .atlas-source-card:hover::before,
    .atlas-metric-card:hover::before {
        opacity: 1;
    }

    .atlas-feature-card:hover,
    .atlas-source-card:hover,
    .atlas-metric-card:hover {
        border-color: rgba(0,229,255,0.18);
        box-shadow: var(--atlas-shadow-hover);
        transform: translateY(-2px);
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
        border-radius: 8px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        color: var(--atlas-text-secondary);
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        line-height: 1;
        backdrop-filter: blur(6px);
    }

    .atlas-chip.cyan { color: var(--atlas-cyan); background: rgba(0,229,255,0.10); border-color: rgba(0,229,255,0.18); }
    .atlas-chip.yellow { color: var(--atlas-yellow); background: rgba(255,216,77,0.10); border-color: rgba(255,216,77,0.18); }
    .atlas-chip.green { color: var(--atlas-green); background: rgba(110,255,154,0.10); border-color: rgba(110,255,154,0.18); }
    .atlas-chip.pink { color: var(--atlas-pink); background: rgba(255,92,138,0.10); border-color: rgba(255,92,138,0.18); }

    .atlas-side-brand {
        padding: 0.85rem;
        margin-bottom: 0.75rem;
        border: 1px solid var(--atlas-card-border);
        border-radius: var(--atlas-radius-md);
        background: linear-gradient(135deg, rgba(0,229,255,0.06) 0%, transparent 60%);
        backdrop-filter: blur(12px);
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
        border: 1px solid rgba(0,229,255,0.2);
        border-radius: var(--atlas-radius-sm);
        background: linear-gradient(135deg, rgba(0,229,255,0.08) 0%, rgba(167,139,250,0.06) 100%);
        font-family: var(--atlas-font-mono);
        font-size: 0.72rem;
        color: var(--atlas-cyan);
        margin-bottom: 0.5rem;
        backdrop-filter: blur(6px);
    }

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a,
    .stFormSubmitButton > button {
        border: none !important;
        border-radius: var(--atlas-radius-sm) !important;
        background: linear-gradient(135deg, rgba(0,229,255,0.85) 0%, rgba(167,139,250,0.85) 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-family: var(--atlas-font-body) !important;
        box-shadow: var(--atlas-shadow-glass) !important;
        min-height: 2.5rem !important;
        backdrop-filter: blur(8px) !important;
        transition: transform var(--atlas-transition), box-shadow var(--atlas-transition) !important;
        letter-spacing: 0.02em;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--atlas-shadow-hover) !important;
        background: linear-gradient(135deg, rgba(0,229,255,0.95) 0%, rgba(167,139,250,0.95) 100%) !important;
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
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: var(--atlas-radius-sm) !important;
        box-shadow: none !important;
        backdrop-filter: blur(6px) !important;
        transition: border-color var(--atlas-transition), box-shadow var(--atlas-transition);
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--atlas-cyan) !important;
        box-shadow: 0 0 0 3px rgba(0,229,255,0.12) !important;
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
        background: var(--atlas-card-bg);
        border: 1px solid var(--atlas-card-border);
        border-radius: var(--atlas-radius-sm);
        box-shadow: var(--atlas-shadow-glass);
        backdrop-filter: blur(var(--atlas-glass-blur));
        padding: 0.7rem 0.85rem;
        transition: border-color var(--atlas-transition), transform var(--atlas-transition);
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(0,229,255,0.18);
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
            radial-gradient(ellipse at 100% 0%, rgba(0,229,255,0.08), transparent 40%),
            radial-gradient(ellipse at 0% 100%, rgba(167,139,250,0.06), transparent 40%);
        background-color: var(--atlas-card-glass);
        border: 1px solid var(--atlas-card-border);
        border-radius: var(--atlas-radius-xl);
        position: relative;
        overflow: hidden;
    }

    .atlas-hero::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--atlas-cyan), transparent);
        opacity: 0.3;
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
        background: linear-gradient(135deg, rgba(0,229,255,0.06) 0%, transparent 100%);
        border-left: 3px solid var(--atlas-cyan);
        backdrop-filter: blur(12px);
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
        border: 1px solid var(--atlas-card-border);
        border-radius: var(--atlas-radius-sm);
        background: rgba(255,255,255,0.02);
        backdrop-filter: blur(6px);
        transition: border-color var(--atlas-transition), background var(--atlas-transition);
    }

    .atlas-step-chip:hover {
        border-color: rgba(0,229,255,0.15);
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


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def apply_atlas_theme() -> None:
    st.markdown(ATLAS_CSS, unsafe_allow_html=True)


def render_sidebar_navigation(active_page: str) -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="atlas-side-brand" role="banner" aria-label="ATLAS brand">
                <div class="atlas-kicker">ATLAS</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        text_logo = Path(__file__).resolve().parents[1] / "assets" / "atlas.png"
        if text_logo.exists():
            st.image(str(text_logo), use_container_width=True)
        st.markdown(
            "<p style='color: var(--atlas-muted); font-size: 0.75rem; line-height: 1.4; margin: 0.25rem 0 0 0;'>"
            "Operational climate monitoring, prediction workflows, and research-grade analysis.</p>",
            unsafe_allow_html=True,
        )
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
                <p class="atlas-nav-caption">Theme: Dark orbital mode</p>
                <p class="atlas-nav-caption">Layout: 12-column responsive shell</p>
                <p class="atlas-nav-caption">UI mix: NASA science + Apple glass + neobrutal cards</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_topbar(active_page: str, subtitle: str, search_placeholder: str = "Search climate signals, regions, or datasets") -> str:
    utc_stamp = datetime.now(timezone.utc).strftime("%H:%M UTC")
    left, center, right = st.columns((1.15, 1.0, 0.7))
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
    with right:
        st.markdown(
            f"""
            <div class="atlas-topbar-card" role="region" aria-label="System status">
                <div class="atlas-chip-row">
                    <span class="atlas-chip cyan">Live</span>
                    <span class="atlas-chip yellow" aria-label="Time: {_escape(utc_stamp)}">{_escape(utc_stamp)}</span>
                    <span class="atlas-chip pink">Analyst</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    return search_value


def render_app_shell(active_page: str, subtitle: str, search_placeholder: str = "Search climate signals, regions, or datasets") -> str:
    apply_atlas_theme()
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
