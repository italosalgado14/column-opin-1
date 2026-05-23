"""
Pipeline completo. Corre todos los scripts numerados y exporta sus charts.

Uso:
    python scripts/build_all.py
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

# Permite ejecutar tanto con `python scripts/build_all.py` como
# `python -m scripts.build_all` desde el directorio analytics/.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Cuando agregues un análisis nuevo, súmalo aquí
MODULES: list[str] = [
    "01_gini_comparado",
]


def main() -> int:
    print(f"[build_all] {len(MODULES)} análisis a procesar\n")
    failures: list[tuple[str, Exception]] = []

    for mod_name in MODULES:
        print(f"→ {mod_name}")
        t0 = time.perf_counter()
        try:
            mod = importlib.import_module(mod_name)
            from lib import export  # noqa: PLC0415
            chart_id = getattr(mod, "CHART_ID", mod_name)
            export(mod.build(), chart_id)
            elapsed = (time.perf_counter() - t0) * 1000
            print(f"  ok ({elapsed:.0f} ms)\n")
        except Exception as exc:  # noqa: BLE001
            failures.append((mod_name, exc))
            print(f"  ERROR: {exc}\n")

    if failures:
        print(f"\n[build_all] {len(failures)} fallaron:")
        for name, exc in failures:
            print(f"  - {name}: {exc}")
        return 1
    print(f"[build_all] todos los análisis se exportaron correctamente.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
