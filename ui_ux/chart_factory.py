from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go


FONT_FAMILY = "'Geist', sans-serif"
PAPER_BG = "rgba(0,0,0,0)"
PLOT_BG = "rgba(30,32,36,0.85)"
GRID_COLOR = "rgba(255,255,255,0.08)"
TEXT_COLOR = "#e2e2e8"
MUTED_COLOR = "#b9cacb"
CYAN = "#00dbe7"
YELLOW = "#ffb950"
PINK = "#FF5C8A"
GREEN = "#6EFF9A"
SLATE = "#94A3B8"
CRIMSON = "#FF5C8A"

GEO_COASTLINE = "rgba(255,255,255,0.55)"
GEO_COUNTRY = "rgba(255,255,255,0.22)"
GEO_LAND = "rgba(32,42,65,0.62)"
GEO_OCEAN = "rgba(7,11,22,0.88)"
GEO_GRID = "rgba(255,255,255,0.10)"
GLOBE_BASE_DARK = "#0c0e12"
GLOBE_BASE_LIGHT = "#cbd5e1"


def set_chart_theme(dark: bool = True) -> None:
    global PLOT_BG, GRID_COLOR, TEXT_COLOR, MUTED_COLOR
    global GEO_COASTLINE, GEO_COUNTRY, GEO_LAND, GEO_OCEAN, GEO_GRID
    global GLOBE_BASE_DARK, GLOBE_BASE_LIGHT
    if dark:
        PLOT_BG = "rgba(30,32,36,0.85)"
        GRID_COLOR = "rgba(255,255,255,0.08)"
        TEXT_COLOR = "#e2e2e8"
        MUTED_COLOR = "#b9cacb"
        GEO_COASTLINE = "rgba(255,255,255,0.55)"
        GEO_COUNTRY = "rgba(255,255,255,0.22)"
        GEO_LAND = "rgba(32,42,65,0.62)"
        GEO_OCEAN = "rgba(7,11,22,0.88)"
        GEO_GRID = "rgba(255,255,255,0.10)"
        GLOBE_BASE_DARK = "#0c0e12"
        GLOBE_BASE_LIGHT = "#cbd5e1"
    else:
        PLOT_BG = "rgba(241,245,249,0.95)"
        GRID_COLOR = "rgba(0,0,0,0.08)"
        TEXT_COLOR = "#0f172a"
        MUTED_COLOR = "#64748b"
        GEO_COASTLINE = "rgba(0,0,0,0.35)"
        GEO_COUNTRY = "rgba(0,0,0,0.15)"
        GEO_LAND = "rgba(210,225,235,0.85)"
        GEO_OCEAN = "rgba(190,212,230,0.55)"
        GEO_GRID = "rgba(0,0,0,0.08)"
        GLOBE_BASE_DARK = "#cbd5e1"
        GLOBE_BASE_LIGHT = "#cbd5e1"


def _downsample_grid(
    lon_values: np.ndarray,
    lat_values: np.ndarray,
    z_values: np.ndarray,
    *,
    max_lat: int,
    max_lon: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    lat_step = max(1, int(np.ceil(len(lat_values) / max_lat)))
    lon_step = max(1, int(np.ceil(len(lon_values) / max_lon)))
    return lon_values[::lon_step], lat_values[::lat_step], z_values[::lat_step, ::lon_step]


def _apply_chart_style(
    figure: go.Figure,
    *,
    title: str,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
    show_legend: bool = True,
) -> go.Figure:
    r_margin = 60 if "yaxis2" in figure.layout else 15
    figure.update_layout(
        title=title,
        margin=dict(l=10, r=r_margin, t=56, b=12),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        title_font=dict(family="Space Grotesk, sans-serif", size=18, color=TEXT_COLOR),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0.0,
            bgcolor="rgba(11,15,26,0.55)",
            bordercolor="rgba(255,255,255,0.06)",
            borderwidth=1,
            font=dict(color=TEXT_COLOR),
        ),
        showlegend=show_legend,
        transition=dict(duration=260, easing="cubic-in-out"),
    )
    if xaxis_title is not None:
        figure.update_xaxes(
            title=xaxis_title,
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=False,
            color=TEXT_COLOR,
            title_font=dict(color=MUTED_COLOR),
        )
    if yaxis_title is not None:
        figure.update_layout(
            yaxis=dict(
                title=yaxis_title,
                showgrid=True,
                gridcolor=GRID_COLOR,
                zeroline=False,
                color=TEXT_COLOR,
                title_font=dict(color=MUTED_COLOR),
            )
        )
    return figure


