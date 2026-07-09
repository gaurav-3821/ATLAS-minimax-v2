from __future__ import annotations

import pandas as pd
import streamlit as st

from ui_ux.chart_factory import (
    create_air_quality_figure,
    create_anomaly_bar_figure,
    create_donut_figure,
    create_forecast_delta_figure,
    create_forecast_figure,
    create_gauge_figure,
    create_live_signal_figure,
    create_ranked_bar_figure,
    create_risk_timeline_figure,
    create_risk_radar,
    create_station_history_figure,
    create_timeline_figure,
)
from utils.data_loader import detect_axes, get_active_dataset, spatial_mean_series, to_display_array
from utils.live_data import (
    fetch_air_quality_with_source,
    fetch_current_weather_with_source,
    fetch_forecast_with_source,
    fetch_noaa_station_history_with_source,
    get_default_location_query,
    resolve_location_with_source,
)
from utils.risk_engine import build_risk_profile, build_risk_timeline
from utils.real_climate import get_real_global_temperature_frames
from ui_ux.style import render_app_shell, render_feature_card, render_info_banner, render_page_hero, render_section_intro
from ui_ux.stitch_components import render_bento_card, render_alert_card, render_ticker_bar


st.set_page_config(page_title="ATLAS | Dashboard", page_icon=":material/dashboard:", layout="wide")


