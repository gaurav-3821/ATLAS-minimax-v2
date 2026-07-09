from __future__ import annotations

import html
from pathlib import Path

import streamlit as st

from ui_ux.chart_factory import set_chart_theme
from ui_ux.stitch_effects import ALL_STITCH_EFFECTS
from ui_ux.stitch_tokens import NAV_ITEMS_STITCH, NAV_ITEMS_SECONDARY


NAV_ITEMS = [
    {"label": "Story Mode", "route": "/Story_Mode", "icon": "play_circle"},
    {"label": "Dashboard", "route": "/Dashboard", "icon": "dashboard"},
    {"label": "Global Map", "route": "/Global_Climate_Map", "icon": "public"},
    {"label": "Climate Signals", "route": "/Climate_Signals", "icon": "query_stats"},
    {"label": "Risk Intelligence", "route": "/Risk_Intelligence", "icon": "warning"},
    {"label": "Predictions", "route": "/AI_Predictions", "icon": "auto_graph"},
    {"label": "Data Explorer", "route": "/Data_Explorer", "icon": "travel_explore"},
    {"label": "Research Lab", "route": "/Research_Lab", "icon": "science"},
    {"label": "Reports", "route": "/Reports", "icon": "description"},
    {"label": "Settings", "route": "/Settings", "icon": "settings"},
]


