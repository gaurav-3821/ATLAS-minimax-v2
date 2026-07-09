from __future__ import annotations

import html

import pandas as pd
import plotly.graph_objects as go
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


def _render_ai_narrative(title: str, brief: str, result: dict[str, object], variable_label: str, unit_label: str) -> None:
    """Render the AI copilot brief as a flowing narrative section with inline key metrics."""
    direction = str(result.get("direction", "flat"))
    projected = float(result.get("projected_change", 0.0))
    peak = float(result.get("peak_delta", 0.0))
    peak_month = str(result.get("peak_month", "n/a"))
    horizon = int(result.get("horizon", 24))
    latest_fc = float(result.get("latest_forecast", 0.0))
    conf_width = float(result.get("confidence_width", 0.0))
    recent = float(result.get("recent_change", 0.0))

    chips = [
        f"{direction} {projected:+.2f}",
        f"peak step {peak:+.2f}",
        f"{peak_month} seasonal high",
    ]
    if conf_width > 0.0:
        chips.append(f"band \u00b1{conf_width:.2f}")
    chip_html = "".join(f"<span class='atlas-chip cyan'>{html.escape(c)}</span>" for c in chips)

    lines = _clean_brief_lines(brief)
    paragraphs = []
    for line in lines:
        if line and "unavailable" not in line.lower():
            paragraphs.append(
                f'<p style="font-family: var(--atlas-font-body); font-size: 0.88rem; '
                f'color: var(--atlas-text-secondary); line-height: 1.75; margin: 0 0 0.5rem 0;">'
                f'{html.escape(line)}</p>'
            )
    narrative_html = "\n".join(paragraphs) if paragraphs else ""

    trend_color = "var(--atlas-error)" if projected > 0 else "var(--atlas-primary-fixed-dim)"
    recent_color = "var(--atlas-error)" if recent > 0 else "var(--atlas-primary-fixed-dim)"

    st.markdown(
        f"""
        <div class="glass-panel" style="padding: 1.5rem 1.75rem; margin-bottom: 1.5rem; border-top: 2px solid var(--atlas-primary-fixed-dim);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span class="material-symbols-outlined" style="color: var(--atlas-primary-fixed-dim); font-size: 1.25rem;">auto_awesome</span>
                    <span style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-primary-fixed-dim); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;">{html.escape(title)}</span>
                </div>
                <span style="font-family: var(--atlas-font-mono); font-size: 0.55rem; color: var(--atlas-muted); letter-spacing: 0.08em;">{html.escape(unit_label)}</span>
            </div>
            <div style="display: flex; gap: 0.4rem; margin-bottom: 1rem; flex-wrap: wrap;">{chip_html}</div>
            {narrative_html}
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--atlas-glass-border);">
                <div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.55rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.15rem;">Forecast end</div>
                    <div style="font-family: var(--atlas-font-heading); font-size: 1.2rem; font-weight: 700; color: var(--atlas-text);">{latest_fc:.2f}</div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted);">{html.escape(unit_label)}</div>
                </div>
                <div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.55rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.15rem;">Projected</div>
                    <div style="font-family: var(--atlas-font-heading); font-size: 1.2rem; font-weight: 700; color: {trend_color};">{projected:+.2f}</div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted);">{direction} over {horizon}mo</div>
                </div>
                <div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.55rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.15rem;">Recent shift</div>
                    <div style="font-family: var(--atlas-font-heading); font-size: 1.2rem; font-weight: 700; color: {recent_color};">{recent:+.2f}</div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted);">pre-forecast 30mo</div>
                </div>
                <div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.55rem; color: var(--atlas-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.15rem;">Confidence band</div>
                    <div style="font-family: var(--atlas-font-heading); font-size: 1.2rem; font-weight: 700; color: var(--atlas-primary-fixed-dim);">{conf_width:.2f}</div>
                    <div style="font-family: var(--atlas-font-mono); font-size: 0.6rem; color: var(--atlas-muted);">width at horizon</div>
                </div>
            </div>
        </div>
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

    has_ai = False
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
                st.session_state["ai_brief"] = ai_brief
                st.session_state["ai_generated"] = True
            except Exception as exc:
                st.session_state["ai_brief"] = f"AI briefing unavailable: {exc}"
                st.session_state["ai_generated"] = False

    if st.session_state.get("ai_generated") and st.session_state.get("ai_brief"):
        has_ai = True
        ai_brief = str(st.session_state["ai_brief"])
        _render_ai_narrative(
            f"Copilot analysis: {region_name} {variable_label}",
            ai_brief, result, variable_label, unit_label,
        )
        # Inline regenerate button
        if st.button(":material/refresh: Regenerate analysis", key="regen_ai", use_container_width=True):
            st.session_state.pop("ai_generated", None)
            st.session_state.pop("ai_brief", None)
            st.rerun()

    if not has_ai:
        metric_cols = st.columns(4)
        with metric_cols[0]:
            render_metric_card("Latest value", f"{diagnostics['latest']:.2f}", f"{region_name} regional mean")
        with metric_cols[1]:
            render_metric_card("Long-run mean", f"{diagnostics['mean']:.2f}", "Historical baseline from selected series")
        with metric_cols[2]:
            render_metric_card("Volatility", f"{diagnostics['volatility']:.2f}", "Standard deviation of observed series")
        with metric_cols[3]:
            render_metric_card("Projected change", f"{projected_change:+.2f}", f"{horizon}-month {result['direction']} move")

    forecast_tag = f" | AI: {projected_change:+.2f} over {horizon}mo" if has_ai else ""
    render_section_intro(
        "Prediction surface",
        f"The forecast line and confidence band show a {horizon}-month {result['direction']} move of {projected_change:+.2f} {unit_label}."
        + (" The AI analysis above contextualizes these numbers against recent momentum and seasonal patterns." if has_ai else ""),
        eyebrow="Forecast",
    )
    fig_pred = create_prediction_figure(
        observed_df=observed_df,
        forecast_df=forecast_df,
        title=f"{region_name} {variable_label} outlook{forecast_tag}",
        value_column="value",
        y_label=unit_label,
    )
    if has_ai:
        fc_last = forecast_df.iloc[-1]
        fc_first = forecast_df.iloc[0]
        fig_pred.add_annotation(
            x=fc_last["time"], y=fc_last["forecast"],
            text=f"End: {float(fc_last['forecast']):.2f} {unit_label}",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="var(--atlas-primary-fixed-dim)",
            font=dict(size=10, color="var(--atlas-primary-fixed-dim)"),
            bgcolor="rgba(0,0,0,0.6)", bordercolor="var(--atlas-glass-border)", borderwidth=1,
            ax=40, ay=-30,
        )
        fig_pred.add_annotation(
            x=fc_first["time"], y=float(fc_first["forecast"]),
            text=f"Start: {float(fc_first['forecast']):.2f}",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="var(--atlas-muted)",
            font=dict(size=10, color="var(--atlas-muted)"),
            bgcolor="rgba(0,0,0,0.6)", bordercolor="var(--atlas-glass-border)", borderwidth=1,
            ax=-40, ay=30,
        )
        fig_pred.add_hline(
            y=float(fc_last["forecast"]),
            line_dash="dot", line_color="var(--atlas-primary-fixed-dim)", line_width=1,
            annotation_text=f"{float(fc_last['forecast']):.2f}", annotation_position="right",
        )
    st.plotly_chart(fig_pred, use_container_width=True)

    top_left, top_right = st.columns(2)
    with top_left:
        render_section_intro(
            "Forecast change bars",
            f"Bars show each forecast step change. The strongest modeled step is {float(result['peak_delta']):+.2f} {unit_label}.",
            eyebrow="Momentum",
        )
        fig_delta = create_forecast_delta_figure(
            forecast_df,
            title=f"Forecast momentum | peak {float(result['peak_delta']):+.2f} {unit_label}",
            value_label=f"{variable_label} step change ({unit_label})",
        )
        if has_ai:
            frame = forecast_df.copy()
            val_col = "temperature_c" if "temperature_c" in frame.columns else "forecast"
            frame["delta"] = frame[val_col].diff().fillna(0.0)
            peak_idx = int(frame["delta"].abs().idxmax()) if not frame.empty else -1
            if peak_idx >= 0:
                peak_time = frame.iloc[peak_idx]["time"]
                peak_delta_val = float(frame.iloc[peak_idx]["delta"])
                fig_delta.add_annotation(
                    x=peak_time, y=peak_delta_val,
                    text=f"Peak: {peak_delta_val:+.2f}",
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="var(--atlas-primary-fixed-dim)",
                    font=dict(size=10, color="var(--atlas-primary-fixed-dim)"),
                    bgcolor="rgba(0,0,0,0.6)", bordercolor="var(--atlas-glass-border)", borderwidth=1,
                    ax=0, ay=-40,
                )
        st.plotly_chart(fig_delta, use_container_width=True)
    with top_right:
        render_section_intro(
            "Seasonal pattern",
            f"Monthly averages explain the seasonal signal carried into the forecast. The observed high is around {result['peak_month']}.",
            eyebrow="Seasonality",
        )
        fig_season = create_seasonality_bar_figure(
            observed_df,
            title=f"Observed seasonal pattern | high {result['peak_month']}",
            value_column="value",
            y_label=unit_label,
        )
        if has_ai and result["peak_month"] != "n/a":
            monthly_vals = observed_df.copy()
            monthly_vals["time"] = pd.to_datetime(monthly_vals["time"])
            monthly_vals["month_label"] = monthly_vals["time"].dt.strftime("%b")
            monthly_avg = monthly_vals.groupby("month_label")["value"].mean()
            peak_val = float(monthly_avg.max())
            fig_season.add_annotation(
                x=result["peak_month"], y=peak_val,
                text=f"Peak: {peak_val:.2f}",
                showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=1.5, arrowcolor="var(--atlas-primary-fixed-dim)",
                font=dict(size=10, color="var(--atlas-primary-fixed-dim)"),
                bgcolor="rgba(0,0,0,0.6)", bordercolor="var(--atlas-glass-border)", borderwidth=1,
                ax=0, ay=-40,
            )
            fig_season.add_hline(
                y=peak_val, line_dash="dot", line_color="var(--atlas-primary-fixed-dim)", line_width=1,
                annotation_text=f"high {peak_val:.2f}", annotation_position="left",
            )
        st.plotly_chart(fig_season, use_container_width=True)

    lower_left, lower_right = st.columns((1.1, 0.9))
    with lower_left:
        render_section_intro(
            "Recent signal bars",
            f"Recent bars show the observed pre-forecast move of {float(result['recent_change']):+.2f} {unit_label}.",
            eyebrow="Observed",
        )
        fig_recent = create_anomaly_bar_figure(
            observed_df.tail(30),
            title=f"Recent observed values | {float(result['recent_change']):+.2f} {unit_label}",
            value_column="value",
            y_label=unit_label,
        )
        if has_ai:
            recent_tail = observed_df.tail(30)
            first_val = float(recent_tail["value"].iloc[0])
            last_val = float(recent_tail["value"].iloc[-1])
            mid_idx = len(recent_tail) // 2
            fig_recent.add_annotation(
                x=recent_tail.iloc[0]["time"], y=first_val,
                text=f"Start: {first_val:.2f}",
                showarrow=True, arrowhead=2, arrowsize=1, arrowcolor="var(--atlas-muted)",
                font=dict(size=9, color="var(--atlas-muted)"),
                bgcolor="rgba(0,0,0,0.6)", bordercolor="var(--atlas-glass-border)", borderwidth=1,
                ax=-30, ay=20,
            )
            fig_recent.add_annotation(
                x=recent_tail.iloc[-1]["time"], y=last_val,
                text=f"End: {last_val:.2f}",
                showarrow=True, arrowhead=2, arrowsize=1, arrowcolor="var(--atlas-primary-fixed-dim)",
                font=dict(size=9, color="var(--atlas-primary-fixed-dim)"),
                bgcolor="rgba(0,0,0,0.6)", bordercolor="var(--atlas-glass-border)", borderwidth=1,
                ax=30, ay=-20,
            )
        st.plotly_chart(fig_recent, use_container_width=True)
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