def main() -> None:
    topbar_search = render_app_shell(
        "Dashboard",
        "Global KPI summary, live location monitoring, and top-line climate risk signals.",
        search_placeholder="Search a city, signal, or climate KPI",
    )
    if topbar_search:
        st.session_state["atlas_ops_location"] = topbar_search

    location_query = st.session_state.get("atlas_ops_location", "Delhi, IN")

    render_page_hero(
        "Mission control",
        "Dashboard",
        "A premium control surface for live weather, historical climate context, and risk signals focused on Delhi operations by default.",
        subtitle="Delhi live metrics, alerts, and long-range climate context",
    )

    with st.sidebar:
        st.header("Operational inputs")
        history_days = st.slider("NOAA history window", min_value=14, max_value=90, value=45, step=1)

    dataset, source_label = get_active_dataset()
    data_array = to_display_array(dataset["t2m"], "t2m")
    axes = detect_axes(data_array)
    real_monthly, real_annual, real_source = get_real_global_temperature_frames()
    if real_monthly is not None:
        global_df = real_monthly.rename(columns={"anomaly": "temperature"})[["time", "temperature"]].copy()
        source_label = real_source
    else:
        global_series = spatial_mean_series(data_array, axes, "Global", anomaly_mode=False)
        global_df = global_series.to_dataframe(name="temperature").reset_index().rename(columns={axes["time"]: "time"})
    recent_anomaly = float(global_df["temperature"].iloc[-1] - global_df["temperature"].tail(min(len(global_df), 120)).mean())
    anomaly_baseline = float(global_df["temperature"].tail(min(len(global_df), 240)).mean())
    anomaly_bars = global_df.tail(24).copy()
    anomaly_bars["anomaly"] = anomaly_bars["temperature"] - anomaly_baseline

    with st.spinner("Connecting to live data sources..."):
        location, resolved_weather, location_source = resolve_location_with_source(location_query)
        if resolved_weather:
            weather = resolved_weather
            weather_source = location_source
        else:
            weather, weather_source = fetch_current_weather_with_source(location["lat"], location["lon"])
        forecast_df, forecast_source = fetch_forecast_with_source(location["lat"], location["lon"])
        air_current, air_forecast, air_source = fetch_air_quality_with_source(location["lat"], location["lon"])
        noaa_result, noaa_source = fetch_noaa_station_history_with_source(location["lat"], location["lon"], days=history_days)
    source_items = [weather_source, forecast_source, air_source, noaa_source]
    live_count = sum(1 for item in source_items if item["is_live"])

    risk_profile = build_risk_profile(
        weather or {"temperature_c": 0.0, "humidity_pct": 0.0, "wind_mps": 0.0, "pressure_hpa": 1013.0},
        forecast_df,
        air_current or {"aqi": 1, "pm2_5": 0.0},
        noaa_result["history"] if noaa_result else None,
    )
    risk_timeline = build_risk_timeline(forecast_df)

    render_info_banner(
        f"Tracking {location['label']} with {live_count}/{len(source_items)} live operational feeds. "
        f"Global temperature anomaly source: {source_label}."
    )

    ticker_items = [
        {"icon": "thermostat", "label": "GLOBAL", "value": f"{global_df['temperature'].iloc[-1]:+.2f} C", "color": "var(--atlas-primary-fixed-dim)"},
        {"icon": "location_on", "label": location["label"].split(",")[0].upper(), "value": f"{weather['temperature_c']:.1f} C" if weather else "N/A", "color": "var(--atlas-tertiary-fixed-dim)"},
        {"icon": "air", "label": "AQI", "value": f"{air_current['aqi']}" if air_current else "N/A", "color": "var(--atlas-error)"},
        {"icon": "warning", "label": "RISK", "value": f"{risk_profile['composite']:.0f}/100", "color": "var(--atlas-primary-fixed-dim)"},
        {"icon": "satellite_alt", "label": "FEEDS", "value": f"{live_count}/{len(source_items)} LIVE", "color": "var(--atlas-primary-fixed-dim)"},
    ]
    render_ticker_bar(ticker_items)

    render_feature_card("Operational target", f"Primary dashboard context is pinned to {location['label'] if location else 'Delhi, IN'} so the live and historical views point to the same place.")
    source_cols = st.columns(4)
    for column, title, source in zip(source_cols, ["Weather", "Forecast", "AQI", "Station"], source_items):
        with column:
            render_feature_card(f"{title}: {source['mode']}", str(source["detail"]))

    metric_cols = st.columns(5)
    with metric_cols[0]:
        render_bento_card("Global Anomaly", f"{global_df['temperature'].iloc[-1]:+.2f}", "C", f"Source: {source_label}", icon="thermostat")
    with metric_cols[1]:
        if weather:
            render_bento_card("Tracked City", f"{weather['temperature_c']:.1f}", "C", str(location["label"]), icon="location_on")
        else:
            render_bento_card("Tracked City", "N/A", "", "Offline demo", icon="location_off")
    with metric_cols[2]:
        if air_current:
            render_bento_card("Air Quality", f"AQI {air_current['aqi']}", "", str(air_current["category"]), icon="air", accent_color="var(--atlas-error)")
        else:
            render_bento_card("Air Quality", "N/A", "", "Offline demo", icon="air", accent_color="var(--atlas-muted)")
    with metric_cols[3]:
        render_bento_card("Climate Anomaly", f"{recent_anomaly:+.2f}", "C", "Relative to trailing 10-year mean", icon="trending_up")
    with metric_cols[4]:
        render_bento_card("Risk Index", f"{risk_profile['composite']:.0f}", "/100", str(risk_profile["composite_label"]), icon="warning", progress_pct=risk_profile["composite"])

    render_section_intro(
        "Executive surface",
        "Top-level views center on Delhi forecast dynamics, air quality, and risk progression, with fallback data when live services are unavailable.",
        eyebrow="Overview",
    )
    top_left, top_right = st.columns((1.18, 0.82))
    with top_left:
        if not forecast_df.empty and location:
            st.plotly_chart(
                create_live_signal_figure(forecast_df, title=f"{location['label']} live signal ribbon"),
                use_container_width=True,
            )
        else:
            st.plotly_chart(
                create_timeline_figure(
                    global_df,
                    title="Global activity timeline",
                    value_column="temperature",
                    y_label="Global temperature anomaly (deg C)",
                ),
                use_container_width=True,
            )
    with top_right:
        radar_tab, mix_tab = st.tabs(["Radar", "Mix"])
        with radar_tab:
            st.plotly_chart(
                create_risk_radar(risk_profile["scores"], title="Risk intelligence radar"),
                use_container_width=True,
            )
        with mix_tab:
            st.plotly_chart(
                create_donut_figure(risk_profile["scores"], title="Hazard share"),
                use_container_width=True,
            )

    chart_left, chart_mid, chart_right = st.columns(3)
    with chart_left:
        render_section_intro(
            "Composite risk gauge",
            "A single dial makes the overall operational climate posture easy to read during a fast demo.",
            eyebrow="Indicator",
        )
        st.plotly_chart(
            create_gauge_figure(risk_profile["composite"], title="Composite risk", suffix="/100"),
            use_container_width=True,
        )
    with chart_mid:
        render_section_intro(
            "Hazard ranking",
            "Ranked bars make it obvious which hazard is leading instead of hiding the signal in cards alone.",
            eyebrow="Ranking",
        )
        st.plotly_chart(
            create_ranked_bar_figure(risk_profile["scores"], title="Hazard scores", x_label="Risk score"),
            use_container_width=True,
        )
    with chart_right:
        render_section_intro(
            "Risk pulse timeline",
            "Stacked risk curves make the next Delhi forecast window feel more operational and easier to scan at a glance.",
            eyebrow="Pulse",
        )
        if not risk_timeline.empty:
            st.plotly_chart(
                create_risk_timeline_figure(risk_timeline, title="Delhi forecast risk pulse"),
                use_container_width=True,
            )
        else:
            st.plotly_chart(
                create_anomaly_bar_figure(
                    anomaly_bars[["time", "anomaly"]],
                    title="Global anomaly bars",
                    value_column="anomaly",
                    y_label="Temperature anomaly (deg C)",
                ),
                use_container_width=True,
            )

    alerts_col, forecast_col = st.columns((0.82, 1.18))
    with alerts_col:
        render_section_intro(
            "Extreme weather alerts",
            "Risk panels synthesize live weather, forecast progression, station history, and AQI.",
            eyebrow="Alerts",
        )
        for title, panel in risk_profile["panels"].items():
            severity = "critical" if panel["score"] >= 70 else "warning" if panel["score"] >= 40 else "info"
            render_alert_card(title, f"Score {panel['score']:.0f}/100 - {panel['label']}", severity=severity)
        if risk_profile["alerts"]:
            for alert in risk_profile["alerts"]:
                render_info_banner(alert)
        else:
            render_info_banner("No elevated climate risk signals were triggered by the current ruleset.")

    with forecast_col:
        render_section_intro(
            "Forecast track",
            "OpenWeather three-hour forecasts feed the short-range Delhi outlook with smoother chart styling and clearer change signals.",
            eyebrow="Nowcasting",
        )
        if forecast_df.empty:
            st.info("Forecast data is unavailable until a valid live location is resolved.")
        else:
            st.plotly_chart(
                create_forecast_figure(forecast_df, title=f"{location['label']} forecast"),
                use_container_width=True,
            )
            st.plotly_chart(
                create_forecast_delta_figure(forecast_df, title="Forecast change bars"),
                use_container_width=True,
            )

    lower_left, lower_right = st.columns(2)
    with lower_left:
        render_section_intro(
            "Air quality stack",
            "AQI and particulate trends provide a direct Delhi health-risk layer using the live air-pollution feed.",
            eyebrow="AQI",
        )
        if air_forecast.empty:
            st.info("Air quality forecast is unavailable for the current location.")
        else:
            st.plotly_chart(
                create_air_quality_figure(air_forecast, title=f"{location['label']} air quality"),
                use_container_width=True,
            )

    with lower_right:
        render_section_intro(
            "Ground truth",
            "Nearby NOAA station history helps ground the short-range dashboard in observed conditions.",
            eyebrow="Station",
        )
        if noaa_result and not noaa_result["history"].empty:
            station = noaa_result["station"]
            st.plotly_chart(
                create_station_history_figure(noaa_result["history"], title=f"{station['name']} recent history"),
                use_container_width=True,
            )
        else:
            st.info("NOAA station data is unavailable or no daily summaries were returned for the selected window.")


if __name__ == "__main__":
    main()
