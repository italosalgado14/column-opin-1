"""
C003 — PISA matemáticas comparado.

Verifica la afirmación de la Sección 3 ("Mapa global") sobre Noruega:
  > Educación pública seria, exigente, igualitaria, sin selección temprana

Compara los mismos seis países usados en los gráficos previos:
Noruega, Finlandia, Dinamarca (cercanos a la familia ilustrada) frente a
Estados Unidos, Chile y Argentina (lejanos).

Fuente: OECD PISA (Programme for International Student Assessment),
ronda 2022 — puntaje promedio en matemáticas de estudiantes de 15 años,
procesado por Our World in Data. Archivo en
`data/raw/owid-pisa-mathematics.csv`.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from lib import RAW, export

CHART_ID = "pisa-matematicas"
CSV = RAW / "owid-pisa-mathematics.csv"
VALUE_COL = "Mathematics"

# País OWID → (etiqueta ES, grupo). Misma lista que los gráficos previos.
COUNTRIES: dict[str, tuple[str, str]] = {
    "Norway":         ("Noruega",        "Cercanos"),
    "Finland":        ("Finlandia",      "Cercanos"),
    "Denmark":        ("Dinamarca",      "Cercanos"),
    "United States":  ("Estados Unidos", "Lejanos"),
    "Chile":          ("Chile",          "Lejanos"),
    "Argentina":      ("Argentina",      "Lejanos"),
}

# Referencia OECD: el promedio OCDE en matemáticas PISA 2022 fue 472.
OECD_AVERAGE_2022 = 472


def _load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    sub = df[df["Entity"].isin(COUNTRIES.keys())].copy()
    latest = sub.sort_values("Year").groupby("Entity").tail(1)

    name_map = {orig: es for orig, (es, _) in COUNTRIES.items()}
    group_map = {orig: grp for orig, (_, grp) in COUNTRIES.items()}
    return pd.DataFrame({
        "pais":   latest["Entity"].map(name_map).values,
        "score":  latest[VALUE_COL].round(0).astype(int).values,
        "anio":   latest["Year"].astype(int).values,
        "fuente": "OECD PISA / OWID",
        "grupo":  latest["Entity"].map(group_map).values,
    })


def build() -> go.Figure:
    df = _load_data().sort_values("score")

    color_map = {"Cercanos": "#1f3a8a", "Lejanos": "#8a2424"}
    colors = [color_map[g] for g in df["grupo"]]

    fig = go.Figure(
        go.Bar(
            x=df["score"],
            y=df["pais"],
            orientation="h",
            marker_color=colors,
            text=[f"{v}" for v in df["score"]],
            textposition="outside",
            customdata=df[["anio", "fuente", "grupo"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Puntaje: %{x}<br>"
                "Año: %{customdata[0]}<br>"
                "Fuente: %{customdata[1]}<br>"
                "Grupo: %{customdata[2]}"
                "<extra></extra>"
            ),
        )
    )

    years = sorted(df["anio"].unique())
    year_range = f"{years[0]}" if len(years) == 1 else f"{years[0]}–{years[-1]}"

    fig.update_layout(
        title={
            "text": "Desempeño en matemáticas · PISA",
            "subtitle": {"text": "Puntaje promedio a los 15 años — mismos seis países"},
        },
        xaxis_title="Puntaje PISA matemáticas (promedio OCDE 2022 ≈ 472)",
        yaxis_title="",
        showlegend=False,
        height=400,
        shapes=[
            {
                "type": "line",
                "x0": OECD_AVERAGE_2022, "x1": OECD_AVERAGE_2022,
                "y0": -0.5, "y1": len(df) - 0.5,
                "line": {"color": "#6e6e6e", "width": 1, "dash": "dash"},
            }
        ],
        annotations=[
            {
                "text": f"Promedio OCDE {OECD_AVERAGE_2022}",
                "x": OECD_AVERAGE_2022, "y": len(df) - 0.5,
                "xanchor": "left", "yanchor": "bottom",
                "showarrow": False,
                "font": {"size": 10, "color": "#6e6e6e"},
            },
            {
                "text": f"Fuente: OECD PISA vía Our World in Data ({year_range})",
                "xref": "paper", "yref": "paper",
                "x": 0, "y": -0.22, "xanchor": "left", "yanchor": "top",
                "showarrow": False,
                "font": {"size": 11, "color": "#6e6e6e"},
            },
        ],
    )
    fig.update_xaxes(range=[350, 550])

    return fig


if __name__ == "__main__":
    export(build(), CHART_ID, source="OECD PISA 2022 (OWID)")
