import os
import glob
import shutil

# Lista de carpetas originales con tus variables
variables = ["CTI", "RGB", "TUR", "CCU", "CWS", "TSM", "AOT", "KDB", "SDD", "SLP"]

# Carpeta donde se guardarán los datos de prueba
root_out = "prueba"

os.makedirs(root_out, exist_ok=True)

for var in variables:
    src_dir = var  # carpeta original (ej: TUR/)
    dst_dir = os.path.join(root_out, var)  # prueba/TUR/

    if not os.path.exists(src_dir):
        print(f"⚠ La carpeta {src_dir} no existe, se omite.")
        continue

    # Crear carpeta de salida
    os.makedirs(dst_dir, exist_ok=True)

    # Tomar 15 archivos (de cualquier tipo)
    files = sorted(
        glob.glob(os.path.join(src_dir, "*"))
    )

    # Filtrar para evitar carpetas vacías
    if len(files) == 0:
        print(f"⚠ No hay archivos dentro de {src_dir}")
        continue

    # Seleccionar los primeros 15
    sample = files[:15]

    print(f"📁 Copiando 15 archivos de {var} → {dst_dir}")

    # Copiar archivos
    for f in sample:
        shutil.copy(f, dst_dir)

print("✔ Proceso completado.")

