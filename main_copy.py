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

#--------------------------conexion html con el chatbot----------------------------
from pydantic import BaseModel #Se usa para definir la estructura de los datos que el cliente (el frontend) enviará a la API.
from fastapi.middleware.cors import CORSMiddleware

from prediction import predecir_diabetes # Nos ayuda a encontrar sinonimos de palabras. 
import conexionAutHtml # Importamos el archivo `conexionAutHtml.py`


if __name__ == "__main__":
    conexionAutHtml.start_server()

#nltk.data.path.append('C:/Users/Usuario/AppData/Local/Programs/Python/Python312/Lib/site-packages/nltk') #Yenifer
nltk.data.path.append('C:/Users/ASUS/AppData/Local/Programs/Python/Python312/Lib/site-packages/nltk') #Jessica


#--------------------------------conexio html con el chatbot-----------------------------------------------
# Creamos la aplicación FastAPI, que será el motor de nuestra API
# Esto inicializa la API con un nombre y una versión
app = FastAPI()

#permitimos peticiones desde la pagina web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #["http://localhost:5000"], aqui se puede poner la url de la web
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#----------------------------------conexión con el chatbot-------------------------------------------
#Creamos la ruta para el chatbot
#Indica que esta función responderá a las solicitudes POST en la ruta /chatbot.
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