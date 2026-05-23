"""Helpers compartidos: rutas, exportación de figuras Plotly al sitio."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import plotly.graph_objects as go

# Rutas absolutas calculadas desde la ubicación de este archivo
ROOT = Path(__file__).resolve().parents[2]
ANALYTICS = ROOT / "analytics"
RAW = ANALYTICS / "data" / "raw"
PROCESSED = ANALYTICS / "data" / "processed"
OUTPUT = ANALYTICS / "output"
SITE_CHARTS = ROOT / "static" / "data" / "charts"

# Tema base para que los gráficos hereden la estética editorial del sitio.
# El front (charts.js) inyecta paper/plot bg en función del tema activo.
EDITORIAL_LAYOUT: dict[str, Any] = {
    "font": {
        "family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "size": 13,
        "color": "#1a1a1a",
    },
    "title": {
        "font": {
            "family": "'Crimson Pro', Georgia, serif",
            "size": 20,
            "color": "#1a1a1a",
        },
        "x": 0,
        "xanchor": "left",
    },
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"t": 60, "b": 60, "l": 70, "r": 30},
    "xaxis": {"gridcolor": "#e2dfd7", "zerolinecolor": "#e2dfd7"},
    "yaxis": {"gridcolor": "#e2dfd7", "zerolinecolor": "#e2dfd7"},
    "colorway": ["#8a2424", "#1f3a8a", "#1f7a44", "#a87a1f", "#5a3a8a", "#4a4a4a"],
    "hoverlabel": {
        "bgcolor": "#fbfaf6",
        "bordercolor": "#8a2424",
        "font": {"family": "Inter, sans-serif", "size": 12, "color": "#1a1a1a"},
    },
}


def export(fig: go.Figure, chart_id: str, *, source: str | None = None) -> None:
    """
    Exporta una figura Plotly a JSON en dos lugares:
    - analytics/output/{chart_id}.json   (auditoría / debug)
    - static/data/charts/{chart_id}.json (consumido por el sitio)
    """
    OUTPUT.mkdir(parents=True, exist_ok=True)
    SITE_CHARTS.mkdir(parents=True, exist_ok=True)

    # Aplicar tema editorial sin sobrescribir lo que el script ya definió
    base_layout = dict(EDITORIAL_LAYOUT)
    fig.update_layout(**{k: v for k, v in base_layout.items() if k not in fig.layout})

    payload: dict[str, Any] = json.loads(fig.to_json())
    if source:
        payload.setdefault("meta", {})["source"] = source

    out_paths = [OUTPUT / f"{chart_id}.json", SITE_CHARTS / f"{chart_id}.json"]
    for p in out_paths:
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  wrote {p.relative_to(ROOT)}")
