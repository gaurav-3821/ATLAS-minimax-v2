from __future__ import annotations


# ---------------------------------------------------------------------------
# ATLAS Stitch Visual Effects — CSS Strings
# Pure CSS effects extracted from the Stitch HTML specs.  These are designed
# to be injected alongside the existing ATLAS_CSS via st.markdown().
# No JavaScript required — all effects are CSS-only.
# ---------------------------------------------------------------------------

# ── Scan Line Effect ───────────────────────────────────────────────────────
# A thin horizontal line that sweeps from top to bottom across the viewport.
STITCH_SCANLINE = """
<style>
    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, rgba(0,219,231,0.15) 50%, transparent 100%);
        z-index: 9999;
        pointer-events: none;
        animation: stitchScanline 8s linear infinite;
    }
    @keyframes stitchScanline {
        0%   { top: -2px; }
        100% { top: 100vh; }
    }
    @media (prefers-reduced-motion: reduce) {
        .stApp::after { animation: none; display: none; }
    }
</style>
"""

# ── Noise Texture Overlay ─────────────────────────────────────────────────
# Subtle grain overlay on all glass panels to add depth.
STITCH_NOISE_TEXTURE = """
<style>
    .atlas-glass-panel::before,
    .atlas-hero::before,
    .atlas-feature-card::before,
    .atlas-metric-card::before,
    .atlas-source-card::before,
    .atlas-info-banner::before,
    .atlas-story-panel::before,
    .atlas-section-head::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.025;
        pointer-events: none;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
        background-size: 128px 128px;
        z-index: 0;
    }
    .atlas-glass-panel,
    .atlas-hero,
    .atlas-feature-card,
    .atlas-metric-card,
    .atlas-source-card,
    .atlas-info-banner,
    .atlas-story-panel,
    .atlas-section-head {
        position: relative;
    }
</style>
"""

# ── Neo-Brutalist Border ───────────────────────────────────────────────────
# Thicker 2px accent border variant for high-emphasis cards.
STITCH_NEO_BRUTALIST = """
<style>
    .atlas-neo-border {
        border: 2px solid rgba(0,219,231,0.25) !important;
    }
    .atlas-neo-border-error {
        border: 2px solid rgba(255,180,171,0.35) !important;
    }
    html[data-theme="light"] .atlas-neo-border {
        border-color: rgba(8,145,178,0.25) !important;
    }
    html[data-theme="light"] .atlas-neo-border-error {
        border-color: rgba(220,38,38,0.25) !important;
    }
</style>
"""

# ── Liquid Hover Effect ────────────────────────────────────────────────────
# Cards get brighter blur + glow on hover.
STITCH_LIQUID_HOVER = """
<style>
    .atlas-liquid-hover {
        transition: backdrop-filter 0.3s ease, background 0.3s ease, box-shadow 0.3s ease !important;
    }
    .atlas-liquid-hover:hover {
        backdrop-filter: blur(30px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(200%) !important;
        background: rgba(255,255,255,0.08) !important;
        box-shadow: 0 0 20px rgba(0,219,231,0.12) !important;
    }
    html[data-theme="light"] .atlas-liquid-hover:hover {
        background: rgba(255,255,255,0.85) !important;
        box-shadow: 0 0 20px rgba(8,145,178,0.08) !important;
    }
</style>
"""

# ── Laser Focus Ring ───────────────────────────────────────────────────────
# Accent glow on focus for inputs and interactive elements.
STITCH_LASER_FOCUS = """
<style>
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: var(--atlas-primary-fixed-dim) !important;
        box-shadow: 0 0 15px rgba(0,219,231,0.3), inset 0 2px 4px rgba(0,0,0,0.2), 0 0 0 3px rgba(0,219,231,0.15) !important;
    }
    html[data-theme="light"] .stTextInput input:focus,
    html[data-theme="light"] .stTextArea textarea:focus,
    html[data-theme="light"] .stNumberInput input:focus {
        box-shadow: 0 0 15px rgba(8,145,178,0.2), inset 0 2px 4px rgba(0,0,0,0.04), 0 0 0 3px rgba(8,145,178,0.1) !important;
    }
</style>
"""

# ── Telemetry Ticker ───────────────────────────────────────────────────────
# Horizontal scrolling bar for live data feeds.  Accepts items as a list
# of dicts with keys: icon, label, value, color.
STITCH_TICKER_ITEM_TEMPLATE = """
<div style="display: flex; align-items: center; gap: 1rem;">
    <span class="material-symbols-outlined" style="color: {color}">{icon}</span>
    <span class="atlas-topbar-kicker">{label}</span>
    <span style="font-family: var(--atlas-font-mono); font-size: 0.72rem; color: {color}; font-weight: 600;">{value}</span>
</div>
<div style="height: 16px; width: 1px; background: rgba(255,255,255,0.15);"></div>
"""


