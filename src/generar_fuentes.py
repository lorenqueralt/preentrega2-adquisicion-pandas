"""
generar_fuentes.py
-------------------
Genera los archivos fuente de ejemplo para la pre-entrega:
  - data/raw/transacciones.csv        (ventas: id_producto, cantidad, fecha)
  - data/raw/maestro_productos.xlsx   (catalogo: id_producto, nombre_producto, precio_unitario)

Se introducen a proposito dos problemas de calidad tipicos del enunciado:
  1) Valores nulos en 'cantidad' y en 'fecha' dentro del CSV.
  2) 'id_producto' con TIPOS DISTINTOS entre fuentes:
        - CSV  -> entero (101, 102, ...)
        - Excel-> texto  ("101", "102", ...)
     Esto fuerza a normalizar la llave antes del merge.
Ademas se incluye una transaccion con un id_producto inexistente en el maestro,
para mostrar el manejo de filas que no matchean en el merge.

Este script es solo para reproducir los datos de ejemplo; no es parte del ETL.
"""
import pandas as pd

# --- Maestro de productos (se guardara como Excel) ---
maestro = pd.DataFrame({
    # ID como TEXTO a proposito (en Excel quedaran como string)
    "id_producto":      ["101", "102", "103", "104", "105"],
    "nombre_producto":  ["Teclado mecanico", "Mouse inalambrico", "Monitor 24\"",
                         "Auriculares USB", "Webcam HD"],
    "precio_unitario":  [25999.90, 12500.00, 89990.50, 18750.00, 15400.75],
})

# --- Transacciones (se guardara como CSV) ---
transacciones = pd.DataFrame({
    # ID como ENTERO a proposito (en CSV quedaran como int64)
    "id_producto": [101, 102, 103, 101, 104, 105, 102, 103, 104, 101, 105, 999],
    "cantidad":    [2,   1,   None, 3,   1,   None, 4,   2,   1,   5,   2,   1],
    "fecha": [
        "2024-03-01", "2024-03-01", "2024-03-02", "2024-03-03",
        "2024-03-03", "2024-03-04", "2024-03-05", None,
        "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09",
    ],
})

if __name__ == "__main__":
    transacciones.to_csv("data/raw/transacciones.csv", index=False)
    maestro.to_excel("data/raw/maestro_productos.xlsx", index=False, engine="openpyxl")
    print("OK: fuentes generadas en data/raw/")
    print(transacciones.dtypes)
    print(maestro.dtypes)