def create_heatmap(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    figure = go.Figure(
        data=[
            go.Heatmap(
                z=map_slice.values,
                x=map_slice[lon_axis].values,
                y=map_slice[lat_axis].values,
                colorscale=colorscale,
                zsmooth="best",
                colorbar=dict(title=dict(text=colorbar_title, font=dict(color=TEXT_COLOR)), tickfont=dict(color=TEXT_COLOR)),
                hovertemplate="Lon %{x:.1f}<br>Lat %{y:.1f}<br>Value %{z:.2f}<extra></extra>",
            )
        ]
    )
    return _apply_chart_style(
        figure,
        title=title,
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        show_legend=False,
    )


def create_spatial_map(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
    projection: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    lon_values = np.asarray(map_slice[lon_axis].values, dtype=float)
    lon_values = np.where(lon_values > 180.0, lon_values - 360.0, lon_values)
    lat_values = np.asarray(map_slice[lat_axis].values, dtype=float)
    z_values = np.asarray(map_slice.values, dtype=float)
    lon_values, lat_values, z_values = _downsample_grid(lon_values, lat_values, z_values, max_lat=72, max_lon=144)
    lon_mesh, lat_mesh = np.meshgrid(lon_values, lat_values)
    marker_size = 6 if len(lat_values) <= 36 else 4
    projection_map = {
        "Analyst contour": "natural earth",
        "Dense field": "equirectangular",
        "Regional focus": "winkel tripel",
        "Comparison delta": "natural earth",
        "Projection map": "natural earth",
        "Orbital map": "orthographic",
    }
    figure = go.Figure(
        data=[
            go.Scattergeo(
                lon=lon_mesh.ravel(),
                lat=lat_mesh.ravel(),
                mode="markers",
                marker=dict(
                    size=marker_size,
                    symbol="square",
                    opacity=0.9,
                    color=z_values.ravel(),
                    colorscale=colorscale,
                    line=dict(width=0),
                    colorbar=dict(title=dict(text=colorbar_title, font=dict(color=TEXT_COLOR)), tickfont=dict(color=TEXT_COLOR)),
                ),
                customdata=np.column_stack((lat_mesh.ravel(), lon_mesh.ravel(), z_values.ravel())),
                hovertemplate="Lat %{customdata[0]:.1f}<br>Lon %{customdata[1]:.1f}<br>Value %{customdata[2]:.2f}<extra></extra>",
                showlegend=False,
            )
        ]
    )
    subtitle = f"{title} - {projection} view" if projection else title
    figure.update_layout(
        title=subtitle,
        margin=dict(l=10, r=10, t=56, b=12),
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
            geo=dict(
                projection_type=projection_map.get(projection, "natural earth"),
                resolution=50,
                showframe=False,
                showcoastlines=True,
                coastlinecolor=GEO_COASTLINE,
                coastlinewidth=1.1,
                showcountries=True,
                countrycolor=GEO_COUNTRY,
                showland=True,
                landcolor=GEO_LAND,
                showocean=True,
                oceancolor=GEO_OCEAN,
                lataxis=dict(showgrid=True, gridcolor=GEO_GRID),
                lonaxis=dict(showgrid=True, gridcolor=GEO_GRID),
                bgcolor="rgba(0,0,0,0)",
            ),
    )
    return figure


def create_time_series(
    series_df: pd.DataFrame,
    value_column: str,
    trend_df: pd.DataFrame,
    anomaly_mask,
    title: str,
    y_label: str,
) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=series_df["time"],
            y=series_df[value_column],
            mode="lines+markers",
            name="Observed",
            line=dict(color=CYAN, width=2.6),
            marker=dict(size=4.5, color=CYAN),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=trend_df["time"],
            y=trend_df["trend"],
            mode="lines",
            name="Trend",
            line=dict(color=YELLOW, width=2.2, dash="dash"),
            line_shape="spline",
        )
    )
    if anomaly_mask is not None and np.any(anomaly_mask):
        anomaly_df = series_df.loc[anomaly_mask]
        figure.add_trace(
            go.Scatter(
                x=anomaly_df["time"],
                y=anomaly_df[value_column],
                mode="markers",
                name="Anomalies",
                marker=dict(color=PINK, size=8, symbol="diamond"),
            )
        )
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title=y_label)


