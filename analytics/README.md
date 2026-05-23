# Analytics — verificación de afirmaciones publicadas

Este directorio contiene el trabajo de análisis que respalda los gráficos y datos publicados en la columna. La idea: **ningún gráfico llega al sitio sin un script reproducible aquí**.

## Filosofía

- **Trazabilidad**: cada gráfico publicado tiene (a) datos crudos en `data/raw/` con su fuente documentada, (b) un script en `scripts/` que lo procesa, y (c) una entrada en [`claims.md`](./claims.md).
- **Reproducible**: cualquier persona con Docker debe poder reproducir todos los gráficos con `docker compose --profile analytics-build run --rm analytics-build`.
- **Separación**: la analítica vive aquí; el sitio sólo consume el JSON final en `static/data/charts/`.

## Estructura

```
analytics/
├── claims.md             # Registro de afirmaciones del documento → estado de verificación
├── data/
│   ├── raw/              # Datos originales (CSV/XLSX descargados) + sources.md
│   ├── processed/        # Datos limpios y normalizados
│   └── README.md
├── notebooks/            # Exploración interactiva (Jupyter Lab)
├── scripts/
│   ├── lib.py            # Helpers: rutas, exportación de figuras Plotly
│   └── build_all.py      # Pipeline completo: corre todos los análisis y exporta charts
└── output/               # JSON Plotly intermedio (también copiado a static/data/charts/)
```

## Cómo correr

### Jupyter Lab (exploración interactiva)

```bash
docker compose --profile analytics up analytics
```

Abre <http://localhost:8888>. No tiene contraseña (entorno local).

### Pipeline completo (para regenerar todos los gráficos publicados)

```bash
docker compose --profile analytics-build run --rm analytics-build
```

Esto:

1. Lee datos en `analytics/data/raw/`.
2. Ejecuta `analytics/scripts/build_all.py`.
3. Escribe JSONs Plotly en `analytics/output/` y los copia a `static/data/charts/`.
4. La próxima vez que Zola compile, los gráficos quedan disponibles en el sitio.

### Sólo Python local (sin Docker)

```bash
cd analytics
pip install -r requirements.txt
python scripts/build_all.py
```

## Cómo agregar un análisis nuevo

1. **Documenta la afirmación** en [`claims.md`](./claims.md) (lo que dice el texto, dónde, qué dato la respalda).
2. **Descarga los datos** a `data/raw/` y agrega entrada en `data/raw/sources.md` con URL, fecha, columnas relevantes.
3. **Crea un script** en `scripts/NN_nombre.py` siguiendo el patrón de `01_gini_comparado.py`:
   - Función `build()` que devuelve un `plotly.graph_objects.Figure`.
   - Constante `CHART_ID` que define el archivo `static/data/charts/{CHART_ID}.json`.
4. **Regístralo** en `scripts/build_all.py` (lista `MODULES`).
5. **Inserta en el .md** correspondiente: `{{ chart(id="mi-chart", title="...") }}`.
6. Corre el pipeline y verifica.

## Cómo escribir un script de análisis

Patrón mínimo (`scripts/NN_titulo.py`):

```python
"""Análisis breve: qué claim verifica, qué fuente usa."""
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
from .lib import RAW, export

CHART_ID = "mi-chart"

def build() -> go.Figure:
    df = pd.read_csv(RAW / "mi-dataset.csv")
    fig = go.Figure(...)
    return fig

if __name__ == "__main__":
    export(build(), CHART_ID)
```

`export()` guarda el JSON en ambos sitios: `analytics/output/` (auditoría) y `static/data/charts/` (consumido por el sitio).
