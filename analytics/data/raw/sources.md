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
- **Notas**: serie de un solo año (2020). Reemplazada por `oecd-hsl-trust-in-government.csv` (serie temporal) en el script `02_confianza_gobierno.py`. Se conserva como referencia cruzada.

## `analytics/data/raw/oecd-hsl-trust-in-government.csv`

- **Descripción**: Confianza en el gobierno nacional, % de la población de 15+ años. Serie temporal 2006-2025, promedios trianuales (cada valor cubre una ola de ~3 años del Gallup World Poll).
- **Fuente**: OECD How's Life — Future Well-being, dataflow `DSD_HSL@DF_HSL_FWB`, medida `14_3` ("Trust in government"). Construida sobre Gallup World Poll.
- **Descarga directa (CSV)**: <https://sdmx.oecd.org/public/rest/data/OECD.WISE.WDP,DSD_HSL@DF_HSL_FWB,/?format=csvfilewithlabels&startPeriod=2006>
- **Filtros aplicados al guardar**: `MEASURE=14_3`, `UNIT_MEASURE=PT_POP_Y_GE15`, `AGE=_T`, `SEX=_T`, `EDUCATION_LEV=_T`, `REF_AREA` ∈ {NOR, FIN, DNK, USA, CHL, ARG}.
- **Cobertura**: 6 países × 20 años = 120 filas. Todos los seis países del marco tienen cobertura anual completa 2006-2025.
- **Fecha de incorporación**: 2026-05-23
- **Notas**: el script `02_confianza_gobierno.py` deduplica bloques de años con el mismo valor y conserva un punto por ola, anclado al año central del bloque.

## `analytics/data/raw/owid-pisa-mathematics.csv`

- **Descripción**: Puntaje promedio en matemáticas de estudiantes de 15 años, PISA (2003–2022).
- **Fuente**: OECD Programme for International Student Assessment (PISA) — procesado por Our World in Data.
- **URL del dataset**: <https://ourworldindata.org/grapher/pisa-test-score-mean-performance-on-the-mathematics-scale>
- **Descarga directa (CSV)**: <https://ourworldindata.org/grapher/pisa-test-score-mean-performance-on-the-mathematics-scale.csv>
- **Cobertura**: ~80 países, varias rondas (2003, 2006, 2009, 2012, 2015, 2018, 2022).
- **Fecha de incorporación**: 2026-05-23
- **Notas**: el script toma el año más reciente disponible por país (2022 para los seis del marco). Verifica la afirmación "Educación pública seria, exigente, igualitaria" sobre Noruega.