def render_ticker_css() -> str:
    """Return CSS for the horizontal scrolling telemetry ticker."""
    return """
    <style>
        .atlas-ticker-wrap {
            overflow: hidden;
            white-space: nowrap;
            width: 100%;
        }
        .atlas-ticker-track {
            display: inline-flex;
            align-items: center;
            gap: 2rem;
            animation: atlasTickerScroll 40s linear infinite;
            padding: 0 1rem;
        }
        .atlas-ticker-track:hover {
            animation-play-state: paused;
        }
        @keyframes atlasTickerScroll {
            0%   { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        @media (prefers-reduced-motion: reduce) {
            .atlas-ticker-track { animation: none; }
        }
    </style>
    """


def render_ticker_bar(items: list[dict[str, str]]) -> str:
    """Build the HTML for a scrolling telemetry ticker bar.

    Parameters
    ----------
    items : list[dict]
        Each item must have keys: icon, label, value, color.
        Items are duplicated internally for a seamless loop.
    """
    if not items:
        return ""

    inner = ""
    for item in items:
        inner += STITCH_TICKER_ITEM_TEMPLATE.format(**item)

    # Duplicate for seamless loop
    duplicated = inner + inner

    return (
        f'<div class="atlas-ticker-wrap glass-panel" style="height: 64px; display: flex; align-items: center;">'
        f'<div class="atlas-ticker-track">{duplicated}</div>'
        f"</div>"
    )


# ── Bento Card Inner Glow ─────────────────────────────────────────────────
# Inner highlight line at the top-left edge of glass panels.
STITCH_INNER_GLOW = """
<style>
    .atlas-inner-glow {
        box-shadow: inset 1px 1px 0px rgba(255,255,255,0.12);
    }
    html[data-theme="light"] .atlas-inner-glow {
        box-shadow: inset 1px 1px 0px rgba(255,255,255,0.7);
    }
</style>
"""

# ── Active Status Dot ──────────────────────────────────────────────────────
# Pulsing dot for live status indicators.
STITCH_STATUS_DOT = """
<style>
    .atlas-stitch-status-dot {
        width: 8px;
        height: 8px;
        background-color: var(--atlas-primary-fixed-dim);
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px var(--atlas-primary-fixed-dim);
        animation: atlasPulseDot 2s infinite ease-in-out;
    }
    .atlas-stitch-status-dot-error {
        background-color: var(--atlas-error);
        box-shadow: 0 0 8px var(--atlas-error);
    }
    .atlas-stitch-status-dot-warning {
        background-color: var(--atlas-tertiary-fixed-dim);
        box-shadow: 0 0 8px var(--atlas-tertiary-fixed-dim);
    }
</style>
"""

# ── Progress Bar (inline metric) ───────────────────────────────────────────
# Thin horizontal bar used inside bento cards.
STITCH_PROGRESS_BAR = """
<style>
    .atlas-progress-track {
        width: 100%;
        height: 4px;
        background: rgba(255,255,255,0.08);
        margin-top: 12px;
        position: relative;
        overflow: hidden;
    }
    .atlas-progress-fill {
        height: 100%;
        transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    }
    html[data-theme="light"] .atlas-progress-track {
        background: rgba(0,0,0,0.06);
    }
</style>
"""


def render_progress_bar(pct: float, color: str = "var(--atlas-primary-fixed-dim)") -> str:
    """Return HTML for a thin progress bar.

    Parameters
    ----------
    pct : float
        Fill percentage (0-100).
    color : str
        CSS color for the fill.
    """
    pct = max(0.0, min(100.0, pct))
    return (
        f'<div class="atlas-progress-track">'
        f'<div class="atlas-progress-fill" style="width: {pct:.0f}%; background: {color};"></div>'
        f"</div>"
    )


# ── Combined Stitch Effects Bundle ─────────────────────────────────────────
# Single string that injects all Stitch visual effects at once.
# Call this from apply_atlas_theme() or render_app_shell().
ALL_STITCH_EFFECTS = "\n".join([
    STITCH_SCANLINE,
    STITCH_NOISE_TEXTURE,
    STITCH_NEO_BRUTALIST,
    STITCH_LIQUID_HOVER,
    STITCH_LASER_FOCUS,
    STITCH_INNER_GLOW,
    STITCH_STATUS_DOT,
    STITCH_PROGRESS_BAR,
    render_ticker_css(),
    """
    <style>
        .atlas-anomaly-item:hover {
            background: rgba(0,219,231,0.08) !important;
        }
        html[data-theme="light"] .atlas-anomaly-item:hover {
            background: rgba(8,145,178,0.06) !important;
        }
    </style>
    """,
])
