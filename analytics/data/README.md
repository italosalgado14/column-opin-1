# Datos

## Convención

- `raw/` contiene archivos descargados **sin modificar** (CSV, XLSX, JSON tal como vienen de la fuente).
- `processed/` contiene los datasets limpios listos para graficar. Estos sí los generan los scripts.
- Cualquier archivo en `raw/` debe estar registrado en [`raw/sources.md`](./raw/sources.md) con: URL, fecha de descarga, archivo, descripción.

## Tamaño

Si un dataset crudo supera 50 MB, **no lo subas al repo**. Documéntalo en `sources.md` con el comando exacto para descargarlo. Para datasets pesados, considera Git LFS o un bucket externo.

## Reproducibilidad

`processed/` debe poder regenerarse desde `raw/` corriendo `python scripts/build_all.py`. No edites manualmente archivos en `processed/`.
