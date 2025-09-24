# docs/diccionario.md
# 📖 Diccionario de Datos

Este documento describe el significado, formato y reglas de cada campo incluido en el dataset.

- **Campo**: Nombre de la columna
- **Tipo de dato**: string, int, float, date...
- **Descripción**: qué representa
- **Reglas de validación**: valores permitidos, rangos, restricciones
# docs/gobernanza.md
# 🛡️ Gobernanza de Datos

Políticas aplicadas en este laboratorio:

- Separación de capas (raw, bronze, silver, gold).
- Trazabilidad de orígenes → KPI.
- Restricciones sobre qué datos pueden ser incluidos (solo públicos/sintéticos).
- Versionado de código y documentación en GitHub.
# tests/checklist.md
# ✅ Checklist de validación

- [ ] ¿Los CSV han sido cargados en `/data/raw`?
- [ ] ¿Se ejecutaron validaciones de tipos, nulos y duplicados?
- [ ] ¿Se generaron datasets en `/data/bronze` y `/data/silver`?
- [ ] ¿Los KPIs reflejan datos trazables desde las fuentes?
- [ ] ¿La documentación (`docs/`) está actualizada?
- [ ] # 📖 Diccionario de Datos

Este diccionario describe el **esquema canónico** utilizado en el laboratorio para normalizar datos heterogéneos.

## Esquema Canónico

| Campo    | Tipo de dato | Formato / Unidad | Descripción                                 |
|----------|--------------|------------------|---------------------------------------------|
| date     | date         | YYYY-MM-DD       | Fecha de la transacción o registro          |
| partner  | string       | Texto plano      | Contraparte asociada (cliente/proveedor)    |
| amount   | float        | EUR              | Importe monetario expresado en euros        |

---

## Mapeos Origen → Canónico

Ejemplos de correspondencia entre campos de distintos CSV y el esquema canónico.

| Origen (columna) | Dataset de ejemplo    | Canónico (`date`) | Canónico (`partner`) | Canónico (`amount`) |
|------------------|-----------------------|-------------------|-----------------------|----------------------|
| `fecha`          | ventas_2023.csv       | ✅                | —                     | —                    |
| `customer_name`  | sales_q1.csv          | —                 | ✅                    | —                    |
| `importe_total`  | facturas.csv          | —                 | —                     | ✅                   |
| `transaction_dt` | bank_ops.csv          | ✅                | —                     | —                    |
| `cliente`        | pedidos.csv           | —                 | ✅                    | —                    |
| `valor`          | pagos.csv             | —                 | —                     | ✅                   |

> 📌 **Nota**: los mapeos deben documentarse y actualizarse a medida que se incorporen nuevas fuentes.
# 🛡️ Gobernanza de Datos

Este documento define las políticas de gobernanza aplicadas en el laboratorio.

---

## Origen y Linaje
- Todos los archivos fuente (CSVs) se almacenan en **`/data/raw`**.  
- Cada dataset pasa por fases: **raw → bronze → silver → (gold opcional)**.  
- Se documenta el linaje de cada campo en el diccionario de datos.  
- La app Streamlit debe permitir rastrear un KPI hasta sus datos de origen.

---

## Validaciones Mínimas
- Tipos de datos correctos (`date`, `string`, `float`).  
- Fechas en formato **ISO 8601** (`YYYY-MM-DD`).  
- Campos `amount` no nulos y con valores numéricos válidos.  
- Eliminación de duplicados exactos.  
- Reglas específicas según dataset documentadas en `docs/diccionario.md`.

---

## Política de Mínimos Privilegios
- Los datasets en **raw** solo son accesibles por el rol **Data Engineer**.  
- Las capas **bronze** y **silver** son accesibles para **Data Analyst**.  
- La capa **gold** (KPIs) es accesible a **Business Users**.  
- Cada usuario/rol tiene permisos únicamente sobre las carpetas y operaciones necesarias.  

---

## Trazabilidad
- Cada dataset transformado debe incluir un **registro de origen** (archivo fuente, fecha de carga).  
- Se generan **logs de validación y transformación** para auditar el proceso.  
- Los KPIs en la app Streamlit deben indicar la última fecha de actualización.

---

## Roles
| Rol            | Responsabilidades                                                       |
|----------------|-------------------------------------------------------------------------|
| Data Engineer  | Ingesta, validación, normalización, mantenimiento de pipelines.         |
| Data Analyst   | Exploración de datos en bronze/silver, creación de consultas y métricas.|
| Business User  | Consumo de KPIs y visualizaciones desde la app.                         |
| Data Steward   | Garantizar calidad de datos, actualización del diccionario y gobernanza.|


# ✅ Checklist de validación del laboratorio

