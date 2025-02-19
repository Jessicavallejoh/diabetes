"""
Imagina que esta API es una herramienta para la prediccion de diabetes:
La función load_diabetes() cargar caracteristicas de diabetes desde un archivo CSV.
La función get_diabetes() muestra todo el catálogo cuando alguien lo pide.
La función get_diabetes(id) muestra el id de diabetes que se ha pedido.
La función chatbot (query) es un asistente que responde a preguntas sobre diabetes.
La función get_diabetes_by_category (cagory) ayuda a encontrar películas según su género (acción, comedia, etc.).
"""
#LO HIZO JESSICA
### USAR ESTE COMANDO PARA CORRER EL CODIGO  uvicorn nombre_del_archivo:app --reload --port 9000 --log-level debug


# Importamos las herramientas necesarias para contruir nuestra API
from typing import Optional
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse para páginas web, JSONResponse para respuestas en formato JSON. 
import pandas as pd # Pandas nos ayuda a manejar datos en tablasm como si fuera un Excel.
import nltk # NLTK es una librería para procesar texto y analizar palabras. 
from nltk.tokenize import word_tokenize # Se usa para dividir un texto en palabras individuales.
from nltk.corpus import wordnet

from prediction import predecir_diabetes # Nos ayuda a encontrar sinonimos de palabras. 

#import nltk
#print(nltk.__file__)

#nltk.data.path.append('C:/Users/Usuario/AppData/Local/Programs/Python/Python312/Lib/site-packages/nltk') #Yenifer
nltk.data.path.append('C:/Users/ASUS/AppData/Local/Programs/Python/Python312/Lib/site-packages/nltk') #Jessica


# Descargamos las herramientas necesarias de NLTK para el análisis de palabras.

nltk.download('punkt') # Paquete para dividir frases en palabras.
nltk.download('punkt_tab') # Paquete para dividir frases en palabras.  
nltk.download('wordnet') # Paquete para encontrar sinonimos de palabras en inglés.

# Función para cargar las películas desde un archivo CSV

def load_diabetes():
    # Leemos el archivo que contiene información de diabetes y seleccionamps las columnas más importantes
    df = pd.read_csv("Dataset/prediccion_diabetes_copy.csv")[['ID', 'gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']]
    
    # Renombramos las columnas para que sean más faciles de entender
    df.columns = ['id', 'gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']
    
     # Llenamos los espacios vacíos con texto vacío y convertimos los datos en una lista de diccionarios 
    return df.fillna('').to_dict(orient='records')

    #cargamos las caracteristicas de diabetes al iniciar la API para no leer el archivo cada vez que se haga una petición.
diabetes_list = load_diabetes()

# Función para encontrar sinónimos de una palabra

def get_synonyms(word): 
    # Usamos WordNet para obtener distintas palabras que significan lo mismo.
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# Creamos la aplicación FastAPI, que será el motor de nuestra API
# Esto inicializa la API con un nombre y una versión
app = FastAPI(title="Mi aplicación de predición de diabetes", version="1.0.0")

   
# Ruta de inicio: Cuando alguien entra a la API sin especificar nada, verá un mensaje de bienvenida.

@app.get('/', tags=['Home'])
def home():
# Cuando entremos en el navegador a http://127.0.0.1:8000/ veremos un mensaje de bienvenida
    return HTMLResponse('<h1>Vamos a predecir si tienes diabetes</h1>')

# Obteniendo la lista de caracteristicas de diabetes
# Creamos una ruta para obtener todas las caracteristicas de diabetes disponibles

# Ruta para obtener todas las personas con diabetes disponible
@app.get('/diabetes', tags=['Diabetes'])
def get_diabetes():
    
    #si hay algun caso de diabetes, lo mostramos, sino mostramos un mensaje de error
    return diabetes_list or HTTPException(status_code=500, detail="No hay datos de diabetes")

# Ruta para obtener una caracteristica específica según su ID
@app.get('/diabetes/{id}', tags=['Diabetes'])
def get_diabetes(id: int):
    # Buscamos en la lista de diabetes la que tenga el mismo ID
    return next((m for m in diabetes_list if m['id'] == id), {"detalle": "Caso no encontrado"})

# Ruta del chatbot que responde con caracteísticas de diabetes según palabras clave de la categoría

@app.get('/chatbot', tags=['Chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intención del usuario
    query_words = word_tokenize(query.lower())
    
     # Buscamos sinónimos de las palabras clave para ampliar la búsqueda
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)
    
    # Filtramos la lista de películas buscando coincidencias en la categoría
    results = [m for m in diabetes_list if any (s in m['smoking_history'].lower() for s in synonyms)]
    
    #si hay algun caso de diabetes, lo mostramos, sino mostramos un mensaje de error
    return JSONResponse (content={
        "respuesta": "Aquí tienes los datos relacionados a tu consulta: " if results else "No encontré predicciones de diabetes relacionados.",
        "diabetes": results
    })
    
# Ruta para buscar datos de diabetes por genero
@app.get ('/diabetes/by_gender/', tags=['Diabetes'])
def get_diabetes_by_gener(gender: str):
    # Filtramos la lista de películas según la categoría ingresada
    return [m for m in diabetes_list if gender.lower() == m['gender'].lower()]

@app.post('/predict_diabetes', tags=['Diabetes'])
def predict_diabetes(gender: str, age: int, hypertension: int, heart_disease: int, smoking_history: str, peso: float, altura:  float, HbA1c_input: Optional[str]="", glucose_input: Optional[str]=""):
    prediction = predecir_diabetes(gender, age, hypertension, heart_disease, smoking_history, peso, altura, HbA1c_input, glucose_input)
    return prediction

