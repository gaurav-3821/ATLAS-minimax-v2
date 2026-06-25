# ATLAS Climate Intelligence Platform

![Operational Dashboard](assets/stitch/c842b64b351144098ca8a9f66fda9187.png)

ATLAS is a dark, multi-page Streamlit climate product built around stable live APIs, historical NetCDF analysis, risk scoring, model-assisted forecasting, and report generation.

The current build blends:

- **Liquid glassmorphism** — animated frosted-glass panels with shimmer sweeps and ambient blob drift
- **Mission Control aesthetic** — Hanken Grotesk headlines, JetBrains Mono telemetry, Fira Sans body
- **Scientific Vanguard styling** — atmospheric cyan accents, emergency amber alerts, critical red risks
- **Light / Dark mode** — toggleable with persistent OS preference detection

## Product Modules

| Module | Preview |
|--------|---------|
| `Landing` — premium product intro with global preview and source status | |
| `Story Mode` — guided climate narrative with chapter-based maps, charts, and projections | ![Story Mode](assets/stitch/ed84600642b2473b9b77939fc789c157.png) |
| `Dashboard` — live climate metrics, AQI, forecast, and risk radar | ![Dashboard](assets/stitch/c842b64b351144098ca8a9f66fda9187.png) |
| `Global Map` — interactive globe, heatmaps, hotspots, and satellite context | ![Global Map](assets/stitch/eca433e368d546d9a9bb3173a02a898a.png) |
| `Climate Signals` — long-range anomalies and comparison views | ![Climate Signals](assets/stitch/2dad4a79aca3455aaaac8b0b880a1f34.png) |
| `Risk Intelligence` — flood, wildfire, heatwave, storm, and AQI scoring | ![Risk Intelligence](assets/stitch/04bb64e6cdff402c864ac665584ef7d9.png) |
| `Predictions` — model-assisted outlooks and natural-language query steering | ![Predictions](assets/stitch/b4d76faa56f64639a1e047c048891277.png) |
| `Data Explorer` — open exploration, local extraction, compare mode, and timelapse | ![Data Explorer](assets/stitch/47909802617c4669925890e5307cb673.png) |
| `Research Lab` — dataset upload, scenario simulation, and model testing | ![Research Lab](assets/stitch/6edc8da5f2bb40d19981f5ac9f7cd414.png) |
| `Reports` — markdown and PDF climate briefing export | ![Reports](assets/stitch/65fa88f443984c12ac552a0320033b63.png) |
| `Settings` — API credential inputs and source readiness | ![Settings](assets/stitch/36e5dad0848e4d70b412bfbd0d6bd40c.png) |

## Design System

ATLAS uses a custom design system called **Atmos Mission Control** with the following tokens:

- **Color palette**: Deep space (#020408) base, atmospheric cyan (#00E5FF) primary, emergency amber (#FFAB00) tertiary, critical red (#FF3D00) for alerts
- **Typography**: Hanken Grotesk (headlines), Inter (body), JetBrains Mono (data/labels)
- **Glassmorphism**: `backdrop-filter: blur(28px)`, multi-layer shadows, radial caustic overlays, animated shimmer sweeps
- **Border radius**: Organic 16–36px for cards, 8px for buttons/inputs
- **Spacing**: 4px base unit, 24px gutters, 48px page margins (desktop)

> Full design tokens and component specs are available in the Stitch MCP design system (`assets/stitch/`).

## Live APIs

Deploy-profile live integrations:

- `NASA GIBS`
- `NOAA Climate Data Online`
- `OpenWeatherMap`

Deferred for the hackathon deploy profile:

- `Copernicus Climate Data`
- `Google Earth Engine`

## Credentials

ATLAS now defaults to server-side credentials only:

1. environment variables
2. `.streamlit/secrets.toml`
3. optional runtime inputs only when `ATLAS_ENABLE_RUNTIME_CREDENTIAL_INPUTS=true`

Supported names:

```bash
OPENWEATHER_API_KEY=<your key>
NOAA_API_TOKEN=<your token>
ATLAS_DEFAULT_LOCATION=Delhi, IN
ATLAS_ENABLE_RUNTIME_CREDENTIAL_INPUTS=false
```

An example template is included at `.streamlit/secrets.example.toml`.

## Local Setup

1. Create and activate a Python 3.10+ environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

4. Add server-side credentials through `.streamlit/secrets.toml` or environment variables.

## One-Click Deploy

ATLAS includes `render.yaml` for a simple Render deployment.

Set these environment variables in the host:

```bash
OPENWEATHER_API_KEY=<your key>
NOAA_API_TOKEN=<your token>
ATLAS_DEFAULT_LOCATION=Delhi, IN
ATLAS_ENABLE_RUNTIME_CREDENTIAL_INPUTS=false
```

## Verification

Run the lightweight smoke test:

```bash
python smoke_check.py
```

Expected output:

```text
ATLAS smoke check passed.
```

Run the live provider check before deployment:

```bash
python live_api_check.py
```

This verifies the configured OpenWeather, NOAA, and NASA GIBS paths against a known diagnostic location.

## Historical Dataset

The bundled synthetic dataset is generated automatically on first launch and includes:

- `t2m`
- `precipitation`
- `sea_level_pressure`
- `wind_speed`

Expected coordinate names:

- `time`
- `lat` or `latitude`
- `lon` or `longitude`

## Notes

- The historical workspace remains usable even when live APIs are offline.
- `Reports` falls back to markdown bytes if PDF libraries are unavailable.
- `runtime.txt` pins the hosted Python version for Streamlit deployments.
- Copernicus and Google Earth Engine were intentionally deferred from the deploy profile to keep the hackathon demo reliable.
