from __future__ import annotations

import html

import streamlit as st

from ui_ux.stitch_effects import render_progress_bar


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


# ---------------------------------------------------------------------------
# Stitch Component Library — New render functions
# These are ADDITIVE.  Old render_metric_card(), render_feature_card(), etc.
# keep working exactly as before.  Pages can adopt these gradually.
# ---------------------------------------------------------------------------


def render_bento_card(
    title: str,
    value: str,
    unit: str,
    source: str,
    *,
    accent_color: str = "var(--atlas-primary-fixed-dim)",
    progress_pct: float | None = None,
    icon: str = "",
) -> None:
    """Large bento-style metric card with neo-brutalist inner border.

    Replaces the simpler render_metric_card() when a more prominent
    display is desired.  Works in both dark and light modes.
    """
    icon_html = (
        f'<span class="material-symbols-outlined" style="color: {accent_color}; font-size: 32px; opacity: 0.25;">{_esc(icon)}</span>'
        if icon
        else ""
    )
    progress_html = render_progress_bar(progress_pct, accent_color) if progress_pct is not None else ""
    st.markdown(
        f"""
        <div class="atlas-feature-card atlas-neo-border atlas-liquid-hover" style="padding: 1.5rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
                <div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.65rem; color: {accent_color}; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; margin-bottom: 0.25rem;">{_esc(title)}</div>
                </div>
                {icon_html}
            </div>
            <div style="background: var(--atlas-surface-container); border: 2px solid {accent_color}33; padding: 1rem;">
                <div style="display: flex; align-items: baseline; gap: 0.5rem;">
                    <span style="font-family: var(--atlas-font-heading); font-size: 2.75rem; font-weight: 700; color: {accent_color}; line-height: 1;">{_esc(value)}</span>
                    <span style="font-family: var(--atlas-font-heading); font-size: 1.15rem; color: var(--atlas-muted); opacity: 0.6;">{_esc(unit)}</span>
                </div>
                {progress_html}
                <div style="font-family: var(--atlas-font-mono); font-size: 0.65rem; color: var(--atlas-muted); margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">{_esc(source)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_anomaly_feed(items: list[dict[str, str]]) -> None:
    """Scrollable anomaly/event feed with colored left borders.

    Parameters
    ----------
    items : list[dict]
        Each item must have keys: severity, title, detail, time.
        severity maps to border color: 'critical' -> error, 'observation' -> primary,
        'metrics' -> tertiary.
    """
    if not items:
        st.info("No anomaly events to display.")
        return

    rows_html = ""
    for item in items:
        sev = item.get("severity", "observation").lower()
        if sev == "critical":
            border_color = "var(--atlas-error)"
            label_color = "var(--atlas-error)"
            label = "CRITICAL EVENT"
            bg = "rgba(255,180,171,0.05)"
            hover_bg = "rgba(255,180,171,0.10)"
        elif sev == "metrics":
            border_color = "var(--atlas-tertiary-fixed-dim)"
            label_color = "var(--atlas-tertiary-fixed-dim)"
            label = "METRICS"
            bg = "rgba(255,185,80,0.05)"
            hover_bg = "rgba(255,185,80,0.10)"
        else:
            border_color = "var(--atlas-primary-fixed-dim)"
            label_color = "var(--atlas-primary-fixed-dim)"
            label = "OBSERVATION"
            bg = "rgba(0,219,231,0.05)"
            hover_bg = "rgba(0,219,231,0.10)"

        rows_html += f"""
        <div class="atlas-anomaly-item" style="padding: 1rem; border-left: 2px solid {border_color}; background: {bg}; cursor: pointer; transition: background 0.2s;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                <span style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: {label_color}; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">{label}</span>
                <span style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted); opacity: 0.4;">{_esc(item.get('time', ''))}</span>
            </div>
            <div style="font-family: var(--atlas-font-heading); font-size: 0.88rem; color: var(--atlas-text); margin-bottom: 0.25rem; font-weight: 600;">{_esc(item.get('title', ''))}</div>
            <div style="font-family: var(--atlas-font-body); font-size: 0.78rem; color: var(--atlas-muted); line-height: 1.45; opacity: 0.8;">{_esc(item.get('detail', ''))}</div>
        </div>
        """

    st.markdown(
        f"""
        <div style="max-height: 500px; overflow-y: auto; scrollbar-width: thin;">
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_signal_card(
    label: str,
    value: str,
    change: str,
    *,
    change_color: str = "var(--atlas-error)",
    progress_pct: float | None = None,
) -> None:
    """Compact signal indicator card (e.g. AMOC Stability, Arctic Albedo).

    Used in grids to show key planetary signals with a small progress bar.
    """
    progress_html = render_progress_bar(progress_pct) if progress_pct is not None else ""
    st.markdown(
        f"""
        <div class="atlas-feature-card atlas-liquid-hover" style="padding: 1rem; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.08em;">{_esc(label)}</div>
            <div style="display: flex; align-items: baseline; gap: 0.4rem; margin-top: 0.5rem;">
                <span style="font-family: var(--atlas-font-heading); font-size: 1.5rem; font-weight: 700; color: var(--atlas-primary);">{_esc(value)}</span>
                <span style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: {change_color};">{_esc(change)}</span>
            </div>
            {progress_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alert_card(
    title: str,
    detail: str,
    *,
    severity: str = "warning",
    badge: str = "",
    distance: str = "",
) -> None:
    """Alert card with severity-colored border and optional distance badge.

    Parameters
    ----------
    severity : str
        'critical' -> error border, 'warning' -> tertiary, 'info' -> primary.
    badge : str
        Short label like 'L3_ALERT'.
    distance : str
        Distance string like '24km'.
    """
    if severity == "critical":
        border = "var(--atlas-error)"
        badge_bg = "var(--atlas-error)"
        badge_fg = "var(--atlas-on-error)"
    elif severity == "info":
        border = "var(--atlas-primary-fixed-dim)"
        badge_bg = "rgba(0,219,231,0.15)"
        badge_fg = "var(--atlas-primary)"
    else:
        border = "var(--atlas-tertiary-fixed-dim)"
        badge_bg = "rgba(255,185,80,0.15)"
        badge_fg = "var(--atlas-tertiary-fixed-dim)"

    badge_html = (
        f'<span style="background: {badge_bg}; color: {badge_fg}; padding: 2px 8px; font-family: var(--atlas-font-mono); font-size: 0.6rem; font-weight: 700; text-transform: uppercase;">{_esc(badge)}</span>'
        if badge
        else ""
    )
    distance_html = (
        f'<span style="font-family: var(--atlas-font-mono); font-size: 0.72rem; color: var(--atlas-muted);">{_esc(distance)}</span>'
        if distance
        else ""
    )
    st.markdown(
        f"""
        <div style="background: var(--atlas-surface-container); border: 2px solid {border}40; padding: 0.85rem; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <span style="font-family: var(--atlas-font-mono); font-size: 0.65rem; color: {border}; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;">{_esc(title)}</span>
                {badge_html}{distance_html}
            </div>
            <p style="font-size: 0.78rem; color: var(--atlas-muted); opacity: 0.7; margin: 0; line-height: 1.45;">{_esc(detail)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero_analysis(
    vector_label: str,
    value: str,
    unit: str,
    yoy_change: str,
    baseline: str,
    confidence_pct: float,
) -> None:
    """Large hero section for signal analysis pages (e.g. Climate Signals).

    Shows a dominant value display with trend indicator and confidence bar.
    """
    yoy_color = "var(--atlas-error)" if yoy_change.startswith("+") else "var(--atlas-primary-fixed-dim)"
    st.markdown(
        f"""
        <div class="atlas-hero" style="padding: 2rem 2.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        <span class="atlas-stitch-status-dot"></span>
                        <span style="font-family: var(--atlas-font-mono); font-size: 0.65rem; color: var(--atlas-primary-fixed-dim); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">CURRENT VECTOR: {_esc(vector_label)}</span>
                    </div>
                    <div style="font-family: var(--atlas-font-heading); font-size: 4rem; font-weight: 700; color: var(--atlas-primary); line-height: 1; margin-bottom: 0.5rem;">
                        {_esc(value)} <span style="font-size: 1.5rem; color: var(--atlas-muted); font-weight: 300;">{_esc(unit)}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-family: var(--atlas-font-mono); font-size: 0.82rem; color: {yoy_color}; display: flex; align-items: center; gap: 0.25rem;">
                            <span class="material-symbols-outlined" style="font-size: 16px;">trending_up</span> {_esc(yoy_change)} YOY
                        </span>
                        <span style="font-family: var(--atlas-font-mono); font-size: 0.82rem; color: var(--atlas-muted); opacity: 0.6;">BASELINE: {_esc(baseline)}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.65rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.35rem;">SIGNAL INTEGRITY</div>
                    <div style="width: 128px; height: 4px; background: rgba(255,255,255,0.1); position: relative;">
                        <div style="height: 100%; background: var(--atlas-primary-fixed-dim); width: {confidence_pct:.0f}%; box-shadow: 0 0 8px var(--atlas-primary-fixed-dim);"></div>
                    </div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-primary-fixed-dim); margin-top: 0.3rem;">{confidence_pct:.1f}% CONFIDENCE</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_planetary_gauge(score: float, max_score: float = 100.0) -> None:
    """SVG ring gauge for planetary health index or composite scores."""
    import math

    radius = 45
    circumference = 2 * math.pi * radius
    pct = min(score / max_score, 1.0)
    offset = circumference * (1 - pct)

    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: center; padding: 2rem;">
            <div style="font-family: var(--atlas-font-mono); font-size: 0.65rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 2rem;">PLANETARY HEALTH INDEX</div>
            <div style="position: relative; width: 192px; height: 192px;">
                <svg style="width: 100%; height: 100%; transform: rotate(-90deg);" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="{radius}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2"/>
                    <circle cx="50" cy="50" r="{radius}" fill="none" stroke="var(--atlas-primary-fixed-dim)" stroke-width="4"
                            stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
                            style="filter: drop-shadow(0 0 6px var(--atlas-primary-fixed-dim));"/>
                </svg>
                <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <span style="font-family: var(--atlas-font-heading); font-size: 2.5rem; font-weight: 700; color: var(--atlas-primary); line-height: 1;">{score:.1f}</span>
                    <span style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted);">/ {max_score:.1f}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ticker_bar(items: list[dict[str, str]]) -> None:
    """Render the horizontal scrolling telemetry ticker inside the page.

    Wraps the HTML generation from stitch_effects and injects via st.markdown.
    """
    from ui_ux.stitch_effects import render_ticker_bar as _build_ticker

    ticker_html = _build_ticker(items)
    if ticker_html:
        st.markdown(ticker_html, unsafe_allow_html=True)
