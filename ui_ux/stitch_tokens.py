from __future__ import annotations


# ---------------------------------------------------------------------------
# ATLAS Stitch Design Tokens
# Extracted from Google Stitch MCP-generated HTML specs in assets/stitch/
# These mirror the Material Design 3 color system used across all Stitch
# page specs.  Import and use in any new component or CSS string.
# ---------------------------------------------------------------------------

# ── Color Palette (Dark Mode) ──────────────────────────────────────────────
COLORS_DARK: dict[str, str] = {
    "background": "#111318",
    "on-background": "#e2e2e8",
    "surface": "#111318",
    "surface-dim": "#111318",
    "surface-bright": "#37393e",
    "surface-variant": "#333539",
    "surface-container-lowest": "#0c0e12",
    "surface-container-low": "#1a1c20",
    "surface-container": "#1e2024",
    "surface-container-high": "#282a2e",
    "surface-container-highest": "#333539",
    "surface-tint": "#00dbe7",
    "primary": "#e1fdff",
    "primary-fixed": "#74f5ff",
    "primary-fixed-dim": "#00dbe7",
    "primary-container": "#00f2ff",
    "on-primary": "#00363a",
    "on-primary-fixed": "#002022",
    "on-primary-fixed-variant": "#004f54",
    "on-primary-container": "#006a71",
    "inverse-primary": "#00696f",
    "secondary": "#d1bcff",
    "secondary-fixed": "#e9ddff",
    "secondary-fixed-dim": "#d1bcff",
    "secondary-container": "#7000ff",
    "on-secondary": "#3c0090",
    "on-secondary-fixed": "#23005b",
    "on-secondary-fixed-variant": "#5700c9",
    "on-secondary-container": "#ddcdff",
    "tertiary": "#fff6ef",
    "tertiary-fixed": "#ffddb3",
    "tertiary-fixed-dim": "#ffb950",
    "tertiary-container": "#ffd49c",
    "on-tertiary": "#452b00",
    "on-tertiary-fixed": "#291800",
    "on-tertiary-fixed-variant": "#624000",
    "on-tertiary-container": "#845600",
    "error": "#ffb4ab",
    "error-container": "#93000a",
    "on-error": "#690005",
    "on-error-container": "#ffdad6",
    "on-surface": "#e2e2e8",
    "on-surface-variant": "#b9cacb",
    "outline": "#849495",
    "outline-variant": "#3a494b",
    "inverse-surface": "#e2e2e8",
    "inverse-on-surface": "#2f3035",
}

# ── Color Palette (Light Mode) ─────────────────────────────────────────────
COLORS_LIGHT: dict[str, str] = {
    "background": "#f0f4f8",
    "on-background": "#0f172a",
    "surface": "#f8fafc",
    "surface-dim": "#f0f4f8",
    "surface-bright": "#ffffff",
    "surface-variant": "#e2e8f0",
    "surface-container-lowest": "#ffffff",
    "surface-container-low": "#f8fafc",
    "surface-container": "#f1f5f9",
    "surface-container-high": "#e2e8f0",
    "surface-container-highest": "#e2e8f0",
    "surface-tint": "#0891b2",
    "primary": "#0891b2",
    "primary-fixed": "#cffafe",
    "primary-fixed-dim": "#0891b2",
    "primary-container": "#22d3ee",
    "on-primary": "#ffffff",
    "on-primary-fixed": "#002022",
    "on-primary-fixed-variant": "#004f54",
    "on-primary-container": "#164e63",
    "inverse-primary": "#00696f",
    "secondary": "#6366f1",
    "secondary-fixed": "#e9ddff",
    "secondary-fixed-dim": "#a5b4fc",
    "secondary-container": "#a5b4fc",
    "on-secondary": "#ffffff",
    "on-secondary-fixed": "#23005b",
    "on-secondary-fixed-variant": "#5700c9",
    "on-secondary-container": "#312e81",
    "tertiary": "#1e293b",
    "tertiary-fixed": "#ffddb3",
    "tertiary-fixed-dim": "#d97706",
    "tertiary-container": "#d97706",
    "on-tertiary": "#ffffff",
    "on-tertiary-fixed": "#291800",
    "on-tertiary-fixed-variant": "#624000",
    "on-tertiary-container": "#78350f",
    "error": "#dc2626",
    "error-container": "#fecaca",
    "on-error": "#ffffff",
    "on-error-container": "#7f1d1d",
    "on-surface": "#0f172a",
    "on-surface-variant": "#334155",
    "outline": "#64748b",
    "outline-variant": "#e2e8f0",
    "inverse-surface": "#0f172a",
    "inverse-on-surface": "#f8fafc",
}

