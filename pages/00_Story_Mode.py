from __future__ import annotations

import html

import streamlit as st

from ui_ux.chart_factory import (
    create_story_bar,
    create_story_comparison,
    create_story_heatmap,
    create_story_scenarios,
    create_story_timeline,
)
from ui_ux.style import render_app_shell, render_page_hero
from utils.story_content import STORY_MODE_CONFIG


st.set_page_config(page_title="ATLAS | Story Mode", page_icon=":material/play_circle:", layout="wide")


def _render_step_chips(steps: list[dict[str, object]], active_index: int) -> None:
    columns = st.columns(len(steps))
    for index, (column, step) in enumerate(zip(columns, steps)):
        active_class = "active" if index == active_index else ""
        title = html.escape(str(step["title"]))
        component = html.escape(str(step["visual_panel"]["component"]))
        with column:
            st.markdown(
                f"""
                <div class="atlas-step-chip {active_class}">
                    <strong>{index + 1}. {title}</strong>
                    <span>{component}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_visual(step: dict[str, object]) -> None:
    source = STORY_MODE_CONFIG["data_sources"]
    component = str(step["visual_panel"]["component"])
    if component == "heatmap + line_chart":
        gt = source["global_temperature"]
        map_col, chart_col = st.columns((1.05, 0.95))
        with map_col:
            st.plotly_chart(create_story_heatmap(), use_container_width=True)
        with chart_col:
            st.plotly_chart(
                create_story_timeline(gt["years"], gt["temperature_anomaly_c"], "Global Temperature Anomaly"),
                use_container_width=True,
            )
        return
    if component == "comparison_chart":
        aa = source["arctic_amplification"]
        st.plotly_chart(
            create_story_comparison(
                aa["years"],
                {"Global": aa["anomaly_c"]["Global"], "Arctic": aa["anomaly_c"]["Arctic"]},
                {"Global": "#00E5FF", "Arctic": "#FF5C8A"},
                "Global vs Arctic Warming",
            ),
            use_container_width=True,
        )
        return
    if component == "line_chart":
        gt = source["global_temperature"]
        st.plotly_chart(
            create_story_timeline(gt["years"], gt["temperature_anomaly_c"], "Global Temperature Anomaly"),
            use_container_width=True,
        )
        return
    if component == "bar_chart":
        st.plotly_chart(
            create_story_bar(source["extreme_events"]["events"], "Extreme Weather Events Over Time"),
            use_container_width=True,
        )
        return
    if component == "scenario_projection_chart":
        fp = source["future_projection"]
        scenario_colors = {"low_emissions": "#6EFF9A", "medium_emissions": "#FFD84D", "high_emissions": "#FF5C8A"}
        st.plotly_chart(
            create_story_scenarios(fp["scenarios"], scenario_colors, "Future Warming Scenarios"),
            use_container_width=True,
        )
        return
    st.warning("Visualization not implemented yet")


def main() -> None:
    render_app_shell(
        "Story Mode",
        "Interactive climate narrative with stable scene navigation, visible narrative text, and reliable visual rendering.",
        search_placeholder="Search story chapters",
    )
    render_page_hero(
        "Interactive narrative",
        "ATLAS Story Mode",
        "A guided climate story built with reliable Streamlit rendering, chapter chips, and fallback demo visuals.",
        subtitle="Narrative text, AI insight, and visual scenes that always render",
    )

    story_steps = STORY_MODE_CONFIG["story_steps"]

    if "step_index" not in st.session_state:
        st.session_state.step_index = 0

    step_index = min(st.session_state.step_index, len(story_steps) - 1)
    step = story_steps[step_index]

    control_cols = st.columns((1, 1, 4))
    with control_cols[0]:
        if st.button("Previous", use_container_width=True, disabled=step_index == 0):
            st.session_state.step_index -= 1
            st.rerun()
    with control_cols[1]:
        if st.button("Next", use_container_width=True, disabled=step_index == len(story_steps) - 1):
            st.session_state.step_index += 1
            st.rerun()
    with control_cols[2]:
        st.progress((step_index + 1) / len(story_steps), text=f"Chapter {step_index + 1} of {len(story_steps)}")

    _render_step_chips(story_steps, step_index)

    st.markdown("### Visualization")
    _render_visual(step)

    st.markdown("### " + str(step["title"]))
    st.write(step["narrative_panel"]["text"])
    st.info("AI Insight: " + str(step["narrative_panel"].get("ai_insight", "No AI insight available for this scene.")))


if __name__ == "__main__":
    main()
