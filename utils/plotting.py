"""
utils/plotting.py
------------------
Plotly figure builders. All charts share one dark, glassy theme so the
app looks like one cohesive product instead of a stack of default plots.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from ui.theme import PALETTE, BAND_COLORS

PLOT_BG = "rgba(0,0,0,0)"
FONT_COLOR = PALETTE["text"]
GRID_COLOR = "rgba(255,255,255,0.06)"


def _base_layout(fig, title=None, height=420):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family="Inter, sans-serif"),
        title=dict(text=title, font=dict(size=17, color="#FFFFFF")) if title else None,
        margin=dict(l=40, r=30, t=50 if title else 20, b=40),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.18),
        hoverlabel=dict(bgcolor="#1a2036", font_color="#fff"),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    fig.update_yaxes(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR)
    return fig


def eeg_time_series(times: np.ndarray, data: np.ndarray, ch_names: list[str], title="Raw EEG", max_channels=12):
    """data shape: (n_channels, n_samples). Stacks channels vertically like a real EEG viewer."""
    n_show = min(max_channels, len(ch_names))
    fig = go.Figure()
    offset_step = np.nanmax(np.abs(data[:n_show])) * 2.2 if data.size else 1.0
    offset_step = offset_step if offset_step > 0 else 1.0

    palette_cycle = px.colors.qualitative.Prism
    for i in range(n_show):
        fig.add_trace(
            go.Scattergl(
                x=times,
                y=data[i] + i * offset_step,
                mode="lines",
                name=ch_names[i],
                line=dict(width=1, color=palette_cycle[i % len(palette_cycle)]),
                hovertemplate=f"{ch_names[i]}<br>t=%{{x:.2f}}s<extra></extra>",
            )
        )
    fig.update_yaxes(
        tickvals=[i * offset_step for i in range(n_show)],
        ticktext=ch_names[:n_show],
        showgrid=False,
    )
    fig.update_xaxes(title="Time (s)")
    return _base_layout(fig, title=title, height=max(420, n_show * 28))


def psd_line_chart(freqs, psd_matrix, ch_names, title="Power Spectral Density"):
    fig = go.Figure()
    palette_cycle = px.colors.qualitative.Prism
    psd_db = 10 * np.log10(np.maximum(psd_matrix, 1e-20))
    for i, ch in enumerate(ch_names):
        fig.add_trace(
            go.Scatter(
                x=freqs,
                y=psd_db[i],
                mode="lines",
                name=ch,
                line=dict(width=1.6, color=palette_cycle[i % len(palette_cycle)]),
            )
        )
    fig.update_xaxes(title="Frequency (Hz)")
    fig.update_yaxes(title="Power (dB)")
    return _base_layout(fig, title=title, height=450)


def band_waveform(times, signal, band_name, title=None):
    color = BAND_COLORS.get(band_name, PALETTE["accent"])
    fig = go.Figure()
    fig.add_trace(
        go.Scattergl(
            x=times,
            y=signal,
            mode="lines",
            line=dict(width=1.3, color=color),
            fill="tozeroy",
            fillcolor=color.replace(")", ", 0.08)").replace("rgb", "rgba") if "rgb" in color else None,
            name=band_name,
        )
    )
    fig.update_xaxes(title="Time (s)")
    fig.update_yaxes(title="Amplitude (µV)")
    return _base_layout(fig, title=title or f"{band_name} Band Waveform", height=380)


def band_power_bar(df: pd.DataFrame, title="Average Band Power"):
    means = df.mean(axis=0)
    fig = go.Figure(
        go.Bar(
            x=means.index,
            y=means.values,
            marker_color=[BAND_COLORS.get(b, PALETTE["accent"]) for b in means.index],
            text=[f"{v:.3f}" for v in means.values],
            textposition="outside",
        )
    )
    fig.update_yaxes(title="Power")
    return _base_layout(fig, title=title, height=380)


def band_power_heatmap(df: pd.DataFrame, title="Band Power by Channel"):
    fig = go.Figure(
        go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            colorscale="Viridis",
            colorbar=dict(title="Power"),
        )
    )
    return _base_layout(fig, title=title, height=max(420, len(df) * 16))


def band_power_radar(df: pd.DataFrame, title="Band Power Profile"):
    means = df.mean(axis=0)
    categories = list(means.index) + [means.index[0]]
    values = list(means.values) + [means.values[0]]
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            line=dict(color=PALETTE["accent"]),
            fillcolor="rgba(124,77,255,0.25)",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(gridcolor=GRID_COLOR, showticklabels=True),
            angularaxis=dict(gridcolor=GRID_COLOR),
        )
    )
    return _base_layout(fig, title=title, height=420)


def sensor_map_scatter(positions: dict, title="Electrode Sensor Map"):
    names = list(positions.keys())
    xs = [positions[n][0] for n in names]
    ys = [positions[n][1] for n in names]
    fig = go.Figure(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            text=names,
            textposition="top center",
            marker=dict(
                size=16,
                color=PALETTE["accent_soft"],
                line=dict(width=2, color=PALETTE["cyan"]),
                opacity=0.9,
            ),
        )
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
    return _base_layout(fig, title=title, height=520)


def ica_components_grid(sources: np.ndarray, times: np.ndarray, n_show=8, title="ICA Components"):
    n_show = min(n_show, sources.shape[0])
    fig = go.Figure()
    offset_step = np.nanmax(np.abs(sources[:n_show])) * 2.2 if sources.size else 1.0
    offset_step = offset_step if offset_step > 0 else 1.0
    for i in range(n_show):
        fig.add_trace(
            go.Scattergl(
                x=times,
                y=sources[i] + i * offset_step,
                mode="lines",
                name=f"IC{i:03d}",
                line=dict(width=1),
            )
        )
    fig.update_yaxes(
        tickvals=[i * offset_step for i in range(n_show)],
        ticktext=[f"IC{i:03d}" for i in range(n_show)],
        showgrid=False,
    )
    fig.update_xaxes(title="Time (s)")
    return _base_layout(fig, title=title, height=max(420, n_show * 40))