def create_globe(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
    marker_size: int = 5,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    lon_values = np.asarray(map_slice[lon_axis].values, dtype=float)
    lat_values = np.asarray(map_slice[lat_axis].values, dtype=float)
    overlay_values = np.asarray(map_slice.values, dtype=float)
    lon_values, lat_values, overlay_values = _downsample_grid(lon_values, lat_values, overlay_values, max_lat=48, max_lon=96)
    lon_radians = np.deg2rad(lon_values)
    lat_radians = np.deg2rad(lat_values)
    lon_mesh, lat_mesh = np.meshgrid(lon_radians, lat_radians)

    radius = 0.985
    spread = np.nanmax(overlay_values) - np.nanmin(overlay_values)
    if not np.isfinite(spread) or spread == 0.0:
        normalized = np.zeros_like(overlay_values)
    else:
        normalized = (overlay_values - np.nanmean(overlay_values)) / spread
    overlay_radius = 1.0 + normalized * 0.06

    x = overlay_radius * np.cos(lat_mesh) * np.cos(lon_mesh)
    y = overlay_radius * np.cos(lat_mesh) * np.sin(lon_mesh)
    z = overlay_radius * np.sin(lat_mesh)
    base_x = radius * np.cos(lat_mesh) * np.cos(lon_mesh)
    base_y = radius * np.cos(lat_mesh) * np.sin(lon_mesh)
    base_z = radius * np.sin(lat_mesh)
    customdata = np.dstack((np.rad2deg(lat_mesh), np.rad2deg(lon_mesh)))

    figure = go.Figure()
    figure.add_surface(
        x=base_x,
        y=base_y,
        z=base_z,
        surfacecolor=np.ones_like(overlay_values),
        colorscale=[[0.0, GLOBE_BASE_DARK], [1.0, GLOBE_BASE_LIGHT]],
        showscale=False,
        hoverinfo="skip",
        opacity=0.82,
        lighting=dict(ambient=0.9, diffuse=0.5, roughness=1.0, specular=0.02),
    )
    figure.add_surface(
        x=x,
        y=y,
        z=z,
        surfacecolor=overlay_values,
        colorscale=colorscale,
        colorbar=dict(title=dict(text=colorbar_title, font=dict(color=TEXT_COLOR)), tickfont=dict(color=TEXT_COLOR)),
        customdata=customdata,
        showscale=True,
        hovertemplate="Lat %{customdata[0]:.1f}<br>Lon %{customdata[1]:.1f}<br>Value %{surfacecolor:.2f}<extra></extra>",
        lighting=dict(ambient=0.75, diffuse=0.85, roughness=0.85, specular=0.08),
        opacity=0.97,
    )
    figure.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=56, b=12),
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="rgba(0,0,0,0)",
            aspectmode="data",
            camera=dict(eye=dict(x=1.7, y=1.32, z=0.88)),
        ),
    )
    return figure


def create_latitude_profile(
    map_slice,
    axes: dict[str, str | None],
    title: str,
    x_label: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    profile = map_slice.mean(dim=lon_axis)

    figure = go.Figure(
        data=[
            go.Scatter(
                x=profile.values,
                y=profile[lat_axis].values,
                mode="lines",
                line=dict(color=GREEN, width=3),
                fill="tozerox",
                fillcolor="rgba(110,255,154,0.12)",
                hovertemplate=f"{x_label} %{{x:.2f}}<br>Lat %{{y:.1f}}<extra></extra>",
            )
        ]
    )
    return _apply_chart_style(
        figure,
        title=title,
        xaxis_title=x_label,
        yaxis_title="Latitude",
        show_legend=False,
    )


def create_animated_heatmap(
    annual_data,
    axes: dict[str, str | None],
    title: str,
    colorscale: str,
    colorbar_title: str,
) -> go.Figure:
    lat_axis = axes["lat"]
    lon_axis = axes["lon"]
    years = annual_data["year"].values.tolist()
    first = annual_data.isel(year=0)

    figure = go.Figure(
        data=[
            go.Heatmap(
                z=first.values,
                x=first[lon_axis].values,
                y=first[lat_axis].values,
                colorscale=colorscale,
                colorbar=dict(title=dict(text=colorbar_title, font=dict(color=TEXT_COLOR)), tickfont=dict(color=TEXT_COLOR)),
                hovertemplate="Lon %{x:.1f}<br>Lat %{y:.1f}<br>Value %{z:.2f}<extra></extra>",
            )
        ],
        frames=[
            go.Frame(
                data=[
                    go.Heatmap(
                        z=annual_data.sel(year=year).values,
                        x=annual_data[lon_axis].values,
                        y=annual_data[lat_axis].values,
                        colorscale=colorscale,
                    )
                ],
                name=str(year),
            )
            for year in years
        ],
    )
    figure.update_layout(
        title=title,
        margin=dict(l=10, r=10, t=56, b=12),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 1.0,
                "y": 1.14,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 240, "redraw": True}, "fromcurrent": True}],
                    }
                ],
            }
        ],
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Year: "},
                "steps": [
                    {
                        "label": str(year),
                        "method": "animate",
                        "args": [[str(year)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}],
                    }
                    for year in years
                ],
            }
        ],
    )
    figure.update_xaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)
    figure.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, zeroline=False)
    return figure


