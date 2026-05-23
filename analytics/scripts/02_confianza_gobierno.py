"""
C002 — Confianza en el gobierno nacional.

Verifica la afirmación de la Sección 3 ("Mapa global"):
  > Noruega: confianza institucional alta (top 3 mundial)

Compara los mismos seis países usados en `01_gini_comparado.py`:
Noruega, Finlandia, Dinamarca (cercanos a la familia ilustrada) frente a
Estados Unidos, Chile y Argentina (lejanos).

Fuente: Wellcome Global Monitor (2020), procesado por Our World in Data.
Pregunta: "¿Cuánto confías en el gobierno nacional?" — proporción que
respondió "mucho" o "algo". Archivo en
`data/raw/owid-trust-in-government.csv`.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from lib import RAW, export

CHART_ID = "confianza-gobierno"
CSV = RAW / "owid-trust-in-government.csv"
VALUE_COL = "Trust the national government in this country"

# País OWID → (etiqueta ES, grupo).
COUNTRIES: dict[str, tuple[str, str]] = {
    "Norway":         ("Noruega",        "Cercanos"),
    "Finland":        ("Finlandia",      "Cercanos"),
    "Denmark":        ("Dinamarca",      "Cercanos"),
    "United States":  ("Estados Unidos", "Lejanos"),
    "Chile":          ("Chile",          "Lejanos"),
    "Argentina":      ("Argentina",      "Lejanos"),
}


def _load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    sub = df[df["Entity"].isin(COUNTRIES.keys())].copy()
    # Por país, último año disponible (OWID sólo tiene 2020 hoy, pero el código
    # queda preparado para futuras actualizaciones).
    latest = sub.sort_values("Year").groupby("Entity").tail(1)

    name_map = {orig: es for orig, (es, _) in COUNTRIES.items()}
    group_map = {orig: grp for orig, (_, grp) in COUNTRIES.items()}
    return pd.DataFrame({
        "pais":      latest["Entity"].map(name_map).values,
        "confianza": latest[VALUE_COL].round(1).values,
        "anio":      latest["Year"].astype(int).values,
        "fuente":    "Wellcome Global Monitor / OWID",
        "grupo":     latest["Entity"].map(group_map).values,
    })


def build() -> go.Figure:
    df = _load_data().sort_values("confianza")

    color_map = {"Cercanos": "#1f3a8a", "Lejanos": "#8a2424"}
    colors = [color_map[g] for g in df["grupo"]]

    fig = go.Figure(
        go.Bar(
            x=df["confianza"],
            y=df["pais"],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1f}%" for v in df["confianza"]],
            textposition="outside",
            customdata=df[["anio", "fuente", "grupo"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Confianza: %{x:.1f}%<br>"
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
            "text": "Confianza en el gobierno nacional",
            "subtitle": {"text": "% que responde \"mucho\" o \"algo\" — mismos seis países"},
        },
        xaxis_title="Porcentaje de la población",
        yaxis_title="",
        showlegend=False,
        height=400,
        annotations=[
            {
                "text": f"Fuente: Wellcome Global Monitor vía Our World in Data ({year_range})",
                "xref": "paper", "yref": "paper",
                "x": 0, "y": -0.22, "xanchor": "left", "yanchor": "top",
                "showarrow": False,
                "font": {"size": 11, "color": "#6e6e6e"},
            }
        ],
    )
    fig.update_xaxes(range=[0, 100], ticksuffix="%")

    return fig


if __name__ == "__main__":
    export(build(), CHART_ID, source="Wellcome Global Monitor 2020 (OWID)")
