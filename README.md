# Pre-entrega · Adquisición y Normalización con Pandas

**Curso:** Data Science II — Coderhouse

Integración de datos de ventas provenientes de **dos fuentes de formato distinto**
(un CSV de transacciones y un Excel con el maestro de productos), con limpieza,
unión por `id_producto`, cálculo de una columna derivada y exportación a Parquet.

## Objetivo

Simular un escenario real en el que los datos llegan de distintos departamentos en
formatos diferentes y deben consolidarse en un único dataset limpio y listo para análisis.

## Estructura del repositorio

```
preentrega2-adquisicion-pandas/
├── data/
│   ├── raw/
│   │   ├── transacciones.csv            # fuente 1: ventas (id_producto, cantidad, fecha)
│   │   └── maestro_productos.xlsx       # fuente 2: catálogo (id_producto, nombre, precio)
│   └── processed/
│       └── ventas_consolidadas.parquet  # salida final
├── src/
│   ├── etl_adquisicion.ipynb            # notebook principal (el proceso completo)
│   └── generar_fuentes.py               # genera los archivos de ejemplo de data/raw
├── requirements.txt
├── .gitignore
└── README.md
```

## Flujo del ETL (`src/etl_adquisicion.ipynb`)

1. **Adquisición** — carga del CSV (`pd.read_csv`) y del Excel (`pd.read_excel`, motor `openpyxl`).
2. **Tipos de datos** — `fecha` → `datetime`; la llave `id_producto` se unifica a `str` en
   ambas fuentes (en origen venía como entero en el CSV y como texto en el Excel).
3. **Nulos** — se eliminan las transacciones con `cantidad` o `fecha` nulas (en datos
   transaccionales imputar una cantidad equivaldría a inventar una venta).
4. **Merge** — unión por `id_producto` (`how="left"` con `indicator`) para auditar y
   descartar las ventas cuyo producto no existe en el maestro.
5. **Columna calculada** — `total_venta = cantidad * precio_unitario`.
6. **Validación** — se verifica la ausencia de nulos en campos críticos.
7. **Exportación** — a `data/processed/ventas_consolidadas.parquet`.

## Cómo reproducirlo

Requiere Python 3.10+.

```bash
# 1. (opcional) entorno virtual
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate

# 2. dependencias
pip install -r requirements.txt

# 3. (opcional) regenerar los archivos fuente de ejemplo
cd src
python generar_fuentes.py       # vuelve a crear data/raw/

# 4. ejecutar el proceso
jupyter notebook etl_adquisicion.ipynb
#   o, sin abrir Jupyter:
jupyter nbconvert --to notebook --execute --inplace etl_adquisicion.ipynb
```

La ejecución deja el archivo final en `data/processed/ventas_consolidadas.parquet`.

## Librerías utilizadas

| Librería  | Uso                                             |
|-----------|-------------------------------------------------|
| pandas    | carga, limpieza, merge y transformación         |
| openpyxl  | motor de lectura del archivo `.xlsx`            |
| pyarrow   | escritura y lectura del formato Parquet         |
| jupyter   | ejecución del notebook                          |

## Notas de diseño

- La llave `id_producto` se normaliza a **string** (no a entero) por robustez: soporta
  SKUs alfanuméricos y ceros a la izquierda, y evita el error típico de hacer *merge* con
  tipos distintos entre fuentes.
- Se eligió **Parquet** sobre CSV para la salida porque es columnar, comprimido y preserva
  los tipos de datos (incluido `datetime`).
