from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from utils.ai_copilot import generate_prediction_brief, get_openrouter_api_key, validate_openrouter_key
from ui_ux.chart_factory import (
    create_anomaly_bar_figure,
    create_forecast_delta_figure,
    create_prediction_figure,
    create_seasonality_bar_figure,
)
from utils.data_loader import (
    REGION_BOUNDS,
    detect_axes,
    format_analysis_label,
    format_variable_units,
    get_active_dataset,
    is_anomaly_array,
    spatial_mean_series,
    to_display_array,
)
from utils.prediction_engine import build_forecast_frame, compute_model_diagnostics, parse_natural_language_query
from utils.real_climate import get_real_temperature_array
from ui_ux.style import render_app_shell, render_feature_card, render_info_banner, render_metric_card, render_page_hero, render_section_intro


st.set_page_config(page_title="ATLAS | AI Predictions", page_icon=":material/auto_graph:", layout="wide")


def _clean_brief_lines(brief: str) -> list[str]:
    lines: list[str] = []
    for raw_line in brief.replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        line = line.lstrip("-*0123456789. ").replace("**", "")
        if line:
            lines.append(line)
    if lines:
        return lines[:4]
    return [brief.strip()] if brief.strip() else ["Forecast brief unavailable."]


def _forecast_results(observed_df: pd.DataFrame, forecast_df: pd.DataFrame, horizon: int) -> dict[str, object]:
    latest_value = float(observed_df["value"].iloc[-1]) if not observed_df.empty else 0.0
    latest_forecast = float(forecast_df["forecast"].iloc[-1]) if not forecast_df.empty else latest_value
    projected_change = latest_forecast - latest_value
    deltas = forecast_df["forecast"].diff().fillna(0.0) if not forecast_df.empty else pd.Series(dtype=float)
    peak_delta = float(deltas.iloc[deltas.abs().argmax()]) if not deltas.empty else 0.0
    recent_change = float(observed_df["value"].tail(30).iloc[-1] - observed_df["value"].tail(30).iloc[0]) if len(observed_df) >= 2 else 0.0
    confidence_width = float(forecast_df["upper"].iloc[-1] - forecast_df["lower"].iloc[-1]) if not forecast_df.empty else 0.0
    direction = "rising" if projected_change > 0 else "falling" if projected_change < 0 else "flat"

    seasonal = observed_df.copy()
    seasonal["time"] = pd.to_datetime(seasonal["time"])
    seasonal["month"] = seasonal["time"].dt.strftime("%b")
    seasonal["month_number"] = seasonal["time"].dt.month
    monthly = seasonal.groupby(["month_number", "month"], as_index=False)["value"].mean().sort_values("month_number")
    peak_month = str(monthly.loc[monthly["value"].idxmax(), "month"]) if not monthly.empty else "n/a"

    return {
        "latest_value": latest_value,
        "latest_forecast": latest_forecast,
        "projected_change": projected_change,
        "peak_delta": peak_delta,
        "recent_change": recent_change,
        "confidence_width": confidence_width,
        "direction": direction,
        "peak_month": peak_month,
        "horizon": horizon,
    }