# ── Typography Tokens ──────────────────────────────────────────────────────
FONT_FAMILIES: dict[str, str] = {
    "display-lg": "Space Grotesk, sans-serif",
    "headline-md": "Space Grotesk, sans-serif",
    "body-md": "Geist, sans-serif",
    "data-mono": "JetBrains Mono, monospace",
    "label-caps": "JetBrains Mono, monospace",
}

FONT_SIZES: dict[str, dict[str, str]] = {
    "display-lg": {"size": "48px", "line-height": "56px", "letter-spacing": "-0.02em", "weight": "700"},
    "display-lg-mobile": {"size": "32px", "line-height": "40px", "letter-spacing": "-0.02em", "weight": "700"},
    "headline-md": {"size": "24px", "line-height": "32px", "letter-spacing": "normal", "weight": "500"},
    "body-md": {"size": "16px", "line-height": "24px", "letter-spacing": "normal", "weight": "400"},
    "data-mono": {"size": "14px", "line-height": "20px", "letter-spacing": "0.05em", "weight": "500"},
    "label-caps": {"size": "11px", "line-height": "16px", "letter-spacing": "0.1em", "weight": "700"},
}

# ── Spacing Tokens ─────────────────────────────────────────────────────────
SPACING: dict[str, str] = {
    "unit": "4px",
    "margin-sm": "16px",
    "gutter": "16px",
    "margin-md": "32px",
    "margin-lg": "48px",
    "container-max": "1440px",
}

# ── Border Radius Tokens ───────────────────────────────────────────────────
BORDER_RADIUS: dict[str, str] = {
    "DEFAULT": "0.25rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "full": "9999px",
}

# ── Semantic Color Aliases (for quick reference) ───────────────────────────
# These map intent names to the actual palette values for dark mode.
SEMANTIC_DARK: dict[str, str] = {
    "glass-fill": "rgba(255,255,255,0.05)",
    "glass-border": "rgba(255,255,255,0.10)",
    "glass-edge": "rgba(255,255,255,0.20)",
    "glass-blur": "20px",
    "glass-saturate": "180%",
    "shadow-glass": "0 8px 32px rgba(0,0,0,0.3)",
    "shadow-sidebar": "10px 0 30px rgba(0,0,0,0.3)",
    "shadow-topbar": "0 0 20px rgba(0,219,231,0.1)",
    "accent-cyan": "#00dbe7",
    "accent-purple": "#7000ff",
    "accent-yellow": "#ffb950",
    "accent-pink": "#FF5C8A",
    "accent-green": "#6EFF9A",
    "accent-error": "#ffb4ab",
}

SEMANTIC_LIGHT: dict[str, str] = {
    "glass-fill": "rgba(255,255,255,0.7)",
    "glass-border": "rgba(0,0,0,0.08)",
    "glass-edge": "rgba(255,255,255,0.9)",
    "glass-blur": "20px",
    "glass-saturate": "180%",
    "shadow-glass": "0 8px 32px rgba(0,0,0,0.06)",
    "shadow-sidebar": "10px 0 30px rgba(0,0,0,0.06)",
    "shadow-topbar": "0 0 20px rgba(0,0,0,0.04)",
    "accent-cyan": "#0891b2",
    "accent-purple": "#6366f1",
    "accent-yellow": "#d97706",
    "accent-pink": "#e11d48",
    "accent-green": "#16a34a",
    "accent-error": "#dc2626",
}

# ── Navigation Items (Stitch version — 5 core + 2 utility) ────────────────
NAV_ITEMS_STITCH: list[dict[str, str]] = [
    {"label": "Story Mode", "route": "/Story_Mode", "icon": "play_circle"},
    {"label": "Dashboard", "route": "/Dashboard", "icon": "dashboard"},
    {"label": "Global Map", "route": "/Global_Climate_Map", "icon": "public"},
    {"label": "Climate Signals", "route": "/Climate_Signals", "icon": "query_stats"},
    {"label": "Risk Intelligence", "route": "/Risk_Intelligence", "icon": "warning"},
    {"label": "Predictions", "route": "/AI_Predictions", "icon": "insights"},
    {"label": "Data Explorer", "route": "/Data_Explorer", "icon": "travel_explore"},
    {"label": "Research Lab", "route": "/Research_Lab", "icon": "science"},
]

NAV_ITEMS_SECONDARY: list[dict[str, str]] = [
    {"label": "Reports", "route": "/Reports", "icon": "description"},
    {"label": "Settings", "route": "/Settings", "icon": "settings"},
    {"label": "Landing", "route": "/", "icon": "home"},
]
