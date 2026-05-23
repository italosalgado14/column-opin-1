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
- **Notas**: el script `scripts/01_gini_comparado.py` ya consume estos CSV directamente (filtros: MEASURE=INC_DISP_GINI, AGE=_T, METHODOLOGY=METH2012, DEFINITION=D_CUR, último año disponible por país).

## `analytics/data/raw/owid-trust-in-government.csv`

- **Descripción**: Porcentaje de personas que confían en el gobierno nacional ("a lot" o "some" en la encuesta Wellcome Global Monitor 2020).
- **Fuente**: Wellcome Trust (2020) — procesado por Our World in Data.
- **URL del dataset**: <https://ourworldindata.org/grapher/share-who-trust-government>
- **Descarga directa (CSV)**: <https://ourworldindata.org/grapher/share-who-trust-government.csv>
- **Cobertura**: ~106 países, año 2020. Incluye Noruega, Dinamarca, Finlandia, Chile, Estados Unidos y Argentina en un solo archivo.
- **Fecha de incorporación**: 2026-05-23
- **Notas**: serie de un solo año (2020), pre-pandemia para varios países y mid-pandemia para otros. Verifica la afirmación "Confianza institucional alta (top 3 mundial)" sobre Noruega.
