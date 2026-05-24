"""
C002 — Confianza en el gobierno nacional, serie temporal.

Verifica la afirmación de la Sección 3 ("Mapa global"):
  > Noruega: confianza institucional alta (top 3 mundial)

Compara los mismos seis países usados en `01_gini_comparado.py`:
Noruega, Finlandia, Dinamarca (cercanos a la familia ilustrada) frente a
Estados Unidos, Chile y Argentina (lejanos), a lo largo de 2006-últimos
datos disponibles.

Fuente: OECD How's Life — Future Well-being (DSD_HSL@DF_HSL_FWB),
medida 14_3 ("Trust in government"). Construida a partir del Gallup
World Poll. La OECD publica promedios trianuales (cada valor se repite
en bloques de 2-3 años porque corresponde a una "ola"), por lo que para
graficar conservamos un punto por ola en el año central de cada bloque.
Unidad: % de la población de 15+ años que responde "yes".
Archivo: `data/raw/oecd-hsl-trust-in-government.csv`.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from lib import RAW, export

CHART_ID = "confianza-gobierno"
CSV = RAW / "oecd-hsl-trust-in-government.csv"

COUNTRIES: dict[str, tuple[str, str]] = {
    "NOR": ("Noruega",        "Cercanos"),
    "FIN": ("Finlandia",      "Cercanos"),
    "DNK": ("Dinamarca",      "Cercanos"),
    "USA": ("Estados Unidos", "Lejanos"),
    "CHL": ("Chile",          "Lejanos"),
    "ARG": ("Argentina",      "Lejanos"),
}

COLOR_BY_COUNTRY: dict[str, str] = {
    "Noruega":        "#1f3a8a",
    "Finlandia":      "#3b6fd9",
    "Dinamarca":      "#7aa3e8",
    "Estados Unidos": "#8a2424",
    "Chile":          "#c46a3a",
    "Argentina":      "#5a1212",
}


def _load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    df = df[df["REF_AREA"].isin(COUNTRIES.keys())].copy()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)

    # Cada valor se repite en bloques de 2-3 años (olas Gallup pooled).
    # Conservamos un punto por ola, anclado al año central del bloque.
    out = []
    for code, sub in df.groupby("REF_AREA"):
        sub = sub.sort_values("TIME_PERIOD").reset_index(drop=True)
        block_start, block_val = None, None
        block_years: list[int] = []
        for _, row in sub.iterrows():
            yr, val = int(row["TIME_PERIOD"]), float(row["OBS_VALUE"])
            if block_val is None or val != block_val:
                if block_years:
                    out.append((code, block_years, block_val))
                block_val = val
                block_years = [yr]
            else:
                block_years.append(yr)
        if block_years:
            out.append((code, block_years, block_val))

    name_map = {c: es for c, (es, _) in COUNTRIES.items()}
    group_map = {c: grp for c, (_, grp) in COUNTRIES.items()}
    return pd.DataFrame([
        {
            "pais":      name_map[code],
            "anio":      yrs[len(yrs) // 2],   # año central de cada ola
            "ola_desde": yrs[0],
            "ola_hasta": yrs[-1],
            "confianza": round(val, 1),
            "fuente":    "OECD How's Life · Gallup World Poll",
            "grupo":     group_map[code],
        }
        for code, yrs, val in out
    ])


def build() -> go.Figure:
    df = _load_data().sort_values(["pais", "anio"])
    order = ["Noruega", "Finlandia", "Dinamarca", "Estados Unidos", "Chile", "Argentina"]

    fig = go.Figure()
    for pais in order:
        sub = df[df["pais"] == pais]
        if sub.empty:
            continue
        grupo = sub["grupo"].iloc[0]
        customdata = list(zip(sub["ola_desde"], sub["ola_hasta"], [grupo] * len(sub)))
        fig.add_trace(go.Scatter(
            x=sub["anio"],
            y=sub["confianza"],
            mode="lines+markers",
            name=pais,
            line={"color": COLOR_BY_COUNTRY[pais], "width": 2.2},
            marker={"size": 7},
            customdata=customdata,
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Ola: %{customdata[0]}–%{customdata[1]}<br>"
                "Confianza: %{y:.1f}%<br>"
                "Grupo: %{customdata[2]}"
                "<extra></extra>"
            ),
        ))

    last_year = int(df["anio"].max())
    first_year = int(df["anio"].min())
    fig.update_layout(
        title={
            "text": "Confianza en el gobierno nacional · evolución temporal",
            "subtitle": {
                "text": f"% que responde \"sí\" — promedios trianuales, {first_year}–{last_year}"
            },
        },
        xaxis_title="Año (centro de cada ola)",
        yaxis_title="Porcentaje de la población (15+ años)",
        showlegend=True,
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.30, "xanchor": "center", "x": 0.5},
        height=460,
        hovermode="x unified",
        annotations=[
            {
                "text": "Fuente: OECD How's Life (Future Well-being, medida 14_3) sobre Gallup World Poll",
                "xref": "paper", "yref": "paper",
                "x": 0, "y": -0.42, "xanchor": "left", "yanchor": "top",
                "showarrow": False,
                "font": {"size": 11, "color": "#6e6e6e"},
            }
        ],
    )
    fig.update_xaxes(dtick=2)
    fig.update_yaxes(range=[0, 100], ticksuffix="%")
    return fig


if __name__ == "__main__":
    export(build(), CHART_ID, source="OECD How's Life · Gallup World Poll")
