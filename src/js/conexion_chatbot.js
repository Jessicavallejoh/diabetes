//----------------------------------------------------------------------------------------
//window.sendMessage = async function() {:  Función para enviar el mensaje de la pagina al backend
//Define una función asíncrona llamada 'sendMessage' y la asigna al objeto window, lo que permite llamarla 
// desde un botón en el HTML.
//async: permite usar await dentro de la función para manejar la respuesta del servidor sin bloquear la ejecución.

/*window.sendMessage = async function() {

    //Obtenemos los valores del formulario
    let userName = document.getElementById("userName").value; //Obtiene el valor del campo de entrada donde el usuario escribe su nombre.
    let message = document.getElementById("userMessage").value; //Obtiene el mensaje escrito por el usuario.

    //Obtenemos los valores del formulario de diabetes
    let userGender = document.getElementById("userGender").value;
    let userAge = document.getElementById("userAge").value;
    let userHypertension = document.getElementById("userHypertension").value;
    let userHeartDisease = document.getElementById("userHeartDisease").value;
    let userSmokingHistory = document.getElementById("userSmokingHistory").value;
    let userPeso = document.getElementById("userPeso").value;
    let userAltura = document.getElementById("userAltura").value;
    let userHbA1c = document.getElementById("userHbA1c")?.value?.trim() || "";
    let userGlucose = document.getElementById("userGlucose")?.value?.trim() || "";


    console.log("Enviando mensaje:", userName +"|"+ message +"|"+ userGender+"|"+ userAge+"|"+ userHypertension+"|"+ userHeartDisease+"|"+ userSmokingHistory+"|"+ userPeso+"|"+ userAltura+"|"+ userHbA1c+"|"+ userGlucose); // Depuración:imprime en la consola del navegador lo que el usuario ingresó

    //Enviamos el mensaje al backend o servidor FASTAPI con fetch
    let response = await fetch("http://127.0.0.1:9000/chatbot", { //Envía una solicitud POST a la URL http://127.0.0.1:8000/chatbot, donde está la API de FastAPI.
        method: "POST", //Indica que estamos enviando datos al servidor (FastAPI).
        headers: { //Especifica que los datos se enviarán en formato JSON.
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ //Convierte los datos (name y text) en un JSON para que FastAPI los pueda recibir.
            name: userName,
            text: message,     
            gender: userGender,
            age: userAge,
            hypertension: userHypertension,
            heart_disease: userHeartDisease,
            smoking_history: userSmokingHistory,
            peso: userPeso,
            altura: userAltura,
            hbA1c_input: userHbA1c,
            glucose_input: userGlucose }) 
    });

    //Convierte la respuesta del servidor de formato JSON a un objeto JavaScript.
    let data = await response.json(); 

    // Depuración: Imprime en la consola la respuesta de FastAPI para asegurarnos de que la comunicación funciona.
    console.log("Respuesta del servidor:", data); 

    //Encuentra un elemento en la página HTML con el id="chatResponse" y reemplaza su contenido con la respuesta de FastAPI.
    document.getElementById("chatResponse").innerText = data.response;
}*/


