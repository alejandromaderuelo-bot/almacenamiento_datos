# streamlit_app.py
"""
Streamlit app para ingestar múltiples CSV heterogéneos, normalizarlos al
esquema canónico (date, partner, amount), etiquetar linaje y derivar una
capa silver (partner × mes). Muestra validaciones, KPIs y permite descargar
bronze/silver como CSV.

Requiere:
- pandas, streamlit, pyarrow (para CSV/Parquet si se amplía)
- Módulos locales en ./src: ingest.py, transform.py, validate.py
"""

from __future__ import annotations

from io import StringIO
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st

# Importar funciones del proyecto
from src.transform import normalize_columns, to_silver
from src.ingest import tag_lineage, concat_bronze
from src.validate import basic_checks


# -----------------------------
# Utilidades
# -----------------------------
def read_csv_with_fallback(file) -> pd.DataFrame:
    """
    Lee un CSV intentando primero utf-8; si falla, usa latin-1.
    Usa inferencia de separador (engine='python') para tolerar ; o ,
    """
    try:
        return pd.read_csv(file, sep=None, engine="python")
    except UnicodeDecodeError:
        # Reiniciar el puntero y reintentar con latin-1
        file.seek(0)
        return pd.read_csv(file, sep=None, engine="python", encoding="latin-1")


def build_mapping(src_date: str, src_partner: str, src_amount: str) -> Dict[str, str]:
    """
    Construye mapping origen->canónico solo con entradas no vacías.
    """
    mapping: Dict[str, str] = {}
    if src_date.strip():
        mapping[src_date.strip()] = "date"
    if src_partner.strip():
        mapping[src_partner.strip()] = "partner"
    if src_amount.strip():
        mapping[src_amount.strip()] = "amount"
    return mapping


def bytes_csv(df: pd.DataFrame) -> bytes:
    """Convierte DataFrame a CSV (UTF-8, sin índice) listo para descarga."""
    return df.to_csv(index=False).encode("utf-8")


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Big Data Storage Lab", page_icon="📦", layout="wide")
st.title("📦 Big Data Storage Lab — Bronze & Silver")

st.caption(
    "Sube múltiples CSV, indica columnas origen para `date`, `partner`, `amount`, "
    "y genera unificado **bronze** + derivado **silver** (partner × mes)."
)

with st.sidebar:
    st.header("⚙️ Configuración")
    st.markdown("Especifica los nombres de columnas de **origen** en los CSV:")

    src_date = st.text_input("Columna para fecha (origen → date)", value="date")
    src_partner = st.text_input("Columna para partner (origen → partner)", value="partner")
    src_amount = st.text_input("Columna para importe (origen → amount)", value="amount")

    st.markdown("---")
    uploaded = st.file_uploader(
        "Sube uno o más CSV",
        type=["csv"],
        accept_multiple_files=True,
        help="Arrastra varios archivos o selecciónalos desde tu equipo.",
    )

# -----------------------------
# Proceso principal
# -----------------------------
if not uploaded:
    st.info("👆 Sube uno o más CSV para comenzar. Configura los nombres de columnas si difieren.")
    st.stop()

mapping = build_mapping(src_date, src_partner, src_amount)

bronze_frames: List[pd.DataFrame] = []
file_summaries: List[str] = []

st.subheader("📥 Ingesta y Normalización (por archivo)")

for file in uploaded:
    with st.expander(f"Archivo: {file.name}", expanded=False):
        try:
            df_raw = read_csv_with_fallback(file)
        except Exception as e:
            st.error(f"No se pudo leer `{file.name}`: {e}")
            continue

        st.write("Vista previa (primeras 10 filas):")
        st.dataframe(df_raw.head(10), use_container_width=True)

        # Normalizar columnas
        df_norm = normalize_columns(df_raw, mapping=mapping)

        # Etiquetar linaje
        df_tagged = tag_lineage(df_norm, source_name=file.name)

        st.write("Normalizado + linaje (primeras 10 filas):")
        st.dataframe(df_tagged.head(10), use_container_width=True)

        bronze_frames.append(df_tagged)
        file_summaries.append(f"✔️ `{file.name}`: {len(df_tagged)} filas tras normalización")

if not bronze_frames:
    st.error("No se generaron datos normalizados. Revisa los archivos de entrada y el mapping.")
    st.stop()

st.success(" | ".join(file_summaries))

# Unificar bronze
bronze = concat_bronze(bronze_frames)

st.subheader("🟤 Bronze unificado")
st.dataframe(bronze, use_container_width=True, height=320)

# Validaciones
st.subheader("🔍 Validaciones básicas")
errors = basic_checks(bronze)

if errors:
    st.error("Se encontraron problemas en el conjunto **bronze**:")
    for e in errors:
        st.write(f"• {e}")
    st.info(
        "Corrige los nombres de columnas en la barra lateral o limpia tus CSV para cumplir el esquema canónico."
    )
else:
    st.success("Validaciones OK: esquema canónico y reglas mínimas cumplidas.")

# Descarga de bronze
col_bz1, col_bz2 = st.columns([1, 3])
with col_bz1:
    st.download_button(
        "⬇️ Descargar bronze.csv",
        data=bytes_csv(bronze),
        file_name="bronze.csv",
        mime="text/csv",
    )

# Si OK, derivar silver
if not errors:
    silver = to_silver(bronze)

    st.subheader("⚪ Silver (partner × mes)")
    st.dataframe(silver, use_container_width=True, height=320)

    # KPIs simples
    st.subheader("📈 KPIs")
    total_amount = pd.to_numeric(silver["amount"], errors="coerce").su