def create_forecast_figure(forecast_df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=forecast_df["time"],
            y=forecast_df["temperature_c"],
            mode="lines+markers",
            name="Temperature",
            line=dict(color=CYAN, width=2.8),
            marker=dict(size=4),
        )
    )
    figure.add_trace(
        go.Bar(
            x=forecast_df["time"],
            y=forecast_df["precip_probability_pct"],
            name="Precipitation chance",
            marker_color="rgba(255,216,77,0.45)",
            yaxis="y2",
            opacity=0.9,
        )
    )
    figure.update_layout(
        yaxis2=dict(
            title="Precipitation chance (%)",
            overlaying="y",
            side="right",
            range=[0, 100],
            showgrid=False,
            color=TEXT_COLOR,
        )
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title="Temperature (deg C)")


def create_air_quality_figure(aq_df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=aq_df["time"],
            y=aq_df["pm2_5"],
            mode="lines",
            name="PM2.5",
            line=dict(color=PINK, width=2.6),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=aq_df["time"],
            y=aq_df["pm10"],
            mode="lines",
            name="PM10",
            line=dict(color=YELLOW, width=2.4),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=aq_df["time"],
            y=aq_df["aqi"],
            mode="lines",
            name="AQI band",
            line=dict(color=SLATE, width=2, dash="dash"),
            yaxis="y2",
        )
    )
    figure.update_layout(
        yaxis2=dict(
            title="AQI",
            overlaying="y",
            side="right",
            range=[0.5, 5.5],
            tickmode="array",
            tickvals=[1, 2, 3, 4, 5],
            showgrid=False,
            color=TEXT_COLOR,
        )
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title="Concentration (ug/m3)")


def create_station_history_figure(history_df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure()
    if "TMAX" in history_df:
        figure.add_trace(
            go.Scatter(
                x=history_df["date"],
                y=history_df["TMAX"],
                mode="lines",
                name="Max temp",
                line=dict(color=PINK, width=2.5),
            )
        )
    if "TMIN" in history_df:
        figure.add_trace(
            go.Scatter(
                x=history_df["date"],
                y=history_df["TMIN"],
                mode="lines",
                name="Min temp",
                line=dict(color=CYAN, width=2.3),
            )
        )
    if "PRCP" in history_df:
        figure.add_trace(
            go.Bar(
                x=history_df["date"],
                y=history_df["PRCP"],
                name="Precipitation",
                marker_color="rgba(110,255,154,0.36)",
                opacity=0.85,
                yaxis="y2",
            )
        )
    figure.update_layout(
        yaxis2=dict(
            title="Precipitation (mm)",
            overlaying="y",
            side="right",
            showgrid=False,
            color=TEXT_COLOR,
        )
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Date", yaxis_title="Temperature (deg C)")


def create_timeline_figure(series_df: pd.DataFrame, title: str, value_column: str, y_label: str, color: str = CYAN) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Scatter(
                x=series_df["time"],
                y=series_df[value_column],
                mode="lines",
                line=dict(color=color, width=2.7),
                line_shape="spline",
                fill="tozeroy",
                fillcolor="rgba(0,229,255,0.10)" if color == CYAN else "rgba(255,92,138,0.12)",
                name=y_label,
            )
        ]
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title=y_label, show_legend=False)


