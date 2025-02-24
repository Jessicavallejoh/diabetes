import pandas as pd  # Importar pandas para manejo de datos
import numpy as np  # Importar numpy para operaciones numéricas
from sklearn.model_selection import train_test_split  # Importar para dividir datos
from sklearn.ensemble import RandomForestClassifier  # Importar clasificador Random Forest
from sklearn.preprocessing import LabelEncoder  # Importar para codificar etiquetas
from sklearn.metrics import accuracy_score

from ollama import process_report  # Importar para calcular precisión

# Cargar dataset
df = pd.read_csv("./Dataset/prediccion_diabetes.csv")  # Leer archivo CSV

# Preprocesamiento
df['gender'] = LabelEncoder().fit_transform(df['gender'])  # Codificar columna 'gender'
df['smoking_history'] = LabelEncoder().fit_transform(df['smoking_history'])  # Codificar columna 'smoking_history'

# Separar variables
X = df.drop(columns=['ID', 'diabetes'])  # Variables independientes (no tiene en cuenta ID y diabetes)
y = df['diabetes']  # Variable dependiente

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Dividir en entrenamiento y prueba

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)  # Crear modelo Random Forest
model.fit(X_train, y_train)  # Entrenar modelo

# Evaluación
y_pred = model.predict(X_test)  # Predecir con datos de prueba
print(f"Precisión del modelo: {accuracy_score(y_test, y_pred):.2f}")  # Imprimir precisión

# Función para pedir datos al usuario y predecir
def predecir_diabetes(gender, age, hypertension, heart_disease, smoking, peso, altura, hba1c_input, glucose_input):
    # Pedir datos al usuario
    bmi = peso / (altura ** 2)  # Calcular BMI
    print("BMI:", type(peso), type(altura), bmi, type(hba1c_input), hba1c_input)  # Debugging
    # Codificar valores categóricos
    gender = 1 if gender == "female" else 0
    smoking_dict = {"never": 0, "former": 1, "current": 2}
    smoking = smoking_dict.get(smoking, 0) #si no esta ninguno de los anteriores entonces dejar cero

    # Crear diccionario de entrada
    datos_usuario = {
        "gender": gender,
        "age": age,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "smoking_history": smoking,
        "bmi": bmi
    }

    # Agregar HbA1c y glucosa solo si el usuario los ingresó
    if hba1c_input:
        datos_usuario["HbA1c_level"] = float(hba1c_input)
    if glucose_input:
        datos_usuario["blood_glucose_level"] = float(glucose_input)

    # Convertir a DataFrame y alinear columnas con el modelo
    df_usuario = pd.DataFrame([datos_usuario])

    # Asegurar que tiene las mismas columnas que el modelo (llenar con media si faltan)
    for col in X.columns:
        if col not in df_usuario:
            df_usuario[col] = X[col].mean()  # Usar media de entrenamiento como valor por defecto

    # Hacer predicción con probabilidad
    probabilidad = model.predict_proba(df_usuario)[0][1]  # Probabilidad de tener diabetes
    
    report= process_report(gender, age, hypertension, heart_disease, smoking, peso, altura, bmi, hba1c_input, glucose_input)
    
    print(f"Probabilidad estimada: {probabilidad * 100:.2f}%")
    
    if probabilidad > 0.5:
        print("¡Tienes un alto riesgo de tener diabetes, hazte examenes!")
    else:
        print("No tienes un alto riesgo de tener diabetes.")
        
    puntaje = f"Probabilidad estimada: {probabilidad * 100}% \n{report}" 
        
   # return puntaje, report 
   
    return puntaje 


