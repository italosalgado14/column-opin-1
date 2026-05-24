"""
C001 — Coeficiente de Gini comparado, serie temporal.

Verifica la afirmación de la Sección 3 ("Mapa global"):
  > Noruega: Gini ~0,27 (uno de los más bajos del mundo)

Compara seis países representativos del documento a lo largo del tiempo
(2000–último año disponible): los más cercanos a la familia ilustrada
(Noruega, Dinamarca, Finlandia) y los más lejanos (Chile, EEUU, Argentina).

Fuentes:
  - OECD Income Distribution Database (IDD) para los cinco países OCDE.
    Filtros: MEASURE=INC_DISP_GINI, AGE=_T, METHODOLOGY=METH2012,
    DEFINITION=D_CUR. Se conservan todas las observaciones >= START_YEAR.
  - World Bank `SI.POV.GINI` para Argentina. La escala 0-100 se normaliza
    a 0-1 para compatibilidad con la OECD.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from lib import RAW, export

CHART_ID = "gini-comparado"
START_YEAR = 2000

OECD_CSV = RAW / "OECD.WISE.INE,DSD_WISE_IDD@DF_IDD,1.0+all.csv"
WB_DIR = RAW / "API_SI.POV.GINI_DS2_en_csv_v2_115456"
WB_CSV = WB_DIR / "API_SI.POV.GINI_DS2_en_csv_v2_115456.csv"

OECD_COUNTRIES: dict[str, tuple[str, str]] = {
    "Noruega":          ("NOR", "Cercanos"),
    "Finlandia":        ("FIN", "Cercanos"),
    "Dinamarca":        ("DNK", "Cercanos"),
    "Estados Unidos":   ("USA", "Lejanos"),
    "Chile":            ("CHL", "Lejanos"),
}

COLOR_BY_COUNTRY: dict[str, str] = {
    "Noruega":        "#1f3a8a",
    "Finlandia":      "#3b6fd9",
    "Dinamarca":      "#7aa3e8",
    "Estados Unidos": "#8a2424",
    "Chile":          "#c46a3a",
    "Argentina":      "#5a1212",
}


def _load_oecd() -> pd.DataFrame:
    df = pd.read_csv(OECD_CSV, low_memory=False)
    mask = (
        (df["MEASURE"] == "INC_DISP_GINI")
        & (df["AGE"] == "_T")
        & (df["METHODOLOGY"] == "METH2012")
        & (df["DEFINITION"] == "D_CUR")
        & (df["REF_AREA"].isin([code for code, _ in OECD_COUNTRIES.values()]))
    )
    sub = df.loc[mask, ["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]].dropna()
    sub["TIME_PERIOD"] = sub["TIME_PERIOD"].astype(int)
    sub = sub[sub["TIME_PERIOD"] >= START_YEAR]

    code_to_label = {code: name for name, (code, _) in OECD_COUNTRIES.items()}
    code_to_group = {code: grp for _, (code, grp) in OECD_COUNTRIES.items()}
    return pd.DataFrame({
        "pais":   sub["REF_AREA"].map(code_to_label).values,
        "anio":   sub["TIME_PERIOD"].values,
        "gini":   sub["OBS_VALUE"].round(3).values,
        "fuente": "OECD IDD",
        "grupo":  sub["REF_AREA"].map(code_to_group).values,
    })


def _load_worldbank_argentina() -> pd.DataFrame:
    df = pd.read_csv(WB_CSV, skiprows=4)
    row = df.loc[df["Country Code"] == "ARG"].iloc[0]
    years = [c for c in df.columns if c.isdigit()]
    series = [
        (int(y), round(row[y] / 100, 3))
        for y in years
        if pd.notna(row[y]) and int(y) >= START_YEAR
    ]
    return pd.DataFrame([
        {"pais": "Argentina", "anio": y, "gini": v, "fuente": "World Bank", "grupo": "Lejanos"}
        for y, v in series
    ])


def _load_data() -> pd.DataFrame:
    return pd.concat([_load_oecd(), _load_worldbank_argentina()], ignore_index=True)


def build() -> go.Figure:
    df = _load_data().sort_values(["pais", "anio"])

    # Ordenar leyenda: cercanos primero (más bajos en Gini), luego lejanos
    order = ["Noruega", "Finlandia", "Dinamarca", "Estados Unidos", "Chile", "Argentina"]
    fig = go.Figure()
    for pais in order:
        sub = df[df["pais"] == pais]
        if sub.empty:
            continue
        fuente = sub["fuente"].iloc[0]
        grupo = sub["grupo"].iloc[0]
        fig.add_trace(go.Scatter(
            x=sub["anio"],
            y=sub["gini"],
            mode="lines+markers",
            name=pais,
            line={"color": COLOR_BY_COUNTRY[pais], "width": 2.2},
            marker={"size": 6},
            customdata=[[fuente, grupo]] * len(sub),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Año: %{x}<br>"
                "Gini: %{y:.3f}<br>"
                "Fuente: %{customdata[0]}<br>"
                "Grupo: %{customdata[1]}"
                "<extra></extra>"
            ),
        ))

    last_year = int(df["anio"].max())
    fig.update_layout(
        title={
            "text": "Coeficiente de Gini · evolución temporal",
            "subtitle": {
                "text": f"Países cercanos vs lejanos al modelo ilustrado, {START_YEAR}–{last_year}"
            },
        },
        xaxis_title="Año",
        yaxis_title="Gini (0 = igualdad perfecta, 1 = desigualdad máxima)",
        showlegend=True,
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.30, "xanchor": "center", "x": 0.5},
        height=460,
        hovermode="x unified",
        annotations=[
            {
                "text": "Fuente: OECD IDD (ingreso disponible) y World Bank SI.POV.GINI (Argentina, normalizado 0-1)",
                "xref": "paper", "yref": "paper",
                "x": 0, "y": -0.42, "xanchor": "left", "yanchor": "top",
                "showarrow": False,
                "font": {"size": 11, "color": "#6e6e6e"},
            }
        ],
    )
    fig.update_xaxes(dtick=2)
    fig.update_yaxes(range=[0.2, 0.55])
    return fig


if __name__ == "__main__":
    export(build(), CHART_ID, source="OECD IDD; World Bank (Argentina)")
