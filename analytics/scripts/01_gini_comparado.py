"""
C001 — Coeficiente de Gini comparado.

Verifica la afirmación de la Sección 3 ("Mapa global"):
  > Noruega: Gini ~0,27 (uno de los más bajos del mundo)

Compara seis países representativos del documento: los más cercanos a la
familia ilustrada (Noruega, Dinamarca, Finlandia) y los más lejanos
(Chile, EEUU, Argentina).

Fuentes (cargadas directamente desde CSVs locales en `data/raw/`):
  - OECD Income Distribution Database (IDD) para los cinco países OCDE.
    Filtro: MEASURE=INC_DISP_GINI, AGE=_T, METHODOLOGY=METH2012,
    DEFINITION=D_CUR. Se toma el año más reciente disponible.
  - World Bank `SI.POV.GINI` para Argentina (no OCDE). El valor está en
    escala 0-100, se normaliza a 0-1 para comparar con OECD.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from lib import RAW, export

CHART_ID = "gini-comparado"

OECD_CSV = RAW / "OECD.WISE.INE,DSD_WISE_IDD@DF_IDD,1.0+all.csv"
WB_DIR = RAW / "API_SI.POV.GINI_DS2_en_csv_v2_115456"
WB_CSV = WB_DIR / "API_SI.POV.GINI_DS2_en_csv_v2_115456.csv"

# País → (código ISO-3, grupo). Argentina se resuelve por separado vía World Bank.
OECD_COUNTRIES: dict[str, tuple[str, str]] = {
    "Noruega":          ("NOR", "Cercanos"),
    "Finlandia":        ("FIN", "Cercanos"),
    "Dinamarca":        ("DNK", "Cercanos"),
    "Estados Unidos":   ("USA", "Lejanos"),
    "Chile":            ("CHL", "Lejanos"),
}


def _load_oecd() -> pd.DataFrame:
    """Gini OCDE — último año disponible por país, población total."""
    df = pd.read_csv(OECD_CSV, low_memory=False)
    mask = (
        (df["MEASURE"] == "INC_DISP_GINI")
        & (df["AGE"] == "_T")
        & (df["METHODOLOGY"] == "METH2012")
        & (df["DEFINITION"] == "D_CUR")
        & (df["REF_AREA"].isin([code for code, _ in OECD_COUNTRIES.values()]))
    )
    sub = df.loc[mask, ["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]].dropna()
    # Último año disponible por país
    latest = sub.sort_values("TIME_PERIOD").groupby("REF_AREA").tail(1)

    code_to_label = {code: name for name, (code, _) in OECD_COUNTRIES.items()}
    code_to_group = {code: grp for _, (code, grp) in OECD_COUNTRIES.items()}
    return pd.DataFrame({
        "pais":   latest["REF_AREA"].map(code_to_label).values,
        "gini":   latest["OBS_VALUE"].round(3).values,
        "anio":   latest["TIME_PERIOD"].astype(int).values,
        "fuente": "OECD IDD",
        "grupo":  latest["REF_AREA"].map(code_to_group).values,
    })


def _load_worldbank_argentina() -> pd.DataFrame:
    """Gini Argentina — último año no nulo del World Bank (escala 0-100 → 0-1)."""
    df = pd.read_csv(WB_CSV, skiprows=4)
    row = df.loc[df["Country Code"] == "ARG"].iloc[0]
    years = [c for c in df.columns if c.isdigit()]
    available = [(int(y), row[y]) for y in years if pd.notna(row[y])]
    year, value = available[-1]
    return pd.DataFrame([{
        "pais":   "Argentina",
        "gini":   round(value / 100, 3),
        "anio":   year,
        "fuente": "World Bank",
        "grupo":  "Lejanos",
    }])


def _load_data() -> pd.DataFrame:
    return pd.concat([_load_oecd(), _load_worldbank_argentina()], ignore_index=True)


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

    years = sorted(df["anio"].unique())
    year_range = f"{years[0]}" if len(years) == 1 else f"{years[0]}–{years[-1]}"

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
                "text": f"Fuente: OECD IDD y World Bank (Argentina), años {year_range}",
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
    export(build(), CHART_ID, source="OECD IDD; World Bank (Argentina)")
