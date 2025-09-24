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