ATLAS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    :root {
        --atlas-bg: #111318;
        --atlas-bg-deep: #0c0e12;
        --atlas-surface: #111318;
        --atlas-surface-container: #1e2024;
        --atlas-surface-container-low: #1a1c20;
        --atlas-surface-container-lowest: #0c0e12;
        --atlas-surface-bright: #37393e;
        --atlas-surface-variant: #333539;
        --atlas-primary: #e1fdff;
        --atlas-primary-fixed-dim: #00dbe7;
        --atlas-primary-container: #00f2ff;
        --atlas-primary-fixed: #74f5ff;
        --atlas-on-primary: #00363a;
        --atlas-on-primary-container: #006a71;
        --atlas-secondary: #d1bcff;
        --atlas-secondary-container: #7000ff;
        --atlas-on-secondary: #3c0090;
        --atlas-tertiary: #fff6ef;
        --atlas-tertiary-container: #ffd49c;
        --atlas-tertiary-fixed-dim: #ffb950;
        --atlas-on-tertiary: #452b00;
        --atlas-error: #ffb4ab;
        --atlas-error-container: #93000a;
        --atlas-on-error: #690005;
        --atlas-text: #e2e2e8;
        --atlas-text-secondary: #b9cacb;
        --atlas-muted: #849495;
        --atlas-subtle: #3a494b;
        --atlas-outline: #849495;
        --atlas-outline-variant: #3a494b;
        --atlas-glass-fill: rgba(255,255,255,0.05);
        --atlas-glass-border: rgba(255,255,255,0.10);
        --atlas-glass-edge: rgba(255,255,255,0.20);
        --atlas-glass-blur: 20px;
        --atlas-glass-saturate: 180%;
        --atlas-shadow-glass: 0 8px 32px rgba(0,0,0,0.3);
        --atlas-shadow-neo: 6px 6px 0px rgba(0,219,231,0.2);
        --atlas-shadow-neo-hover: 10px 10px 0px rgba(0,219,231,0.4);
        --atlas-shadow-topbar: 0 0 20px rgba(0,219,231,0.1);
        --atlas-shadow-sidebar: 10px 0 30px rgba(0,0,0,0.3);
        --atlas-radius-sm: 0.25rem;
        --atlas-radius-md: 0.5rem;
        --atlas-radius-lg: 0.75rem;
        --atlas-radius-full: 9999px;
        --atlas-space-unit: 4px;
        --atlas-space-sm: 16px;
        --atlas-space-md: 32px;
        --atlas-space-lg: 48px;
        --atlas-font-heading: 'Space Grotesk', sans-serif;
        --atlas-font-body: 'Geist', sans-serif;
        --atlas-font-mono: 'JetBrains Mono', monospace;
        --atlas-transition: 300ms cubic-bezier(0.22, 1, 0.36, 1);
        --atlas-transition-fast: 200ms ease;
    }

    html, body, .stApp, .main, div, p, a, li, label, input, textarea, select, button, option {
        font-family: var(--atlas-font-body) !important;
        color: var(--atlas-text) !important;
    }
    h1, h2, h3, h4, h5, h6, .st-emotion-cache-1104yt, [class*="header"], [class*="title"], .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        font-family: var(--atlas-font-heading) !important;
    }
    code, pre, kbd, samp, .stCodeBlock, [class*="mono"], [class*="code"] {
        font-family: var(--atlas-font-mono) !important;
    }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: var(--atlas-bg) !important;
        background-image: none !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    .stApp {
        background-color: var(--atlas-bg);
        background:
            radial-gradient(circle at 20% 30%, rgba(0,219,231,0.08) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(112,0,255,0.08) 0%, transparent 40%);
        animation: atlasLiquidDrift 20s ease-in-out infinite alternate;
    }

    @keyframes atlasLiquidDrift {
        0% { background-position: 0% 0%; }
        33% { background-position: 2% 4%; }
        66% { background-position: -1% -2%; }
        100% { background-position: 0% 0%; }
    }
    @keyframes atlasPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(0.98); }
    }

    @keyframes atlasPulseDot {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
    }

    @keyframes atlasScan {
        from { top: 0%; }
        to { top: 100%; }
    }

    @keyframes atlasFadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes atlasFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined' !important;
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        vertical-align: middle;
        color: inherit !important;
        line-height: 1;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
    ::-webkit-scrollbar-thumb { background: var(--atlas-primary-fixed-dim); border-radius: var(--atlas-radius-full); }

    .atlas-status-dot {
        width: 8px;
        height: 8px;
        background-color: var(--atlas-primary-fixed-dim);
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px var(--atlas-primary-fixed-dim);
        animation: atlasPulseDot 2s infinite ease-in-out;
    }

    #MainMenu { display: none; }
    footer { visibility: hidden; }

    button[data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        background: rgba(0,219,231,0.1) !important;
        border: 1px solid rgba(0,219,231,0.3) !important;
        border-radius: var(--atlas-radius-sm) !important;
        color: var(--atlas-primary) !important;
        padding: 0.4rem !important;
        min-width: 2.2rem !important;
        min-height: 2.2rem !important;
        backdrop-filter: blur(12px) !important;
    }

    button[data-testid="stSidebarCollapsedControl"]:hover,
    button[data-testid="stSidebarCollapseButton"]:hover {
        background: rgba(0,219,231,0.2) !important;
    }

    [data-testid="stSidebarNav"] { display: none; }

    [data-testid="stSidebar"] > div:first-child {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
        border-right: 1px solid var(--atlas-glass-border) !important;
        box-shadow: var(--atlas-shadow-sidebar) !important;
    }

    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child,
    section[data-testid="stSidebar"] > div:first-child {
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
    }

    [data-testid="stSidebar"] > div:first-child::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 1px;
        height: 100%;
        background: linear-gradient(180deg, transparent, rgba(0,219,231,0.15), transparent);
        pointer-events: none;
        z-index: 1;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] div[data-testid="stPageLink"] a {
        padding: 0.5rem 0.75rem;
        border-radius: var(--atlas-radius-md);
        border: 1px solid transparent;
        transition: padding var(--atlas-transition), background var(--atlas-transition), border var(--atlas-transition), color var(--atlas-transition) !important;
    }

    [data-testid="stSidebar"] div[data-testid="stPageLink"] a:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid var(--atlas-glass-border);
        padding-left: 1.25rem;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent;
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 0.85rem;
        padding-bottom: 2.5rem;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: var(--atlas-font-heading);
        color: var(--atlas-text);
        letter-spacing: -0.02em;
        font-weight: 600;
    }

    p, li, label, div[data-testid="stMarkdownContainer"], span {
        color: var(--atlas-text-secondary);
    }

    code, pre {
        font-family: var(--atlas-font-mono) !important;
    }

    .glass-panel,
    .atlas-topbar-card,
    .atlas-hero,
    .atlas-feature-card,
    .atlas-info-banner,
    .atlas-metric-card,
    .atlas-source-card,
    .atlas-section-head,
    .atlas-story-panel,
    .atlas-nav-panel,
    .atlas-stat-card,
    .atlas-source-mini {
        backdrop-filter: blur(var(--atlas-glass-blur)) saturate(var(--atlas-glass-saturate));
        -webkit-backdrop-filter: blur(var(--atlas-glass-blur)) saturate(var(--atlas-glass-saturate));
        background: var(--atlas-glass-fill);
        border: 1px solid var(--atlas-glass-border);
        box-shadow: var(--atlas-shadow-glass);
    }

    .atlas-topbar-card,
    .atlas-feature-card,
    .atlas-info-banner,
    .atlas-metric-card,
    .atlas-source-card,
    .atlas-nav-panel,
    .atlas-stat-card,
    .atlas-source-mini {
        border-top: 1px solid var(--atlas-glass-edge);
        border-left: 1px solid var(--atlas-glass-edge);
        padding: 1rem 1.15rem;
        margin-bottom: 0.75rem;
        transition: border-color var(--atlas-transition), box-shadow var(--atlas-transition), transform var(--atlas-transition);
        position: relative;
    }

    .atlas-topbar-card:hover,
    .atlas-feature-card:hover,
    .atlas-metric-card:hover,
    .atlas-source-card:hover {
        border-color: rgba(0,219,231,0.4);
        box-shadow: var(--atlas-shadow-glass), 0 0 20px rgba(0,219,231,0.1);
        transform: translateY(-2px);
    }

    .atlas-topbar-card {
        padding: 0.7rem 0.9rem;
        min-height: 58px;
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
        border-radius: var(--atlas-radius-sm);
        background: rgba(255,255,255,0.05);
        border: 1px solid var(--atlas-glass-border);
        color: var(--atlas-text-secondary);
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        line-height: 1;
        backdrop-filter: blur(12px) saturate(150%);
        -webkit-backdrop-filter: blur(12px) saturate(150%);
    }

    .atlas-chip.cyan { color: var(--atlas-primary); background: rgba(0,219,231,0.10); border-color: rgba(0,219,231,0.18); }
    .atlas-chip.yellow { color: var(--atlas-tertiary-fixed-dim); background: rgba(255,185,80,0.10); border-color: rgba(255,185,80,0.18); }
    .atlas-chip.green { color: #6EFF9A; background: rgba(110,255,154,0.10); border-color: rgba(110,255,154,0.18); }
    .atlas-chip.pink { color: #FF5C8A; background: rgba(255,92,138,0.10); border-color: rgba(255,92,138,0.18); }

    .atlas-hero-logo-wrap {
        padding: 0.25rem;
        border: 1px solid var(--atlas-glass-border);
        border-radius: var(--atlas-radius-md);
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, var(--atlas-glass-fill) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        box-shadow: var(--atlas-shadow-glass);
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .atlas-hero-logo-wrap img {
        display: block;
        max-width: 128px;
        height: auto;
        margin: 0 auto;
    }

    .atlas-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.25rem 0.6rem;
        border-radius: var(--atlas-radius-sm);
        background: rgba(0,219,231,0.10);
        border: 1px solid rgba(0,219,231,0.20);
        color: var(--atlas-primary);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        line-height: 1;
        backdrop-filter: blur(6px);
    }

    .atlas-side-section {
        margin: 0.75rem 0 0.4rem 0;
        padding: 0 0.3rem;
        font-family: var(--atlas-font-mono);
        font-size: 0.65rem;
        color: var(--atlas-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
    }


    /* ── Stitch Sidebar Upgrade ─────────────────────────────────────────── */
    .atlas-stitch-sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid var(--atlas-glass-border);
    }

    .atlas-stitch-sidebar-brand img {
        width: 36px;
        height: 36px;
        border-radius: var(--atlas-radius-md);
    }

    .atlas-stitch-sidebar-brand-text {
        font-family: var(--atlas-font-heading);
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--atlas-text);
        letter-spacing: -0.02em;
    }

    .atlas-stitch-nav-section {
        margin-bottom: 1.5rem;
    }

    .atlas-stitch-nav-label {
        font-family: var(--atlas-font-mono);
        font-size: 0.6rem;
        color: var(--atlas-muted);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 700;
        padding: 0 0.75rem;
        margin-bottom: 0.5rem;
    }

    [data-testid="stSidebar"] .atlas-stitch-nav-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.65rem 0.75rem;
        margin: 0.15rem 0.5rem;
        border-radius: var(--atlas-radius-md);
        color: var(--atlas-text-secondary);
        text-decoration: none;
        font-family: var(--atlas-font-body);
        font-size: 0.82rem;
        font-weight: 500;
        transition: all 0.15s ease;
        border: 1px solid transparent;
    }

    [data-testid="stSidebar"] .atlas-stitch-nav-item:hover {
        background: rgba(255,255,255,0.06);
        color: var(--atlas-text);
        border-color: var(--atlas-glass-border);
    }

    [data-testid="stSidebar"] .atlas-stitch-nav-item.active {
        background: rgba(0,219,231,0.10);
        color: var(--atlas-primary);
        border-color: rgba(0,219,231,0.20);
        font-weight: 600;
    }

    [data-testid="stSidebar"] .atlas-stitch-nav-item .material-symbols-outlined {
        font-size: 1.15rem;
        color: var(--atlas-primary-fixed-dim);
    }

    [data-testid="stSidebar"] .atlas-stitch-nav-item.active .material-symbols-outlined {
        color: var(--atlas-primary);
    }

    .atlas-stitch-sidebar-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 0.75rem;
        border-top: 1px solid var(--atlas-glass-border);
        background: var(--atlas-glass-fill);
    }

    /* ── Stitch Topbar Upgrade ──────────────────────────────────────────── */
    .atlas-stitch-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1.5rem;
        margin-bottom: 1rem;
        background: var(--atlas-glass-fill);
        border: 1px solid var(--atlas-glass-border);
        border-radius: var(--atlas-radius-lg);
        backdrop-filter: blur(var(--atlas-glass-blur)) saturate(var(--atlas-glass-saturate));
    }

    .atlas-stitch-topbar-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .atlas-stitch-topbar-kicker {
        font-family: var(--atlas-font-mono);
        font-size: 0.65rem;
        color: var(--atlas-primary-fixed-dim);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 700;
    }

    .atlas-stitch-topbar-title {
        font-family: var(--atlas-font-heading);
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--atlas-text);
        letter-spacing: -0.02em;
    }

    .atlas-stitch-topbar-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .atlas-stitch-topbar-search {
        min-width: 280px;
    }

    .atlas-stitch-ticker-bar {
        overflow: hidden;
        white-space: nowrap;
        width: 100%;
        height: 48px;
        display: flex;
        align-items: center;
        background: rgba(0,0,0,0.20);
        border: 1px solid var(--atlas-glass-border);
        border-radius: var(--atlas-radius-md);
        margin-bottom: 1rem;
    }

    .atlas-stitch-ticker-track {
        display: inline-flex;
        align-items: center;
        gap: 2rem;
        animation: atlasTickerScroll 40s linear infinite;
        padding: 0 1rem;
    }

    .atlas-stitch-ticker-track:hover {
        animation-play-state: paused;
    }

    .atlas-stitch-ticker-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .atlas-stitch-ticker-item .material-symbols-outlined {
        font-size: 1rem;
    }

    .atlas-stitch-ticker-label {
        font-family: var(--atlas-font-mono);
        font-size: 0.6rem;
        color: var(--atlas-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .atlas-stitch-ticker-value {
        font-family: var(--atlas-font-mono);
        font-size: 0.72rem;
        font-weight: 600;
    }

    .atlas-stitch-ticker-divider {
        height: 16px;
        width: 1px;
        background: rgba(255,255,255,0.15);
    }

    /* ── Ambient Micro-Interactions ──────────────────────────────────────── */
    .atlas-feature-card,
    .atlas-metric-card,
    .atlas-source-card,
    .atlas-info-banner,
    .atlas-story-panel {
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .atlas-feature-card:hover,
    .atlas-metric-card:hover,
    .atlas-source-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2), 0 0 20px rgba(0,219,231,0.08);
        border-color: rgba(0,219,231,0.3);
    }

    html[data-theme="light"] .atlas-feature-card:hover,
    html[data-theme="light"] .atlas-metric-card:hover,
    html[data-theme="light"] .atlas-source-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.08), 0 0 20px rgba(8,145,178,0.06);
    }

    .atlas-stitch-nav-item {
        transition: all 0.15s ease;
    }

    .atlas-stitch-nav-item:active {
        transform: scale(0.98);
    }

    .stButton > button {
        transition: all 0.2s ease;
    }

    .stButton > button:active {
        transform: scale(0.97);
    }

    @keyframes atlasFadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .atlas-feature-card,
    .atlas-metric-card,
    .atlas-hero,
    .atlas-info-banner {
        animation: atlasFadeIn 0.3s ease-out;
    }

    @media (prefers-reduced-motion: reduce) {
        .atlas-feature-card,
        .atlas-metric-card,
        .atlas-hero,
        .atlas-info-banner {
            animation: none;
        }
        .atlas-feature-card:hover,
        .atlas-metric-card:hover,
        .atlas-source-card:hover {
            transform: none;
        }
    }

    .atlas-hero {
        padding: 2.5rem 2.5rem 2rem;
        margin-bottom: 1.5rem;
        background:
            radial-gradient(ellipse at 100% 0%, rgba(0,219,231,0.10), transparent 40%),
            radial-gradient(ellipse at 0% 100%, rgba(112,0,255,0.07), transparent 40%),
            var(--atlas-glass-fill);
        border-top: 1px solid var(--atlas-glass-edge);
        border-left: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-lg);
        position: relative;
        overflow: hidden;
        box-shadow: var(--atlas-shadow-glass), inset 1px 1px 0 rgba(255,255,255,0.15);
    }

    .atlas-hero::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--atlas-primary), rgba(112,0,255,0.5), transparent);
        opacity: 0.4;
    }

    .atlas-hero h1 {
        margin: 0.8rem 0 0.3rem 0;
        font-size: 3.5rem;
        line-height: 1;
        font-weight: 700;
        letter-spacing: 0;
        background: linear-gradient(135deg, #FFFFFF 0%, var(--atlas-muted) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    html[data-theme="dark"] .atlas-hero h1 {
        background: linear-gradient(135deg, #FFFFFF 0%, var(--atlas-muted) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .atlas-tagline {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--atlas-primary);
    }

    .atlas-subtitle {
        margin-top: 0.75rem;
        max-width: 720px;
        color: var(--atlas-muted);
        font-size: 0.95rem;
        line-height: 1.7;
    }

    .atlas-section-head {
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid var(--atlas-primary);
        border-radius: 0 var(--atlas-radius-sm) var(--atlas-radius-sm) 0;
    }

    .atlas-section-head h3 {
        margin: 0 0 0.2rem 0;
        font-size: 1rem;
        font-weight: 600;
        font-family: var(--atlas-font-heading);
    }

    .atlas-section-head p {
        display: none;
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
        font-family: var(--atlas-font-heading);
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
        background: linear-gradient(135deg, rgba(0,219,231,0.08) 0%, var(--atlas-glass-fill) 100%);
        border-left: 3px solid var(--atlas-primary);
    }

    .atlas-copilot-card {
        border-left: 3px solid var(--atlas-primary-fixed-dim);
    }

    .atlas-copilot-card h4 {
        margin-top: 0.8rem;
        color: var(--atlas-primary);
    }

    .atlas-copilot-lede {
        margin-bottom: 0.8rem !important;
    }

    .atlas-copilot-list {
        margin: 0;
        padding-left: 1.1rem;
        color: var(--atlas-text-secondary);
    }

    .atlas-copilot-list li {
        margin: 0.35rem 0;
        color: var(--atlas-text-secondary);
        font-size: 0.86rem;
        line-height: 1.5;
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
        font-family: var(--atlas-font-mono);
        font-size: 0.65rem;
        color: var(--atlas-muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }

    .atlas-stat-value,
    .atlas-source-value,
    .atlas-metric-value {
        display: block;
        font-family: var(--atlas-font-heading);
        font-weight: 700;
        color: var(--atlas-text);
    }

    .atlas-metric-value {
        font-size: 2rem;
        line-height: 1.1;
        font-family: var(--atlas-font-mono);
        color: var(--atlas-primary);
    }

    .atlas-metric-sub {
        margin-top: 0.3rem;
        color: var(--atlas-muted);
        font-size: 0.78rem;
        line-height: 1.4;
        font-family: var(--atlas-font-mono);
    }

    .atlas-story-label {
        color: #FF5C8A;
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
        border: 1px solid var(--atlas-glass-border);
        border-radius: var(--atlas-radius-sm);
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, var(--atlas-glass-fill) 100%);
        backdrop-filter: blur(16px) saturate(150%);
        -webkit-backdrop-filter: blur(16px) saturate(150%);
        box-shadow: var(--atlas-shadow-glass);
        transition: border-color var(--atlas-transition), background var(--atlas-transition), box-shadow var(--atlas-transition);
    }

    .atlas-step-chip:hover {
        border-color: rgba(0,219,231,0.4);
        box-shadow: var(--atlas-shadow-glass), 0 0 20px rgba(0,219,231,0.05);
    }

    .atlas-step-chip.active {
        background: rgba(0,219,231,0.06);
        border-color: rgba(0,219,231,0.25);
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
        border-left: 3px solid var(--atlas-primary);
        border-radius: 0 var(--atlas-radius-sm) var(--atlas-radius-sm) 0;
    }

    .atlas-status {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.2rem 0.5rem;
        border-radius: var(--atlas-radius-sm);
        background: rgba(110,255,154,0.08);
        border: 1px solid rgba(110,255,154,0.15);
        color: #6EFF9A;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        line-height: 1;
        backdrop-filter: blur(4px);
    }

    .atlas-status.warning {
        color: var(--atlas-tertiary-fixed-dim);
        background: rgba(255,185,80,0.08);
        border-color: rgba(255,185,80,0.15);
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

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a,
    .stFormSubmitButton > button {
        border: none !important;
        border-radius: var(--atlas-radius-sm) !important;
        background: var(--atlas-primary) !important;
        color: var(--atlas-on-primary) !important;
        font-family: var(--atlas-font-mono) !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        box-shadow: var(--atlas-shadow-glass) !important;
        min-height: 2.5rem !important;
        backdrop-filter: blur(12px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(12px) saturate(180%) !important;
        transition: transform var(--atlas-transition-fast), box-shadow var(--atlas-transition-fast), background var(--atlas-transition-fast) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stLinkButton > a:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: var(--atlas-shadow-glass), 0 0 25px rgba(0,219,231,0.2) !important;
        background: var(--atlas-primary-container) !important;
        color: var(--atlas-on-primary-container) !important;
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
        background: rgba(0,0,0,0.2) !important;
        border: 1px solid var(--atlas-glass-border) !important;
        border-radius: var(--atlas-radius-sm) !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2), 0 1px 0 rgba(255,255,255,0.04) !important;
        backdrop-filter: blur(16px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        transition: border-color var(--atlas-transition-fast), box-shadow var(--atlas-transition-fast);
    }

    .stTextInput input {
        font-family: var(--atlas-font-mono) !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--atlas-primary-fixed-dim) !important;
        box-shadow: 0 0 15px rgba(0,219,231,0.3), inset 0 2px 4px rgba(0,0,0,0.2), 0 0 0 3px rgba(0,219,231,0.15) !important;
    }

    .stSlider [data-baseweb="slider"] {
        padding-top: 0.5rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        display: inline-flex;
        gap: 0.25rem;
        width: auto;
        max-width: 100%;
        margin-bottom: 0.9rem;
        padding: 0.25rem;
        border: 1px solid var(--atlas-glass-border);
        border-radius: var(--atlas-radius-md);
        background: rgba(255,255,255,0.05);
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.08);
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 2.35rem;
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: var(--atlas-radius-sm) !important;
        box-shadow: none;
        color: var(--atlas-muted) !important;
        padding: 0.45rem 0.85rem !important;
        margin: 0 !important;
        transition: color var(--atlas-transition), border-color var(--atlas-transition), background var(--atlas-transition), box-shadow var(--atlas-transition);
        font-size: 0.82rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--atlas-text) !important;
        background: rgba(255,255,255,0.07) !important;
        border-color: rgba(255,255,255,0.10) !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--atlas-on-primary) !important;
        background: var(--atlas-primary-fixed-dim) !important;
        border-color: var(--atlas-primary-fixed-dim) !important;
        box-shadow: 0 0 18px rgba(0,219,231,0.18) !important;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid var(--atlas-glass-border);
        border-top: 1px solid var(--atlas-glass-edge);
        border-left: 1px solid var(--atlas-glass-edge);
        border-radius: var(--atlas-radius-sm);
        box-shadow: var(--atlas-shadow-glass);
        backdrop-filter: blur(var(--atlas-glass-blur)) saturate(var(--atlas-glass-saturate));
        -webkit-backdrop-filter: blur(var(--atlas-glass-blur)) saturate(var(--atlas-glass-saturate));
        padding: 0.7rem 0.85rem;
        transition: border-color var(--atlas-transition), transform var(--atlas-transition), box-shadow var(--atlas-transition);
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(0,219,231,0.4);
        box-shadow: var(--atlas-shadow-glass), 0 0 20px rgba(0,219,231,0.1);
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

    .atlas-focusable:focus-visible,
    .atlas-card-focus:focus-visible,
    [tabindex]:focus-visible,
    button:focus-visible,
    a:focus-visible,
    [role="button"]:focus-visible {
        outline: none;
        box-shadow: 0 0 0 3px rgba(0,219,231,0.3) !important;
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    @media (max-width: 1200px) {
        .atlas-hero h1 { font-size: 2.8rem; }
        .atlas-metric-value { font-size: 1.35rem; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    }

    @media (max-width: 900px) {
        .atlas-card-grid { grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); }
        .atlas-stepper { grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); }
    }

    @media (max-width: 800px) {
        .atlas-hero { padding: 1.5rem; }
        .atlas-hero h1 { font-size: 2.2rem; }
        .atlas-topbar-card { min-height: 60px; padding: 0.6rem 0.85rem; }
        .atlas-topbar-title { font-size: 1.45rem !important; }
        .atlas-topbar-kicker { font-size: 0.62rem !important; line-height: 1.35; }
        .atlas-sidebar-logo-wrap img,
        .atlas-hero-logo-wrap img { max-width: 92px; }
    }

    @media (max-width: 640px) {
        .atlas-hero { padding: 1.2rem; }
        .atlas-hero h1 { font-size: 1.8rem; }
        .atlas-tagline { font-size: 0.85rem; }
        .atlas-metric-value { font-size: 1.15rem; }
        [data-testid="stSidebar"] { min-width: 200px; }
    }

    @media (max-width: 480px) {
        .atlas-hero h1 { font-size: 1.5rem; }
        .atlas-tagline { font-size: 0.78rem; }
        [data-testid="stSidebar"] { min-width: 160px; }
    }
</style>
"""

ATLAS_CSS_LIGHT_OVERRIDES = """
<style>
    html[data-theme="light"] {
        --atlas-bg: #f0f4f8;
        --atlas-bg-deep: #e2e8f0;
        --atlas-surface: #f8fafc;
        --atlas-surface-container: #f1f5f9;
        --atlas-surface-container-low: #f8fafc;
        --atlas-surface-container-lowest: #ffffff;
        --atlas-surface-bright: #ffffff;
        --atlas-surface-variant: #e2e8f0;
        --atlas-primary: #0891b2;
        --atlas-primary-fixed-dim: #0891b2;
        --atlas-primary-container: #22d3ee;
        --atlas-primary-fixed: #cffafe;
        --atlas-on-primary: #ffffff;
        --atlas-on-primary-container: #164e63;
        --atlas-secondary: #6366f1;
        --atlas-secondary-container: #a5b4fc;
        --atlas-on-secondary: #ffffff;
        --atlas-tertiary: #1e293b;
        --atlas-tertiary-container: #d97706;
        --atlas-tertiary-fixed-dim: #d97706;
        --atlas-on-tertiary: #ffffff;
        --atlas-error: #dc2626;
        --atlas-error-container: #fecaca;
        --atlas-on-error: #ffffff;
        --atlas-text: #0f172a;
        --atlas-text-secondary: #334155;
        --atlas-muted: #64748b;
        --atlas-subtle: #cbd5e1;
        --atlas-outline: #cbd5e1;
        --atlas-outline-variant: #e2e8f0;
        --atlas-glass-fill: rgba(255,255,255,0.7);
        --atlas-glass-border: rgba(0,0,0,0.08);
        --atlas-glass-edge: rgba(255,255,255,0.9);
        --atlas-shadow-glass: 0 8px 32px rgba(0,0,0,0.06);
        --atlas-shadow-neo: 6px 6px 0px rgba(8,145,178,0.15);
        --atlas-shadow-neo-hover: 10px 10px 0px rgba(8,145,178,0.25);
        --atlas-shadow-topbar: 0 0 20px rgba(0,0,0,0.04);
        --atlas-shadow-sidebar: 10px 0 30px rgba(0,0,0,0.06);
    }

    html[data-theme="light"] .stApp {
        background-color: var(--atlas-bg);
        background:
            radial-gradient(circle at 20% 30%, rgba(8,145,178,0.04) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(99,102,241,0.04) 0%, transparent 40%);
    }

    html[data-theme="light"] .stApp::before {
        opacity: 0;
        animation: none;
    }

    html[data-theme="light"] [data-testid="stSidebar"] > div:first-child {
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
        border-right: 1px solid rgba(0,0,0,0.08) !important;
        box-shadow: var(--atlas-shadow-sidebar) !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"][aria-expanded="true"] > div:first-child,
    html[data-theme="light"] section[data-testid="stSidebar"] > div:first-child {
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(30px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
    }

    html[data-theme="light"] h1,
    html[data-theme="light"] h2,
    html[data-theme="light"] h3,
    html[data-theme="light"] h4,
    html[data-theme="light"] h5,
    html[data-theme="light"] h6 {
        color: #0f172a !important;
    }

    html[data-theme="light"] .atlas-hero h1 {
        background: linear-gradient(135deg, #0f172a 0%, #475569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    html[data-theme="light"] p,
    html[data-theme="light"] li,
    html[data-theme="light"] label,
    html[data-theme="light"] span,
    html[data-theme="light"] div[data-testid="stMarkdownContainer"] {
        color: #334155 !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"] a {
        color: #475569;
    }

    html[data-theme="light"] [data-testid="stSidebar"] a:hover {
        color: #0f172a;
    }

    html[data-theme="light"] .atlas-side-section {
        color: #64748b !important;
    }

    html[data-theme="light"] .atlas-kicker {
        color: #0891b2 !important;
        background: rgba(8,145,178,0.08) !important;
        border-color: rgba(8,145,178,0.15) !important;
    }

    html[data-theme="light"] .atlas-hero {
        background:
            radial-gradient(ellipse at 100% 0%, rgba(8,145,178,0.06), transparent 40%),
            radial-gradient(ellipse at 0% 100%, rgba(99,102,241,0.04), transparent 40%);
        background-color: rgba(255,255,255,0.8);
    }

    html[data-theme="light"] .stButton > button,
    html[data-theme="light"] .stDownloadButton > button,
    html[data-theme="light"] .stLinkButton > a,
    html[data-theme="light"] .stFormSubmitButton > button {
        background: #0891b2 !important;
        color: #ffffff !important;
    }

    html[data-theme="light"] .stButton > button:hover,
    html[data-theme="light"] .stDownloadButton > button:hover {
        background: #22d3ee !important;
        color: #164e63 !important;
    }

    html[data-theme="light"] .stTextInput input,
    html[data-theme="light"] .stNumberInput input,
    html[data-theme="light"] .stTextArea textarea,
    html[data-theme="light"] .stDateInput input,
    html[data-theme="light"] .stSelectbox [data-baseweb="select"],
    html[data-theme="light"] .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.85) !important;
        border-color: var(--atlas-glass-border) !important;
        color: #0f172a !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.8) !important;
    }

    html[data-theme="light"] .atlas-chip {
        background: rgba(0,0,0,0.04);
        border-color: var(--atlas-glass-border);
    }

    html[data-theme="light"] .atlas-section-head {
        background: rgba(8,145,178,0.04) !important;
    }

    html[data-theme="light"] .atlas-info-banner {
        background: linear-gradient(135deg, rgba(8,145,178,0.04) 0%, transparent 100%) !important;
    }

    html[data-theme="light"] .atlas-step-chip.active {
        background: rgba(8,145,178,0.06);
        border-color: rgba(8,145,178,0.2);
    }

    html[data-theme="light"] .atlas-status {
        background: rgba(22,163,74,0.08);
        border-color: rgba(22,163,74,0.15);
        color: #16a34a;
    }

    html[data-theme="light"] .atlas-status.warning {
        color: #d97706;
        background: rgba(217,119,6,0.08);
        border-color: rgba(217,119,6,0.15);
    }

    html[data-theme="light"] .atlas-status.neutral {
        color: #64748b;
        background: rgba(0,0,0,0.03);
        border-color: rgba(0,0,0,0.06);
    }

    html[data-theme="light"] .atlas-feature-card:hover,
    html[data-theme="light"] .atlas-source-card:hover,
    html[data-theme="light"] .atlas-metric-card:hover {
        border-color: rgba(8,145,178,0.25);
        box-shadow: var(--atlas-shadow-glass), 0 0 20px rgba(8,145,178,0.06);
    }

    html[data-theme="light"] [data-testid="stMetric"]:hover {
        border-color: rgba(8,145,178,0.25);
        box-shadow: var(--atlas-shadow-glass), 0 0 20px rgba(8,145,178,0.06);
    }

    html[data-theme="light"] .atlas-hero-logo-wrap {
        background: linear-gradient(135deg, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0.65) 100%) !important;
        border-color: rgba(0,0,0,0.08) !important;
    }

    html[data-theme="light"] [data-testid="stSidebar"] .atlas-stitch-nav-item {
        color: #334155;
    }

    html[data-theme="light"] [data-testid="stSidebar"] .atlas-stitch-nav-item:hover {
        background: rgba(0,0,0,0.04);
        color: #0f172a;
    }

    html[data-theme="light"] [data-testid="stSidebar"] .atlas-stitch-nav-item.active {
        background: rgba(8,145,178,0.08);
        color: #0891b2;
        border-color: rgba(8,145,178,0.20);
    }

    html[data-theme="light"] [data-testid="stSidebar"] .atlas-stitch-nav-item .material-symbols-outlined {
        color: #0891b2;
    }

    html[data-theme="light"] .atlas-stitch-topbar {
        background: rgba(255,255,255,0.8);
        border-color: rgba(0,0,0,0.08);
    }

    html[data-theme="light"] .atlas-stitch-topbar-title {
        color: #0f172a;
    }

    html[data-theme="light"] .atlas-stitch-ticker-bar {
        background: rgba(0,0,0,0.03);
        border-color: rgba(0,0,0,0.06);
    }

    html[data-theme="light"] .atlas-stitch-ticker-divider {
        background: rgba(0,0,0,0.15);
    }

    html[data-theme="light"] .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.78) !important;
        border-color: rgba(0,0,0,0.08) !important;
        box-shadow: inset 1px 1px 0 rgba(255,255,255,0.85) !important;
    }

    html[data-theme="light"] .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
    }

    html[data-theme="light"] .stTabs [data-baseweb="tab"]:hover {
        color: #0f172a !important;
        background: rgba(0,0,0,0.04) !important;
        border-color: rgba(0,0,0,0.08) !important;
    }

    html[data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        background: #0891b2 !important;
        border-color: #0891b2 !important;
        box-shadow: 0 4px 14px rgba(8,145,178,0.18) !important;
    }

    html[data-theme="light"] .atlas-glass-panel::before,
    html[data-theme="light"] .atlas-hero::before,
    html[data-theme="light"] .atlas-feature-card::before,
    html[data-theme="light"] .atlas-metric-card::before,
    html[data-theme="light"] .atlas-source-card::before,
    html[data-theme="light"] .atlas-info-banner::before,
    html[data-theme="light"] .atlas-story-panel::before,
    html[data-theme="light"] .atlas-section-head::before {
        opacity: 0.03;
    }

    html[data-theme="light"] .atlas-glass-panel::after,
    html[data-theme="light"] .atlas-hero::after,
    html[data-theme="light"] .atlas-feature-card::after,
    html[data-theme="light"] .atlas-metric-card::after,
    html[data-theme="light"] .atlas-source-card::after,
    html[data-theme="light"] .atlas-info-banner::after,
    html[data-theme="light"] .atlas-story-panel::after {
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 3px,
            rgba(0,0,0,0.015) 3px,
            rgba(0,0,0,0.015) 4px
        );
    }

    html[data-theme="light"] .stButton > button {
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    html[data-theme="light"] .stButton > button:hover {
        box-shadow: 0 4px 16px rgba(8,145,178,0.12);
        background: rgba(8,145,178,0.06) !important;
    }
</style>
"""

LIGHT_ROOT_CSS = """
:root {
    --atlas-bg: #f0f4f8;
    --atlas-bg-deep: #e2e8f0;
    --atlas-surface: #f8fafc;
    --atlas-surface-container: #f1f5f9;
    --atlas-surface-container-low: #f8fafc;
    --atlas-surface-container-lowest: #ffffff;
    --atlas-surface-bright: #ffffff;
    --atlas-surface-variant: #e2e8f0;
    --atlas-primary: #0891b2;
    --atlas-primary-fixed-dim: #0891b2;
    --atlas-primary-container: #22d3ee;
    --atlas-primary-fixed: #cffafe;
    --atlas-on-primary: #ffffff;
    --atlas-on-primary-container: #164e63;
    --atlas-secondary: #6366f1;
    --atlas-secondary-container: #a5b4fc;
    --atlas-tertiary-fixed-dim: #d97706;
    --atlas-text: #0f172a;
    --atlas-text-secondary: #334155;
    --atlas-muted: #64748b;
    --atlas-subtle: #cbd5e1;
    --atlas-outline: #cbd5e1;
    --atlas-outline-variant: #e2e8f0;
    --atlas-glass-fill: rgba(255,255,255,0.7);
    --atlas-glass-border: rgba(0,0,0,0.08);
    --atlas-glass-edge: rgba(255,255,255,0.9);
    --atlas-shadow-glass: 0 8px 32px rgba(0,0,0,0.06);
    --atlas-shadow-sidebar: 10px 0 30px rgba(0,0,0,0.06);
}
"""


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


@st.cache_data(show_spinner=False)
def _load_b64(path_str: str) -> str:
    import base64
    path = Path(path_str)
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


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
    st.markdown(ATLAS_CSS, unsafe_allow_html=True)
    st.markdown(ALL_STITCH_EFFECTS, unsafe_allow_html=True)
    st.markdown(ATLAS_CSS_LIGHT_OVERRIDES, unsafe_allow_html=True)
    dark_b64 = _load_bg_b64("dark")
    light_b64 = _load_bg_b64("light")
    bg_default = "#111318"
    bg_dark = f"linear-gradient(rgba(4,8,18,0.60), rgba(4,8,18,0.60)), url('data:image/jpeg;base64,{dark_b64}') center/cover no-repeat fixed" if dark_b64 else bg_default
    bg_light = f"linear-gradient(rgba(255,255,255,0.30), rgba(255,255,255,0.30)), url('data:image/jpeg;base64,{light_b64}') center/cover no-repeat fixed" if light_b64 else "#f0f4f8"
    st.markdown(
        f"""
        <style>
            {LIGHT_ROOT_CSS if light_mode else ""}
            .stApp {{
                background: {bg_dark} !important;
                background-color: {bg_default} !important;
            }}
            {"html .stApp" if light_mode else 'html[data-theme="light"] .stApp'} {{
                background: {bg_light} !important;
                background-color: #f0f4f8 !important;
            }}
            [data-testid="stAppViewContainer"],
            .main,
            [data-testid="stHeader"] {{
                background-color: transparent !important;
                background-image: none !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_navigation(active_page: str) -> None:
    with st.sidebar:
        logo_path = Path(__file__).resolve().parents[1] / "assets" / "atlas-logo.png"
        logo_html = ""
        if logo_path.exists():
            logo_html = f'<img src="data:image/png;base64,{_load_b64(str(logo_path))}" alt="ATLAS logo" />'

        st.markdown(
            f"""
            <div class="atlas-stitch-sidebar-brand">
                {logo_html}
                <span class="atlas-stitch-sidebar-brand-text">ATLAS</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='atlas-stitch-nav-label'>Navigation</div>", unsafe_allow_html=True)
        for item in NAV_ITEMS_STITCH:
            active_class = " active" if item["label"] == active_page else ""
            st.markdown(
                f"""
                <a class="atlas-stitch-nav-item{active_class}" href="{_escape(item["route"])}" aria-label="{_escape(item["label"])}">
                    <span class="material-symbols-outlined" aria-hidden="true">{_escape(item["icon"])}</span>
                    <span>{_escape(item["label"])}</span>
                </a>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div class='atlas-stitch-nav-label' style='margin-top: 1.5rem;'>More</div>", unsafe_allow_html=True)
        for item in NAV_ITEMS_SECONDARY:
            active_class = " active" if item["label"] == active_page else ""
            st.markdown(
                f"""
                <a class="atlas-stitch-nav-item{active_class}" href="{_escape(item["route"])}" aria-label="{_escape(item["label"])}">
                    <span class="material-symbols-outlined" aria-hidden="true">{_escape(item["icon"])}</span>
                    <span>{_escape(item["label"])}</span>
                </a>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.toggle("Light mode", key="atlas_light_mode")


def render_topbar(
    active_page: str,
    subtitle: str,
    search_placeholder: str = "Search climate signals, regions, or datasets",
    show_search: bool = True,
) -> str:
    kicker = subtitle if len(subtitle) <= 32 else "Workspace"

    left, right = st.columns((1.3, 0.7)) if show_search else (st.container(), None)
    with left:
        st.markdown(
            f"""
            <div class="atlas-stitch-topbar" role="region" aria-label="Active view: {_escape(active_page)}">
                <div class="atlas-stitch-topbar-left">
                    <span class="atlas-stitch-topbar-kicker">{_escape(kicker)}</span>
                    <span style="color: var(--atlas-muted); font-size: 0.8rem;">|</span>
                    <span class="atlas-stitch-topbar-title">{_escape(active_page)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    if not show_search:
        return ""
    with right:
        st.markdown('<div style="margin-top: 8px;">', unsafe_allow_html=True)
        search_value = st.text_input(
            "Global Search",
            placeholder=search_placeholder,
            key=f"atlas_topbar_search_{active_page.lower().replace(' ', '_')}",
            label_visibility="collapsed",
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return search_value


def render_app_shell(
    active_page: str,
    subtitle: str,
    search_placeholder: str = "Search climate signals, regions, or datasets",
    show_search: bool = True,
) -> str:
    apply_atlas_theme()
    set_chart_theme(dark=not st.session_state.get("atlas_light_mode", False))
    render_sidebar_navigation(active_page)
    return render_topbar(active_page, subtitle, search_placeholder, show_search)


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



