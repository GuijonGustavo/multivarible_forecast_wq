import os
import zipfile
import re

# Lista de archivos ZIP (puedes dejarlo así, o usar os.listdir)
zip_files = [
    "cms-fad1728b-22d6-4c54-9e31-f0388dda7c8d_CTI_1.zip",
    "a80cadf0-09b4-41a4-a6a9-0343ac1368f3_rgb_1.zip",
    "23fb456c-5c7d-4bfc-864e-cb7d4870bb2d_tur_1.zip",
    "cms-0cbb62cf-6d61-4420-ad01-bdcb8491be7f_CCU_1.zip",
    "cms-69fe215b-9aa5-4d43-8caf-831ac6670027_CWS_1.zip",
    "c93cdd4f-e40a-41ab-b2c3-fc560b12ee13_tsm_1.zip",
    "80191006-f9a4-42e3-992b-7505e02101de_aot_1.zip",
    "b3734332-f05f-4d6e-a621-3bc013cc8f1b_kdb_1.zip",
    "b2e06436-d867-471a-9cbb-0fd9690cbe7f_sdd_1.zip",
    "fcc05b7b-37a9-4489-ae46-2b6cfb8cf4a4_slp_1.zip"
]


# Función para extraer el nombre de la variable (TUR, TSM, etc.)
def extract_variable_name(filename):
    """
    Busca algo tipo _TSM_ o _tsm_ y saca la variable.
    """
    pattern = r"_(\w+?)_"
    match = re.search(pattern, filename)
    if match:
        return match.group(1).upper()
    return None


# Crear carpetas y descomprimir
for zip_file in zip_files:
    var = extract_variable_name(zip_file)

    if var is None:
        print(f"No se detectó variable en: {zip_file}")
        continue

    # Crear carpeta si no existe
    out_dir = f"./{var}"
    os.makedirs(out_dir, exist_ok=True)

    print(f"Descomprimiendo {zip_file} → {out_dir}")

    # Descomprimir
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(out_dir)

print("✔ Completado.")

