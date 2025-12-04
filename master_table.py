#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Genera la tabla maestra a partir de múltiples carpetas que contienen archivos .tif.
Cada archivo debe corresponder a un indicador (AOT, CCU, CTI, etc.).
Se extrae la fecha desde el nombre del archivo y se calcula el promedio del raster.
"""

import os
import glob
import rasterio
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------------

CODES = ["AOT", "CCU", "CTI", "CWS", "KDB", "RGB", "SDD", "SLP", "TSM", "TUR"]

BASE_DIR = "data"                    # <--- ajusta si tu ruta es otra
OUTPUT_FILE = "master_table.csv"


# ---------------------------------------------------------------------
# EXTRAER FECHA DESDE NOMBRE (MUY FLEXIBLE)
# ---------------------------------------------------------------------

def extract_date_from_filename(filename):
    """
    Busca patrones YYYYMMDD dentro del nombre del archivo.
    Ejemplo:
        MODIS_AOT_20200115.tif → 2020-01-15
    """
    import re
    match = re.search(r"(20\d{6})", filename)
    if match:
        date_raw = match.group(1)
        return f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:]}"
    return None


# ---------------------------------------------------------------------
# LEER TIFF Y CALCULAR LA MEDIA
# ---------------------------------------------------------------------

def raster_mean(path):
    with rasterio.open(path) as src:
        arr = src.read(1).astype("float32")
        arr = np.where(arr == src.nodata, np.nan, arr)
        return np.nanmean(arr)


# ---------------------------------------------------------------------
# LEER TODAS LAS CARPETAS
# ---------------------------------------------------------------------

def load_all_data():
    records = []

    print("Leyendo carpetas...\n")

    for code in CODES:
        folder = os.path.join(BASE_DIR, code)

        if not os.path.isdir(folder):
            print(f"⚠️ Carpeta no encontrada: {folder}")
            continue

        tif_files = sorted(glob.glob(os.path.join(folder, "*.tif")))

        if not tif_files:
            print(f"⚠️ No hay .tif en {folder}")
            continue

        print(f"📂 {code}: {len(tif_files)} archivos TIFF")

        for f in tif_files:
            date = extract_date_from_filename(os.path.basename(f))
            if date is None:
                print(f"   ⚠️ No se pudo extraer fecha: {f}")
                continue

            try:
                mean_value = raster_mean(f)
                records.append((date, code, mean_value))
            except Exception as e:
                print(f"   ❌ Error leyendo {f}: {e}")

    if not records:
        raise RuntimeError("No se extrajo ningún dato desde los TIFF.")

    df = pd.DataFrame(records, columns=["date", "code", "value"])

    print("\n✓ Datos cargados:", len(df), "registros\n")
    return df


# ---------------------------------------------------------------------
# RESOLVER DUPLICADOS
# ---------------------------------------------------------------------

def fix_duplicates(df):
    dups = df[df.duplicated(subset=["date", "code"], keep=False)]
    if dups.empty:
        return df

    print(f"⚠️ Duplicados detectados: {len(dups)} — Promediando...\n")

    df_clean = (
        df.groupby(["date", "code"], as_index=False)
        .agg({"value": "mean"})
    )
    return df_clean


# ---------------------------------------------------------------------
# PIVOT FINAL
# ---------------------------------------------------------------------

def build_master_table(df):
    master = df.pivot(index="date", columns="code", values="value")
    master = master.sort_index()
    return master


# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== GENERANDO TABLA MAESTRA DESDE TIFF ===\n")

    df = load_all_data()
    df = fix_duplicates(df)
    master = build_master_table(df)

    master.to_csv(OUTPUT_FILE)

    print(f"✓ Listo: {OUTPUT_FILE}\n")
    print("=== FIN ===\n")

