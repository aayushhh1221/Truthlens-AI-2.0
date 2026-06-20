"""TruthLens AI — Plotly chart builders (updated design tokens)."""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#AAB3D6"),
    margin=dict(l=0, r=0, t=30, b=0),
)


def make_gauge_chart(score: int, title: str, color: str = "#7C4DFF") -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": title, "font": {"size": 13, "color": "#AAB3D6"}},
        number={"suffix": "%", "font": {"size": 30, "color": "#FFFFFF", "family": "Poppins"}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"color": "#4E5D8A"}, "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.65},
            "bgcolor": "rgba(255,255,255,0.03)",
            "bordercolor": "rgba(255,255,255,0.06)",
            "steps": [
                {"range": [0, 40],  "color": "rgba(0,229,160,0.08)"},
                {"range": [40, 70], "color": "rgba(255,184,0,0.08)"},
                {"range": [70, 100],"color": "rgba(255,69,96,0.08)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.8, "value": score},
        },
    ))
    fig.update_layout(height=210, **_BASE)
    return fig


def make_radar_chart(scores: dict) -> go.Figure:
    cats = list(scores.keys())
    vals = list(scores.values())
    vals.append(vals[0])
    cats.append(cats[0])
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor="rgba(124,77,255,0.12)",
        line=dict(color="#7C4DFF", width=2),
        marker=dict(color="#A67AFF", size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(visible=True, range=[0, 100],
                            gridcolor="rgba(255,255,255,0.07)",
                            linecolor="rgba(255,255,255,0.07)",
                            tickfont=dict(color="#4E5D8A", size=10)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.07)",
                             linecolor="rgba(255,255,255,0.07)",
                             tickfont=dict(color="#AAB3D6", size=11)),
        ),
        height=310, **_BASE,
    )
    return fig


def make_bar_chart(labels: list, values: list, title: str = "") -> go.Figure:
    colors = ["#FF4560" if v >= 70 else "#FFB800" if v >= 40 else "#00E5A0" for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors, marker_line_width=0,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(color="#AAB3D6", size=11),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#AAB3D6")),
        xaxis=dict(range=[0, 115], gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#4E5D8A")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#AAB3D6")),
        height=250, **_BASE,
    )
    return fig


def make_history_line_chart(history: list):
    if not history:
        return None
    df = pd.DataFrame(history)
    fig = px.line(df, x="label", y="fake_score", markers=True,
                  color_discrete_sequence=["#7C4DFF"])
    fig.update_traces(line=dict(width=2.5), marker=dict(size=8, color="#A67AFF"))
    fig.update_layout(
        xaxis_title="Analysis Run",
        yaxis_title="Fake Score (%)",
        yaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#4E5D8A")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#4E5D8A")),
        height=270, **_BASE,
    )
    return fig


def make_daily_trend_chart(daily: list):
    """Area chart of analyses per day for the dashboard."""
    if not daily:
        return None
    df = pd.DataFrame(daily)
    fig = go.Figure(go.Scatter(
        x=df["day"], y=df["count"], mode="lines", fill="tozeroy",
        line=dict(color="#00CFFF", width=2.5),
        fillcolor="rgba(0,207,255,0.12)",
    ))
    fig.update_layout(
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#4E5D8A")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#4E5D8A"), title="Analyses"),
        height=260, **_BASE,
    )
    return fig


def make_donut_chart(labels: list, values: list, colors: list = None) -> go.Figure:
    """Donut chart for content-type or verdict distribution."""
    colors = colors or ["#7C4DFF", "#00CFFF", "#00E5A0", "#FFB800", "#FF4560"]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0D1736", width=2)),
        textfont=dict(color="#FFFFFF", size=12),
        textinfo="value",
    ))
    fig.update_layout(
        showlegend=True,
        legend=dict(font=dict(color="#AAB3D6", size=11), orientation="h", y=-0.1),
        height=260, **_BASE,
    )
    return fig
