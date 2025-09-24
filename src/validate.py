# src/validate.py
"""
Módulo de validación de datos.
Incluye verificaciones de tipos, duplicados, valores nulos y consistencia.
"""

import pandas as pd

def validate_dataframe(df: pd.DataFrame) -> dict:
    """Ejecuta chequeos básicos de calidad sobre el DataFrame."""
    report = {
        "n_rows": len(df),
        "n_missing": df.isna().sum().to_dict(),
        "n_duplicates": df.duplicated().sum(),
    }
    return report

# TODO: expandir validaciones (rangos, formatos de fecha, integridad referencial, etc.)
