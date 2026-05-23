"""
C001 — Coeficiente de Gini comparado.

Verifica la afirmación de la Sección 3 ("Mapa global"):
  > Noruega: Gini ~0,27 (uno de los más bajos del mundo)

Compara seis países representativos del documento: los más cercanos a la
familia ilustrada (Noruega, Dinamarca, Finlandia) y los más lejanos
(Chile, EEUU, Argentina).

Fuente: OECD Income Distribution Database (Gini, ingreso disponible, post
impuestos y transferencias). Para Argentina se usa el Banco Mundial porque
no es país OCDE.

NOTA: los valores aquí están hardcoded con la fuente comentada por país
para que el pipeline sea reproducible sin descarga manual. Cuando descargues
los CSV oficiales a `data/raw/gini-oecd.csv`, reemplaza el `_load_data()`
por `pd.read_csv(RAW / "gini-oecd.csv")`.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from lib import export

CHART_ID = "gini-comparado"


def _load_data() -> pd.DataFrame:
    # País, valor Gini, año, fuente, agrupación según el marco del documento
    rows = [
        # Cercanos a la familia ilustrada
        ("Noruega",    0.276, 2022, "OECD IDD",       "Cercanos"),
        ("Finlandia",  0.276, 2022, "OECD IDD",       "Cercanos"),
        ("Dinamarca",  0.281, 2022, "OECD IDD",       "Cercanos"),
        # Lejanos
        ("Estados Unidos", 0.395, 2022, "OECD IDD",   "Lejanos"),
        ("Chile",          0.430, 2022, "OECD IDD",   "Lejanos"),
        ("Argentina",      0.413, 2022, "World Bank", "Lejanos"),
    ]
    return pd.DataFrame(rows, columns=["pais", "gini", "anio", "fuente", "grupo"])


def build() -> go.Figure:
    df = _load_data().sort_values("gini")

    # Color según grupo: cercanos en azul republicano, lejanos en rojo
    color_map = {"Cercanos": "#1f3a8a", "Lejanos": "#8a2424"}
    colors = [color_map[g] for g in df["grupo"]]

    fig = go.Figure(
        go.Bar(
            x=df["gini"],
            y=df["pais"],
            orientation="h",
            marker_color=colors,
            text=[f"{v:.3f}" for v in df["gini"]],
            textposition="outside",
            customdata=df[["anio", "fuente", "grupo"]].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Gini: %{x:.3f}<br>"
                "Año: %{customdata[0]}<br>"
                "Fuente: %{customdata[1]}<br>"
                "Grupo: %{customdata[2]}"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title={
            "text": "Coeficiente de Gini · ingreso disponible",
            "subtitle": {"text": "Países más cercanos vs más lejanos al modelo ilustrado"},
        },
        xaxis_title="Gini (0 = igualdad perfecta, 1 = desigualdad máxima)",
        yaxis_title="",
        showlegend=False,
        height=400,
        annotations=[
            {
                "text": "Fuente: OECD IDD (2022) y World Bank para Argentina",
                "xref": "paper", "yref": "paper",
                "x": 0, "y": -0.22, "xanchor": "left", "yanchor": "top",
                "showarrow": False,
                "font": {"size": 11, "color": "#6e6e6e"},
            }
        ],
    )
    fig.update_xaxes(range=[0, 0.5])

    return fig


if __name__ == "__main__":
    export(build(), CHART_ID, source="OECD IDD 2022; World Bank Argentina")
