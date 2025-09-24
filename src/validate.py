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
# src/validate.py
from __future__ import annotations

from typing import List
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype


def basic_checks(df: pd.DataFrame) -> List[str]:
    """
    Ejecuta validaciones mínimas sobre esquema canónico.

    Reglas:
    - Columnas canónicas presentes: 'date', 'partner', 'amount'
    - 'date' es datetime64[*] y sin NaT
    - 'amount' es numérico y >= 0 (sin valores negativos)

    Returns
    -------
    List[str]
        Lista de mensajes de error (vacía si todo ok).
    """
    errors: List[str] = []

    required = {"date", "partner", "amount"}
    missing = required - set(df.columns)
    if missing:
        errors.append(f"Faltan columnas canónicas: {sorted(missing)}")
        # Si faltan columnas clave, el resto de checks pueden fallar; continuar con lo disponible.

    # Check 'date'
    if "date" in df.columns:
        if not is_datetime64_any_dtype(df["date"]):
            try:
                coerced = pd.to_datetime(df["date"], errors="coerce")
            except Exception:
                coerced = pd.Series([pd.NaT] * len(df))
            if not is_datetime64_any_dtype(coerced):
                errors.append("La columna 'date' no es de tipo datetime.")
            if coerced.isna().any():
                errors.append(f"'date' contiene {int(coerced.isna().sum())} valores no parseables (NaT).")
        else:
            if df["date"].isna().any():
                errors.append(f"'date' contiene {int(df['date'].isna().sum())} valores NaT.")

    # Check 'amount'
    if "amount" in df.columns:
        if not is_numeric_dtype(df["amount"]):
            # Intento de coerción para informar con precisión
            coerced = pd.to_numeric(df["amount"], errors="coerce")
            if not is_numeric_dtype(coerced):
                errors.append("La columna 'amount' no es numérica.")
            if coerced.isna().any():
                errors.append(f"'amount' contiene {int(coerced.isna().sum())} valores no numéricos (NaN tras coerción).")
        # Valores negativos
        try:
            negatives = (pd.to_numeric(df["amount"], errors="coerce") < 0).sum()
            if negatives > 0:
                errors.append(f"'amount' contiene {int(negatives)} valores negativos.")
        except Exception:
            # Si no se pudo convertir, ya habrá error anterior
            pass

    return errors

