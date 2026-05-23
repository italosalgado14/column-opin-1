# Fuentes de datos crudos

Cada archivo en este directorio debe tener una entrada aquí.

## `analytics/data/raw/API_SI.POV.GINI_DS2_en_csv_v2_115456`

- **Descripción**: Coeficiente de Gini (ingreso disponible, después de impuestos y transferencias) por país.
- **Fuente**: World Bank Group
- **Indicador OECD**: `Gini index`
- **Año de referencia**: año más reciente disponible por país (2021-2023 según país).
- **Descarga manual**: https://data.worldbank.org/indicator/SI.POV.GINI?end=2025&start=2025&view=bar&year=2025
- **Fecha de incorporación**: 2026-05-09
- **Notas**: 

## `analytics/data/raw/OECD.WISE.INE,DSD_WISE_IDD@DF_IDD,1.0+all.csv`

- **Descripción**: Coeficiente de Gini (ingreso disponible, después de impuestos y transferencias) por país.
- **Fuente**: OECD Income Distribution Database — <https://www.oecd.org/social/income-distribution-database.htm>
- **Indicador OECD**: `IDD: Income Distribution and Poverty / Gini (disposable income, post taxes and transfers)`
- **Año de referencia**: año más reciente disponible por país (2021-2023 según país).
- **Descarga manual**: filtrar por TIME = "latest", METHODE = "current", AGE = "TOT".
- **Para Argentina** (no OCDE): World Bank — <https://data.worldbank.org/indicator/SI.POV.GINI?locations=AR>
- **Fecha de incorporación**: 2026-05-09
- **Notas**: para reproducibilidad sin descarga manual, los valores están "hardcoded" en `scripts/01_gini_comparado.py` con la fuente comentada por país. Cuando descargues los CSV reales, reemplaza la lógica por `pd.read_csv("data/raw/gini-oecd.csv")`.
