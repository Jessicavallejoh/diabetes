import requests
import json

def process_report (gender, age, hypertension, heart_disease, smoking, peso, altura, bmi, hba1c_input, glucose_input):
    url = "http://127.0.0.1:11434/api/chat"
    payload = {
        "model": "llama3.2",
        "messages": [
            { "role": "assistant", "content": "Eres un experto en salud especializado en diabetes, tu función es recomendar medicina alternativa basandote en las caracteristicas especificas del paciente a personas que aún no tienen diabetes pero que talvez podrían tener riesgo de acuerdo a sus caracteristicas: Genero, edad, tiene hipertensión?(0=No, 1=Si), sufre del corazón?(0=No, 1=Si), frecuencia con la que fuma(0= nunca, 1= ocasional, 2= muy frecuente), peso, altura, indice de masa corporal, nivel de HbA1c y Nivel de glucosa en sangre. La medicina alternativa debe estar basada en: medicina herbaria (Es importante mencionar la medicina herbaria especificamente que debería tomar, como se prepara, como se toma y con que frecuencia), ejercicios (solo si aplica, indica detalladamente que tipo de deportes o ejercicios debería realizar, con repeticiones, intensidad y duración), dieta detallada (Es importante mencionar detalladamente recetas que debe seguir semanalmente, especificando los alimentos y cantidades). El reporte debe ser dirigido directamente al paciente y recalcar la importancia de complementar esto con su medicina tradicional, no abandonarla. Evita repetir la información del paciente. Guiate esgtrictamente por el ejemplo proporcionado."},
            { "role": "user", "content": f"Genero: {gender}, Edad: {age}, Hipertension: {hypertension}, Problemas cardiacos: {heart_disease}, Fumador: {smoking}, Peso: {peso}kg, Estatura: {altura}m, Indice masa corporal: {bmi}, HbA1c: {hba1c_input}, Glucosa: {glucose_input}" }
        ],
    }

    # Hacer la solicitud con streaming activado
    response = requests.post(url, json=payload, stream=True)

    # Variable para almacenar la respuesta completa
    full_response = ""

    # Recorrer cada línea del streaming
    for line in response.iter_lines():
        if line:
            try:
                # Convertir la línea JSON a un diccionario de Python
                json_data = json.loads(line.decode('utf-8'))  # Aquí se usa json.loads() correctamente
                # Concatenar el contenido del mensaje
                full_response += json_data["message"]["content"]
            except Exception as e:
                print(f"Error al procesar línea: {e}")

    # Imprimir la respuesta completa
    print(full_response)
    
    return full_response