def create_prediction_figure(
    observed_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    title: str,
    value_column: str,
    y_label: str,
) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=observed_df["time"],
            y=observed_df[value_column],
            mode="lines",
            name="Observed",
            line=dict(color=CYAN, width=2.6),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=forecast_df["time"],
            y=forecast_df["forecast"],
            mode="lines",
            name="Forecast",
            line=dict(color=YELLOW, width=2.6),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=pd.concat([forecast_df["time"], forecast_df["time"][::-1]]),
            y=pd.concat([forecast_df["upper"], forecast_df["lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(255,216,77,0.16)",
            line=dict(color="rgba(255,216,77,0.0)"),
            hoverinfo="skip",
            showlegend=True,
            name="Confidence band",
        )
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title=y_label)


def create_anomaly_bar_figure(
    series_df: pd.DataFrame,
    title: str,
    value_column: str,
    y_label: str,
) -> go.Figure:
    values = series_df[value_column].astype(float)
    colors = [PINK if value >= 0 else CYAN for value in values]
    figure = go.Figure(
        data=[
            go.Bar(
                x=series_df["time"],
                y=values,
                marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.08)", width=1)),
                hovertemplate="Time %{x}<br>Value %{y:.2f}<extra></extra>",
            )
        ]
    )
    _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title=y_label, show_legend=False)
    figure.update_yaxes(zeroline=True, zerolinecolor="rgba(255,255,255,0.35)")
    return figure


def create_ranked_bar_figure(
    values: dict[str, float],
    title: str,
    x_label: str,
    *,
    diverging: bool = False,
) -> go.Figure:
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=True)
    labels = [item[0] for item in ordered]
    scores = [float(item[1]) for item in ordered]
    palette = [PINK, YELLOW, CYAN, GREEN, SLATE]
    if diverging:
        colors = [PINK if score >= 0 else CYAN for score in scores]
    else:
        colors = [palette[index % len(palette)] for index in range(len(scores))]

    figure = go.Figure(
        data=[
            go.Bar(
                x=scores,
                y=labels,
                orientation="h",
                marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.08)", width=1)),
                text=[f"{score:.1f}" for score in scores],
                textposition="outside",
                hovertemplate="%{y}: %{x:.2f}<extra></extra>",
            )
        ]
    )
    _apply_chart_style(figure, title=title, xaxis_title=x_label, yaxis_title=None, show_legend=False)
    figure.update_yaxes(showgrid=False, autorange="reversed", color=TEXT_COLOR)
    if diverging:
        figure.update_xaxes(zeroline=True, zerolinecolor="rgba(255,255,255,0.35)")
    return figure


def create_gauge_figure(
    value: float,
    title: str,
    *,
    suffix: str = "",
    max_value: float = 100.0,
) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Indicator(
                mode="gauge+number",
                value=float(value),
                number={"suffix": suffix, "font": {"color": TEXT_COLOR, "size": 34}},
                gauge={
                    "axis": {"range": [0, max_value], "tickcolor": MUTED_COLOR},
                    "bar": {"color": PINK},
                    "bgcolor": PLOT_BG,
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, max_value * 0.35], "color": "rgba(0,229,255,0.18)"},
                        {"range": [max_value * 0.35, max_value * 0.7], "color": "rgba(255,216,77,0.20)"},
                        {"range": [max_value * 0.7, max_value], "color": "rgba(255,92,138,0.22)"},
                    ],
                    "threshold": {"line": {"color": TEXT_COLOR, "width": 4}, "value": float(value)},
                },
            )
        ]
    )
    figure.update_layout(
        title=title,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        margin=dict(l=24, r=24, t=56, b=18),
    )
    return figure


def create_donut_figure(values: dict[str, float], title: str) -> go.Figure:
    labels = list(values.keys())
    scores = [max(float(score), 0.01) for score in values.values()]
    palette = [PINK, YELLOW, CYAN, GREEN, SLATE]
    figure = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=scores,
                hole=0.62,
                marker=dict(colors=palette[: len(labels)], line=dict(color=PLOT_BG, width=3)),
                textinfo="label+percent",
                textfont=dict(color=TEXT_COLOR),
                sort=False,
            )
        ]
    )
    figure.update_layout(
        title=title,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        margin=dict(l=18, r=18, t=56, b=18),
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, x=0.0),
    )
    return figure


