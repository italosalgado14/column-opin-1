# Registro de afirmaciones verificables

Tabla viva. Cada fila es una afirmación cuantitativa hecha en la columna y su estado de verificación.

| ID | Afirmación | Sección | Fuente declarada | Estado | Script | Chart |
|----|------------|---------|------------------|--------|--------|-------|
| C001 | Noruega: Gini ~0,27 (uno de los más bajos del mundo) | 3 — Mapa global | OECD Income Inequality | ✅ Verificado | `01_gini_comparado.py` | `gini-comparado` |
| C002 | Chile: gasto público total 24,6% del PIB (2024) | 6 — Diagnóstico Chile | DIPRES, OCDE 2025 | ⏳ Pendiente | — | — |
| C003 | Chile: peso del IVA 45% de la recaudación vs 20,2% OCDE | 6 — Diagnóstico Chile | OCDE Tax Reforms 2023 | ⏳ Pendiente | — | — |
| C004 | España: emancipación juvenil cae del 70% (2008) al 17% actual | 4 — Por qué ganó la emoción | INJUVE / Eurostat | ⏳ Pendiente | — | — |
| C005 | Caídas de 30-40 puntos en confianza institucional en 30 años | 4 — Por qué ganó la emoción | Latinobarómetro / Edelman | ⏳ Pendiente | — | — |
| C006 | Kast gana segunda vuelta 2025 con 58% sobre Jara | 5 — Caso chileno | Servel | ⏳ Pendiente | — | — |
| C007 | Plebiscito septiembre 2022: 62% Rechazo | 5 — Caso chileno | Servel | ⏳ Pendiente | — | — |
| C008 | Chile recaudación tributaria ~22% PIB vs 34% OCDE | 6 — Diagnóstico Chile | OCDE Tax Reforms 2023 | ⏳ Pendiente | — | — |
| C009 | Caídas sostenidas en comprensión lectora PISA OCDE durante 15 años | 4 — Por qué ganó la emoción | OECD PISA | ⏳ Pendiente | — | — |
| C010 | Progress Party Noruega: 24% (presión populista) | 3 — Mapa global | Eleciones noruegas 2025 | ⏳ Pendiente | — | — |

## Convenciones

- **Estado**:
  - ✅ Verificado: dato cargado, comparado con la fuente, gráfico publicado o disponible.
  - 🟡 Parcial: dato cargado, pero la afirmación tiene matices (ej: "uno de los más bajos" — depende de qué países comparas).
  - ⏳ Pendiente: aún no se ha hecho el trabajo.
  - ❌ Refutado: el dato no respalda la afirmación. Hay que corregir el texto.

- **Naming**: `CNNN` correlativo. Los IDs no se reusan; si se elimina un claim se marca `[deprecated]` en lugar de borrarlo.

## Cómo agregar un claim

Cuando edites una sección y agregues una afirmación cuantitativa nueva:
1. Asigna `C0NN` siguiente.
2. Anota fuente declarada (lo que cita el texto).
3. Crea el script en `scripts/` cuando lo verifiques y enlaza.