def _render_copilot_card(title: str, brief: str, result: dict[str, object], variable_label: str, unit_label: str) -> None:
    chips = [
        f"{result['direction']} {float(result['projected_change']):+.2f}",
        f"peak step {float(result['peak_delta']):+.2f}",
        f"{result['peak_month']} seasonal high",
    ]
    chip_html = "".join(f"<span class='atlas-chip cyan'>{html.escape(chip)}</span>" for chip in chips)
    result_lines = [
        f"Line chart: {variable_label} is {result['direction']} by {float(result['projected_change']):+.2f} {unit_label} over {int(result['horizon'])} months.",
        f"Momentum bars: the strongest modeled step is {float(result['peak_delta']):+.2f} {unit_label}.",
        f"Recent bars: the observed pre-forecast move is {float(result['recent_change']):+.2f} {unit_label}.",
    ]
    live_lines = [
        line for line in _clean_brief_lines(brief)
        if 40 <= len(line) <= 220 and not line.endswith("-") and "unavailable" not in line.lower()
    ]
    if brief and live_lines:
        result_lines.append(f"Live note: {live_lines[0]}")
    items_html = "".join(f"<li>{html.escape(line)}</li>" for line in result_lines)
    st.markdown(
        f"""
        <article class="atlas-feature-card atlas-copilot-card" tabindex="0" role="article" aria-label="{html.escape(title)}">
            <div class="atlas-chip-row">{chip_html}</div>
            <h4>{html.escape(title)}</h4>
            <p class="atlas-copilot-lede">
                {html.escape(variable_label)} forecast ends at {float(result['latest_forecast']):.2f} {html.escape(unit_label)}
                after {int(result['horizon'])} months, with a {float(result['confidence_width']):.2f} band width.
            </p>
            <ul class="atlas-copilot-list">{items_html}</ul>
        </article>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    render_app_shell(
        "Predictions",
        "Model-assisted climate outlooks, anomaly detection, and natural-language signal steering.",
        search_placeholder="Ask about future warming, rainfall, wind, or pressure",
    )
    render_page_hero(
        "Model-assisted outlooks",
        "AI Predictions",
        "Trend and seasonal projections built from the historical climate workspace, with natural-language steering for faster exploration.",
        subtitle="Forecast surfaces for temperature, rainfall, wind, and pressure signals",
    )

    dataset, label = get_active_dataset()
    user_query = st.sidebar.text_area(
        "Natural-language query",
        value="Show the future warming outlook for the Arctic temperature anomaly.",
        height=120,
    )
    parsed = parse_natural_language_query(user_query)
    horizon = st.sidebar.slider("Forecast horizon (months)", min_value=6, max_value=60, value=24, step=6)
    variable = st.sidebar.selectbox(
        "Climate variable",
        ["t2m", "precipitation", "sea_level_pressure", "wind_speed"],
        index=["t2m", "precipitation", "sea_level_pressure", "wind_speed"].index(str(parsed["variable"])),
    )
    region_name = st.sidebar.selectbox(
        "Region",
        list(REGION_BOUNDS.keys()),
        index=list(REGION_BOUNDS.keys()).index(str(parsed["region"])),
    )
    anomaly_mode = st.sidebar.toggle("Forecast anomaly mode", value=bool(parsed["anomaly_mode"]))
    generate_live_brief = False
    if get_openrouter_api_key():
        key_status = validate_openrouter_key()
        if key_status is None:
            generate_live_brief = st.sidebar.button("Generate live Copilot note", use_container_width=True)
        else:
            st.sidebar.warning(key_status, icon=":material/key:")

    base_array = to_display_array(dataset[variable], variable)
    data_array, source_label = get_real_temperature_array(base_array) if variable == "t2m" else (base_array, label)
    variable_label = format_analysis_label(data_array, variable, anomaly_mode)
    unit_label = format_variable_units(data_array) or variable
    axes = detect_axes(data_array)
    series = spatial_mean_series(data_array, axes, region_name, anomaly_mode=anomaly_mode)
    observed_df = series.to_dataframe(name="value").reset_index().rename(columns={axes["time"]: "time"})
    forecast_df = build_forecast_frame(observed_df, time_column="time", value_column="value", horizon=horizon)
    diagnostics = compute_model_diagnostics(observed_df, "value")
    result = _forecast_results(observed_df, forecast_df, horizon)
    projected_change = float(result["projected_change"])

    render_info_banner(
        f"Parsed query -> {variable_label} over {region_name}. The {horizon}-month forecast is {result['direction']} with projected change {projected_change:+.2f} {unit_label}. Source: {source_label}."
    )
    if is_anomaly_array(data_array):
        render_info_banner(
            "Temperature uses NASA GISTEMP anomaly data directly. The anomaly toggle will not re-center it a second time."
        )

    if generate_live_brief:
        with st.spinner("Generating AI climate brief..."):
            try:
                result_context = (
                    f"{variable_label} over {region_name}; {horizon}-month direction: {result['direction']}; "
                    f"projected line-chart change: {projected_change:+.2f} {unit_label}; "
                    f"largest momentum bar: {float(result['peak_delta']):+.2f} {unit_label}; "
                    f"recent observed bar move: {float(result['recent_change']):+.2f} {unit_label}; "
                    f"seasonal high month: {result['peak_month']}."
                )
                ai_brief = generate_prediction_brief(
                    user_query,
                    region_name,
                    variable,
                    observed_df.tail(120),
                    forecast_df,
                    result_context,
                )
            except Exception as exc:
                ai_brief = f"AI briefing unavailable: {exc}"
        _render_copilot_card("ATLAS Copilot", ai_brief, result, variable_label, unit_label)
    else:
        _render_copilot_card("ATLAS Copilot", "", result, variable_label, unit_label)

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric_card("Latest value", f"{diagnostics['latest']:.2f}", f"{region_name} regional mean")
    with metric_cols[1]:
        render_metric_card("Long-run mean", f"{diagnostics['mean']:.2f}", "Historical baseline from selected series")
    with metric_cols[2]:
        render_metric_card("Volatility", f"{diagnostics['volatility']:.2f}", "Standard deviation of observed series")
    with metric_cols[3]:
        render_metric_card("Projected change", f"{projected_change:+.2f}", f"{horizon}-month {result['direction']} move")

    render_section_intro(
        "Prediction surface",
        f"The forecast line, confidence band, and result cards all reference the same {horizon}-month {result['direction']} move of {projected_change:+.2f} {unit_label}.",
        eyebrow="Forecast",
    )
    st.plotly_chart(
        create_prediction_figure(
            observed_df=observed_df,
            forecast_df=forecast_df,
            title=f"{region_name} {variable_label} outlook | {projected_change:+.2f} {unit_label}",
            value_column="value",
            y_label=unit_label,
        ),
        use_container_width=True,
    )

    top_left, top_right = st.columns(2)
    with top_left:
        render_section_intro(
            "Forecast change bars",
            f"Bars show each forecast step change. The strongest modeled step is {float(result['peak_delta']):+.2f} {unit_label}.",
            eyebrow="Momentum",
        )
        st.plotly_chart(
            create_forecast_delta_figure(
                forecast_df,
                title=f"Forecast momentum | peak {float(result['peak_delta']):+.2f} {unit_label}",
                value_label=f"{variable_label} step change ({unit_label})",
            ),
            use_container_width=True,
        )
    with top_right:
        render_section_intro(
            "Seasonal pattern",
            f"Monthly averages explain the seasonal signal carried into the forecast. The observed high is around {result['peak_month']}.",
            eyebrow="Seasonality",
        )
        st.plotly_chart(
            create_seasonality_bar_figure(
                observed_df,
                title=f"Observed seasonal pattern | high {result['peak_month']}",
                value_column="value",
                y_label=unit_label,
            ),
            use_container_width=True,
        )

    lower_left, lower_right = st.columns((1.1, 0.9))
    with lower_left:
        render_section_intro(
            "Recent signal bars",
            f"Recent bars show the observed pre-forecast move of {float(result['recent_change']):+.2f} {unit_label}.",
            eyebrow="Observed",
        )
        st.plotly_chart(
            create_anomaly_bar_figure(
                observed_df.tail(30),
                title=f"Recent observed values | {float(result['recent_change']):+.2f} {unit_label}",
                value_column="value",
                y_label=unit_label,
            ),
            use_container_width=True,
        )
        render_section_intro(
            "Natural-language query",
            "The parser maps plain language onto the available historical variables and regions so teams can move faster.",
            eyebrow="Query",
        )
        st.markdown(
            f"""
            - **Query:** *{user_query}*
            - **Variable:** `{parsed['variable']}`
            - **Region:** `{parsed['region']}`
            - **Anomaly Mode:** `{parsed['anomaly_mode']}`
            """
        )
    with lower_right:
        render_section_intro(
            "Model notes",
            "This release uses an interpretable baseline model instead of a black-box service so teams can trust what changed and why.",
            eyebrow="Model",
        )
        render_feature_card("Forecast model", "Linear trend plus month-of-year seasonal adjustment with widening confidence bounds.")
        render_feature_card("Anomaly handling", "NASA GISTEMP temperature is already an anomaly series; other fields are centered only when anomaly mode is enabled.")
        render_feature_card("Product fit", "Fast enough for interactive work, transparent enough for research handoff.")


if __name__ == "__main__":
    main()