def create_seasonality_bar_figure(
    series_df: pd.DataFrame,
    title: str,
    value_column: str,
    y_label: str,
) -> go.Figure:
    seasonal = series_df.copy()
    seasonal["time"] = pd.to_datetime(seasonal["time"])
    seasonal["month_number"] = seasonal["time"].dt.month
    seasonal["month_label"] = seasonal["time"].dt.strftime("%b")
    grouped = (
        seasonal.groupby(["month_number", "month_label"], as_index=False)[value_column]
        .mean()
        .sort_values("month_number")
    )
    colors = [CYAN, GREEN, YELLOW, PINK] * 3
    figure = go.Figure(
        data=[
            go.Bar(
                x=grouped["month_label"],
                y=grouped[value_column],
                marker=dict(color=colors[: len(grouped)], line=dict(color="rgba(255,255,255,0.08)", width=1)),
                hovertemplate="%{x}: %{y:.2f}<extra></extra>",
            )
        ]
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Month", yaxis_title=y_label, show_legend=False)


def create_forecast_delta_figure(forecast_df: pd.DataFrame, title: str) -> go.Figure:
    frame = forecast_df.copy()
    value_column = "temperature_c" if "temperature_c" in frame.columns else "forecast"
    frame["temp_delta_c"] = frame[value_column].diff().fillna(0.0)
    colors = [PINK if value >= 0 else CYAN for value in frame["temp_delta_c"]]
    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            x=frame["time"],
            y=frame["temp_delta_c"],
            name="Temperature shift",
            marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.08)", width=1)),
            hovertemplate="Time %{x}<br>Temp shift %{y:.2f} C<extra></extra>",
        )
    )
    if "precip_probability_pct" in frame.columns:
        figure.add_trace(
            go.Scatter(
                x=frame["time"],
                y=frame["precip_probability_pct"],
                mode="lines",
                name="Precipitation chance",
                line=dict(color=YELLOW, width=2.2),
                line_shape="spline",
                yaxis="y2",
                hovertemplate="Time %{x}<br>Precip %{y:.0f}%<extra></extra>",
            )
        )
        figure.update_layout(
            yaxis2=dict(
                title="Precipitation chance (%)",
                overlaying="y",
                side="right",
                range=[0, 100],
                showgrid=False,
                color=TEXT_COLOR,
            )
        )
    _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title="Temperature shift (C)")
    figure.update_layout(yaxis=dict(zeroline=True, zerolinecolor="rgba(255,255,255,0.35)"))
    return figure


def create_risk_radar(risk_scores: dict[str, float], title: str) -> go.Figure:
    categories = list(risk_scores.keys())
    values = list(risk_scores.values())
    if categories:
        categories.append(categories[0])
        values.append(values[0])
    figure = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                line=dict(color=PINK, width=2.5),
                fillcolor="rgba(255,92,138,0.18)",
                name="Risk score",
            )
        ]
    )
    figure.update_layout(
        title=title,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAMILY, color=TEXT_COLOR),
        polar=dict(
            bgcolor=PLOT_BG,
            radialaxis=dict(range=[0, 100], gridcolor=GRID_COLOR, color=TEXT_COLOR),
            angularaxis=dict(gridcolor=GRID_COLOR, color=TEXT_COLOR),
        ),
        margin=dict(l=18, r=18, t=56, b=18),
    )
    return figure


def create_live_signal_figure(forecast_df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=forecast_df["time"],
            y=forecast_df["temperature_c"],
            mode="lines",
            name="Temperature",
            line=dict(color=CYAN, width=3),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=forecast_df["time"],
            y=forecast_df["feels_like_c"],
            mode="lines",
            name="Feels like",
            line=dict(color=PINK, width=2.6, dash="dot"),
            line_shape="spline",
        )
    )
    figure.add_trace(
        go.Bar(
            x=forecast_df["time"],
            y=forecast_df["humidity_pct"],
            name="Humidity",
            marker_color="rgba(255,216,77,0.28)",
            yaxis="y2",
            opacity=0.8,
        )
    )
    figure.update_layout(
        yaxis2=dict(
            title="Humidity (%)",
            overlaying="y",
            side="right",
            range=[0, 100],
            showgrid=False,
            color=TEXT_COLOR,
        )
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title="Temperature (deg C)")


