"""Descarga la tabla PSCompPars del NASA Exoplanet Archive.

Consulta el endpoint TAP (Table Access Protocol) en modo síncrono y
guarda el CSV crudo en data/raw/. El archivo crudo nunca se edita a
mano; para refrescarlo se vuelve a correr este script.

Uso (desde la raíz del repo, con el venv activado):
    python src/download_data.py
"""

from pathlib import Path

import requests

TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# Selección explícita de columnas: solo lo que el análisis necesita.
COLUMNS = [
    "pl_name",          # nombre del planeta
    "discoverymethod",  # método de detección (Transit, Radial Velocity, ...)
    "disc_year",        # año de descubrimiento
    "pl_bmasse",        # masa del planeta [masas terrestres]
    "pl_bmassprov",     # procedencia de la masa (medida, Msini o estimada por relación M-R)
    "pl_rade",          # radio del planeta [radios terrestres]
    "pl_orbper",        # período orbital [días]
    "pl_orbsmax",       # semi-eje mayor de la órbita [UA]
    "pl_eqt",           # temperatura de equilibrio [K]
    "sy_dist",          # distancia al sistema [parsecs]
    "st_teff",          # temperatura efectiva de la estrella [K]
    "st_rad",           # radio de la estrella [radios solares]
]

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "pscomppars.csv"


def build_query() -> str:
    """Devuelve la consulta ADQL para la tabla PSCompPars."""
    return f"select {', '.join(COLUMNS)} from pscomppars"


def download(query: str, output_path: Path) -> None:
    """Ejecuta la consulta TAP y escribe la respuesta CSV en output_path."""
    response = requests.get(
        TAP_URL,
        params={"query": query, "format": "csv"},
        timeout=120,
    )
    response.raise_for_status()
    output_path.write_bytes(response.content)


def main() -> None:
    query = build_query()
    print(f"Consultando el NASA Exoplanet Archive:\n  {query}")
    download(query, OUTPUT_PATH)
    n_rows = sum(1 for _ in OUTPUT_PATH.open(encoding="utf-8")) - 1  # fila de encabezado
    print(f"Se guardaron {n_rows} planetas en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
