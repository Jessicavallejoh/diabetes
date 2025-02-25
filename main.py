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
from fastapi import FastAPI, HTTPException, Request # FastAPI nos ayuda a crear la API, HTTPException maneja errores.
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse para páginas web, JSONResponse para respuestas en formato JSON. 
import pandas as pd # Pandas nos ayuda a manejar datos en tablasm como si fuera un Excel.
import nltk # NLTK es una librería para procesar texto y analizar palabras. 
from nltk.tokenize import word_tokenize # Se usa para dividir un texto en palabras individuales.
from nltk.corpus import wordnet

#--------------------------------conexion html con el chatbot-----------------------------------------------
from pydantic import BaseModel #Se usa para definir la estructura de los datos que el cliente (el frontend) enviará a la API.
from fastapi.middleware.cors import CORSMiddleware
#-----------------------------------------------------------------------------------------------------------
from prediction import predecir_diabetes # Nos ayuda a encontrar sinonimos de palabras. 
import conexionAutHtml # Importamos el archivo `conexionAutHtml.py` nos permite abrir de manera automatica la pagina web con el comando python main.py

#iniciamos el servidor del archivo `conexionAutHtml.py`
if __name__ == "__main__":
    conexionAutHtml.start_server()
    
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

#--------------------------------conexion html con el chatbot-----------------------------------------------
#permitimos peticiones desde la pagina web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #["http://localhost:5000"], aqui se puede poner la url de la web
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#-----------------------------------------------------------------------------------------------------------
   
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


@app.get ('/diabetes/by_age/', tags=['Diabetes'])
def get_diabetes_by_age(age: int):
    # Filtramos la lista de diabetes según la categoría de edad
    return [m for m in diabetes_list if age == m['age']]

@app.get ('/diabetes/by_hypertension/', tags=['Diabetes'])
def get_diabetes_by_hypertension(hypertension: int):
    # Filtramos la lista de diabetes según la categoría hypertension
    return [m for m in diabetes_list if hypertension == m['hypertension']]

@app.get ('/diabetes/by_heart_disease/', tags=['Diabetes'])
def get_diabetes_by_heart_disease(heart_disease: int):
    # Filtramos la lista de diabetes según la categoría hypertension
    return [m for m in diabetes_list if heart_disease == m['heart_disease']]

@app.get ('/diabetes/by_smoking_history/', tags=['Diabetes'])
def get_diabetes_by_smoking_history(smoking_history: str):
    # Filtramos la lista de diabetes según la categoría genero
    return [m for m in diabetes_list if smoking_history.lower() == m['smoking_history'].lower()]

@app.get ('/diabetes/by_bmi/', tags=['Diabetes'])
def get_diabetes_by_bmi(bmi: float):
    # Filtramos la lista de diabetes según la categoría de edad
    return [m for m in diabetes_list if bmi == m['bmi']]

@app.get ('/diabetes/by_HbA1c_level/', tags=['Diabetes'])
def get_diabetes_by_HbA1c_level(HbA1c_level: float):
    # Filtramos la lista de diabetes según la categoría de edad
    return [m for m in diabetes_list if HbA1c_level == m['HbA1c_level']]

@app.get ('/diabetes/by_blood_glucose_level/', tags=['Diabetes'])
def get_diabetes_by_blood_glucose_level(blood_glucose_level: float):
    # Filtramos la lista de diabetes según la categoría de edad
    return [m for m in diabetes_list if blood_glucose_level == m['blood_glucose_level']]

@app.get ('/diabetes/by_diabetes/', tags=['Diabetes'])
def get_diabetes_by_heart_diabetes(diabetes: int):
    # Filtramos la lista de diabetes según la categoría hypertension
    return [m for m in diabetes_list if diabetes == m['diabetes']]

@app.post('/predict_diabetes', tags=['Diabetes'])
def predict_diabetes(gender: str, age: int, hypertension: int, heart_disease: int, smoking_history: str, peso: float, altura:  float, HbA1c_input: Optional[str]="", glucose_input: Optional[str]=""):
    prediction = predecir_diabetes(gender, age, hypertension, heart_disease, smoking_history, peso, altura, HbA1c_input, glucose_input)
    return prediction

#----------------------------------conexión con el chatbot-------------------------------------------
#Creamos la ruta para el chatbot
#Indica que esta función responderá a las solicitudes POST en la ruta /formulario
@app.post("/formulario")

#async: Permite manejar peticiones de forma asíncrona para mejorar el rendimiento.
#user_message: UserMessage: FastAPI espera que el cuerpo de la solicitud tenga un JSON con los datos definidos en ChatRequest.
async def recibir_respuestas(request: Request):
    datos = await request.json()
        
    respuestas = datos.get("respuestas",[])  #  Extrae la lista de respuestas
    print("Respuestas recibidas:", respuestas)  # Debugging
    
    # Validación de los datos
    try:
        # Extrae valores en el orden correcto
        # # Extraer el nombre del usuario (Suponiendo que es la primera respuesta)
        user_name = respuestas[0] if respuestas and isinstance(respuestas[0], str) else "Usuario" # Nombre
        gender = respuestas[1]  # Género (Male / Female)
        age = int(respuestas[2])  # Edad
        hypertension = int(respuestas[3])  # Hipertensión (0 o 1)
        heart_disease = int(respuestas[4])  # Enfermedad cardiovascular (0 o 1)
        smoking_history = respuestas[5]  # Historial de fumar
        peso = float(respuestas[6])  # Peso en kg
        altura = float(respuestas[7]) / 100  # Altura en metros (convierte cm a m)
        
        # Algunos valores pueden ser vacíos, validar antes de convertir
        hbA1c_input = float(respuestas[8]) if respuestas[8] else None
        glucose_input = float(respuestas[9]) if respuestas[9] else None

        # Llamado a la función de predicción
        prediction = predecir_diabetes(gender, age, hypertension, heart_disease, smoking_history, peso, altura, hbA1c_input, glucose_input)

        # Mensaje personalizado
        mensaje = f"Gracias por responder, hemos registrado tus respuestas.<br><br> 🔹{user_name}, tu {prediction}  \n"
        
        #Devuelve una respuesta en formato JSON.
        return {"reply": mensaje} 
    except Exception as e:
        print("Error en el servidor:", str(e))  #  Esto imprimirá el error en la terminal
        return {"error": "Ocurrió un error al procesar los datos."}