def create_risk_timeline_figure(timeline_df: pd.DataFrame, title: str) -> go.Figure:
    figure = go.Figure()
    colors = {"heatwave": PINK, "flood": CYAN, "storm": YELLOW}
    for key, label in [("heatwave", "Heatwave"), ("flood", "Flood"), ("storm", "Storm")]:
        if key not in timeline_df:
            continue
        figure.add_trace(
            go.Scatter(
                x=timeline_df["time"],
                y=timeline_df[key],
                mode="lines",
                name=label,
                line=dict(color=colors[key], width=2.5),
                line_shape="spline",
            )
        )
    figure.update_yaxes(range=[0, 100])
    return _apply_chart_style(figure, title=title, xaxis_title="Time", yaxis_title="Risk score")


def create_raw_heatmap(lon: np.ndarray, lat: np.ndarray, z: np.ndarray, title: str, colorscale: str = "Turbo", colorbar_title: str = "Value") -> go.Figure:
    figure = go.Figure(
        data=[go.Heatmap(z=z, x=lon, y=lat, colorscale=colorscale, zsmooth="best",
                         colorbar=dict(title=colorbar_title),
                         hovertemplate="Lat %{y:.1f}<br>Lon %{x:.1f}<br>Value %{z:.2f}<extra></extra>")]
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Longitude", yaxis_title="Latitude", show_legend=False)


def create_story_heatmap() -> go.Figure:
    lat_vals = np.linspace(-90, 90, 61)
    lon_vals = np.linspace(-180, 180, 121)
    lon_mesh, lat_mesh = np.meshgrid(lon_vals, lat_vals)
    values = (
        0.2 + 0.55 * np.sin(np.deg2rad(lat_mesh)) ** 2
        + 0.18 * np.cos(np.deg2rad(lon_mesh / 1.7))
        + 0.12 * np.sin(np.deg2rad((lat_mesh + lon_mesh) / 2.8))
    )
    return create_raw_heatmap(lon_vals, lat_vals, values, "Global Temperature Heatmap", colorbar_title="Temp anomaly (deg C)")


def create_story_timeline(years: list[int], values: list[float], title: str) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=years, y=values,
            mode="lines+markers",
            line=dict(color=CYAN, width=3, shape="spline"),
            marker=dict(size=9, color=YELLOW),
            fill="tozeroy", fillcolor="rgba(0,229,255,0.12)",
            name="Global anomaly",
        )
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Year", yaxis_title="Temperature anomaly (deg C)", show_legend=False)


def create_story_comparison(years: list[int], series: dict[str, list[float]], colors: dict[str, str], title: str) -> go.Figure:
    figure = go.Figure()
    for name, y_values in series.items():
        figure.add_trace(
            go.Scatter(
                x=years, y=y_values,
                mode="lines+markers",
                line=dict(color=colors.get(name, CYAN), width=3, shape="spline"),
                marker=dict(size=8),
                name=name,
            )
        )
    return _apply_chart_style(figure, title=title, xaxis_title="Year", yaxis_title="Temperature anomaly (deg C)")


def create_story_bar(records: list[dict], title: str, value_key: str = "events", label_key: str = "year") -> go.Figure:
    x_vals = [r[label_key] for r in records]
    y_vals = [r[value_key] for r in records]
    figure = go.Figure(
        data=[go.Bar(x=x_vals, y=y_vals, marker=dict(color=YELLOW, line=dict(color="#000000", width=1)),
                     hovertemplate=f"{{x}}<br>{{y}}<extra></extra>", name="Count")]
    )
    return _apply_chart_style(figure, title=title, xaxis_title="Year", yaxis_title="Event count", show_legend=False)


def create_story_scenarios(scenarios: dict[str, dict], colors: dict[str, str], title: str) -> go.Figure:
    figure = go.Figure()
    for name, payload in scenarios.items():
        figure.add_trace(
            go.Scatter(
                x=payload["years"], y=payload["warming_c"],
                mode="lines+markers",
                line=dict(color=colors.get(name, CYAN), width=3, shape="spline"),
                marker=dict(size=8),
                name=name.replace("_", " ").title(),
            )
        )
    return _apply_chart_style(figure, title=title, xaxis_title="Year", yaxis_title="Projected warming (deg C)")