- [ ] **URL de Streamlit** funcional y accesible públicamente.
- [ ] **bronze.csv** generado y subido a `/data/bronze/`.
- [ ] **silver.csv** generado y subido a `/data/silver/`.
- [ ] **README.md** incluye decisiones justificadas basadas en las **5V de Big Data** (Volumen, Velocidad, Variedad, Veracidad, Valor).
- [ ] Capturas de pantalla del despliegue y ejecución agregadas en `docs/`.
- [ ] **Diccionario de datos** (`docs/diccionario.md`) completo y actualizado con mapeos origen → canónico.
- [ ] **Gobernanza de datos** (`docs/gobernanza.md`) redactada con linaje, validaciones mínimas, mínimos privilegios, trazabilidad y roles.

# 📊 Rúbrica de Evaluación (10 puntos)

| Criterio                     | Puntos | Descripción                                                                 |
|------------------------------|--------|-----------------------------------------------------------------------------|
| **Diseño y justificación**   | 3      | Claridad en arquitectura, modelo de datos y decisiones (incluyendo 5V).     |
| **Calidad de datos**         | 3      | Grado de limpieza, normalización y validaciones correctas en bronze/silver. |
| **Trazabilidad y DW**        | 2      | Evidencia de linaje, separación bronze/silver y conexión KPI ↔ fuentes.     |
| **Documentación**            | 2      | README completo, diccionario y gobernanza claros, capturas en `docs/`.      |
| **Total**                    | 10     |                                                                             |

## 📝 Prompts de reflexión

Responde brevemente a cada punto (3–5 líneas por ítem):

1. **V dominante hoy y V dominante si 2× tráfico**  
   _Respuesta: …_

2. **Trade-off elegido (ej.: más compresión vs CPU)**  
   - ¿Cuál fue la decisión?  
   - ¿Por qué la elegiste?  
   - ¿Cómo la medirás (métrica, experimento)?  
   _Respuesta: …_

3. **Por qué “inmutable + linaje” mejora veracidad y qué coste añade**  
   _Respuesta: …_

4. **KPI principal y SLA del dashboard**  
   - ¿Qué KPI es el más relevante?  
   - ¿Qué decisión de negocio habilita?  
   - ¿Por qué definiste ese SLA/latencia?  
   _Respuesta: …_

5. **Riesgo principal del diseño y mitigación técnica concreta**  
   _Respuesta: …_
## 🚀 Pega y corre

Sigue estos pasos mínimos en orden para completar y entregar el laboratorio:

1. **Crear repo con estructura**  
   - Tiempo: ~15 min  
   - Acción: en GitHub, crea `bigdata-storage-lab-<apellido>` con las carpetas/archivos de la estructura base (`src/`, `docs/`, `tests/`, `data/`).  
   - Check: estructura visible en la raíz, `.gitkeep` en carpetas vacías.

2. **Pegar archivos base**  
   - Tiempo: ~30 min  
   - Acción: copia el contenido de `requirements.txt`, `streamlit_app.py`, `src/*.py`, `docs/*.md`, `tests/checklist.md`.  
   - Check: no hay errores de sintaxis al abrir cada archivo; dependencias correctas en `requirements.txt`.

3. **Subir CSV de prueba**  
   - Tiempo: ~15 min  
   - Acción: carga `ventas_mes.csv`, `sales_may.csv`, `partners_jun.csv` en la app.  
   - Check: se genera **bronze** unificado y **silver** si las validaciones pasan.

4. **Desplegar en Streamlit Community Cloud**  
   - Tiempo: ~20 min  
   - Acción: conecta el repo, selecciona `streamlit_app.py` como main file, despliega.  
   - Check: URL pública funciona, se pueden subir CSV y descargar bronze/silver.

5. **Completar README con reflexiones**  
   - Tiempo: ~20 min  
   - Acción: responde a los **Prompts de reflexión** (5 preguntas), añade decisiones justificadas (5V) y capturas en `docs/`.  
   - Check: README tiene secciones completas y autoexplicativas.

6. **Entregar URLs**  
   - Tiempo: ~5 min  
   - Acción: comparte:  
     - URL del repo GitHub (público)  
     - URL de la app en Streamlit  
   - Check: ambos enlaces funcionan y permiten reproducir el trabajo.

---

### ✅ Antes de entregar, comprueba:
- [ ] **URL de Streamlit** accesible y funcional.  
- [ ] **bronze.csv** y **silver.csv** descargables y con esquema correcto (`date, partner, amount`).  
- [ ] **README.md** incluye decisiones (5V), reflexiones respondidas y capturas.  
- [ ] **docs/** contiene `diccionario.md`, `gobernanza.md`, capturas y tablas de estrategia.  
- [ ] **tests/checklist.md** marcado según cumplimiento.  
