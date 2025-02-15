import pandas as pd

# Cargar el CSV
df = pd.read_csv("Dataset/diabetes_prediction_dataset.csv")

# Agregar una columna de ID (comenzando desde 1)
df.insert(0, "ID", range(1, len(df) + 1))

# Guardar el CSV con la nueva columna
df.to_csv("tu_archivo_con_id.csv", index=False)

print("¡Columna de ID agregada y archivo guardado!")
