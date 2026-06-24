from __future__ import annotations

import streamlit as st

from ui_ux.chart_factory import (
    create_air_quality_figure,
    create_donut_figure,
    create_forecast_figure,
    create_gauge_figure,
    create_ranked_bar_figure,
    create_risk_radar,
    create_risk_timeline_figure,
    create_station_history_figure,
)
from utils.live_data import fetch_air_quality, fetch_forecast, fetch_noaa_station_history, fetch_current_weather, get_default_location_query, resolve_location
from utils.risk_engine import build_risk_profile, build_risk_timeline
from ui_ux.style import render_app_shell, render_feature_card, render_info_banner, render_metric_card, render_page_hero, render_section_intro


st.set_page_config(page_title="ATLAS | Risk Intelligence", page_icon=":material/warning:", layout="wide")


def main() -> None:
    topbar_search = render_app_shell(
        "Risk Intelligence",
        "Hazard scoring, AQI context, and short-range operational alerts for a selected location.",
        search_placeholder="Search heatwave, flood, wildfire, storm, or city",
    )
    if topbar_search:
        st.session_state["atlas_ops_location"] = topbar_search

    location_query = st.session_state.get("atlas_ops_location", get_default_location_query())

    render_page_hero(
        "Hazard layer",
        "Risk Intelligence",
        "Flood, wildfire, heatwave, and storm scoring driven by live forecast, AQI, and station context.",
        subtitle="Operational risk scoring with transparent drivers",
    )

    with st.sidebar:
        st.header("Risk controls")
        history_days = st.slider("NOAA lookback", min_value=14, max_value=90, value=45, step=1)

    with st.spinner("Loading risk intelligence data..."):
        try:
            location, resolved_weather = resolve_location(location_query)
            weather = resolved_weather or fetch_current_weather(location["lat"], location["lon"])
            forecast_df = fetch_forecast(location["lat"], location["lon"])
            air_current, air_forecast = fetch_air_quality(location["lat"], location["lon"])
            try:
                noaa_result = fetch_noaa_station_history(location["lat"], location["lon"], days=history_days)
            except Exception:
                noaa_result = None
            history_df = noaa_result["history"] if noaa_result else None
            risk_profile = build_risk_profile(weather, forecast_df, air_current, history_df)
            risk_timeline = build_risk_timeline(forecast_df)
            render_info_banner(
                f"Risk scoring for {location['label']} is blending live weather, AQI, forecast progression, and any nearby NOAA ground observations."
            )
        except Exception as exc:
            st.warning(f"Risk Intelligence could not connect to the live stack: {exc}")
            st.info("Add valid API credentials in Settings or use coordinates for the target location.")
            return

    metric_cols = st.columns(5)
    for column, title in zip(metric_cols, ["Heatwave", "Flood", "Wildfire", "Storm", "Composite"]):
        with column:
            if title == "Composite":
                render_metric_card("Composite risk", f"{risk_profile['composite']:.0f}/100", str(risk_profile["composite_label"]))
            else:
                panel = risk_profile["panels"][title]
                render_metric_card(title, f"{panel['score']:.0f}/100", str(panel["label"]))

    render_section_intro(
        "Risk trajectory",
        "Short-range forecast data is converted into scenario-style risk scores so operators can see direction, not just the latest point.",
        eyebrow="Timeline",
    )
    if risk_timeline.empty:
        st.info("Forecast data is required to build the risk timeline.")
    else:
        st.plotly_chart(create_risk_timeline_figure(risk_timeline, title="Short-range risk timeline"), use_container_width=True)

    alert_col, aq_col = st.columns(2)
    with alert_col:
        render_section_intro(
            "Alert feed",
            "Every alert is rule-based and traceable to the current weather and forecast profile.",
            eyebrow="Alerts",
        )
        if risk_profile["alerts"]:
            for alert in risk_profile["alerts"]:
                render_feature_card("Triggered alert", alert)
        else:
            render_feature_card("No elevated alerts", "Current hazard rules are not flagging major operational concern.")
        if noaa_result and history_df is not None and not history_df.empty:
            st.plotly_chart(
                create_station_history_figure(history_df, title=f"{noaa_result['station']['name']} station history"),
                use_container_width=True,
            )

    with aq_col:
        render_section_intro(
            "AQI and forecast",
            "Air quality adds a public-health dimension to the broader hazard picture.",
            eyebrow="Health",
        )
        st.plotly_chart(create_forecast_figure(forecast_df, title=f"{location['label']} weather track"), use_container_width=True)
        if not air_forecast.empty:
            st.plotly_chart(create_air_quality_figure(air_forecast, title=f"{location['label']} AQI outlook"), use_container_width=True)


if __name__ == "__main__":
    main()
