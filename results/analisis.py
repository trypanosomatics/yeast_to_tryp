import pandas as pd

# Cargar archivos
df_manual = pd.read_csv("manual_curation.csv")
df_results = pd.read_csv("gdi_results.csv")
df_not_selected = pd.read_csv("gdi_not_selected_data.csv")

# Crear columna in_results: 1 si está en resultados, 0 si no
df_manual["in_results"] = df_manual["inchiKey"].isin(df_results["inchiKey"]).astype(int)

# Crear diccionario de motivos de eliminación
motivos_dict = df_not_selected.set_index("inchiKey")["Filter Name"].to_dict()

# Crear columna de motivos: si está en resultados, queda vacío; si no, se busca el motivo
df_manual["elimination_reason"] = df_manual.apply(
    lambda row: "" if row["in_results"] == 1 else motivos_dict.get(row["inchiKey"], "No encontrado"),
    axis=1
)

# Guardar resultado
df_manual.to_csv("manual_curation_con_info.csv", index=False)

