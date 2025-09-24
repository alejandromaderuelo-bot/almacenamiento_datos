# src/ingest.py
"""
Módulo de ingesta de datos.
Responsable de leer múltiples CSV heterogéneos y volcarlos a /data/raw.
"""

import pandas as pd
from pathlib import Path

def ingest_csv(path: str) -> pd.DataFrame:
    """Lee un CSV y devuelve un DataFrame de pandas."""
    return pd.read_csv(path)

# TODO: Guardar en /data/raw y registrar metadatos
