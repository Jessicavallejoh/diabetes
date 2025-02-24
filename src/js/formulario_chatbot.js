/*En este archivo se encuentran todas las funciones necesarias para procesar
los datos del formulario del chatbot:

    las funciones son:
        1. iniciarChat(): se ejecuta cuando se carga la página para mostrar la pregunta inicial
        2. scrollToBottom(): funcion que hace que el scroll siempre este en la pregunta actual.
        3. mostrarPregunta(): se ejecuta cuando la persona empieza a responder
        4. mostrarRespuestaFinal(): se ejecuta cuando la persona termina de responder y muestra un resumen de las respuestas
        5. guardarRespuesta(): se ejecuta cuando la persona responde a la pregunta
        6. enviarRespuestas(): se ejecuta cuando la persona termina de responder todas las preguntas
        7. mostrarMensajeBienvenida(): se ejecuta cuando se carga la página para mostrar el mensaje de bienvenida*/

//Se definen las preguntas del chatbot
const preguntasChatbot = [
    { pregunta: "Antes de comenzar, dime ¿cuál es tu nombre? 😊", tipo: "texto" },
    { pregunta: "¿Cuál es tu genero?", 
        tipo: "opcion", 
        opciones: {"Masculino":"Male", "Femenino":"Female" } 
    },
    { pregunta: "¿Cuál es tu edad?", tipo: "numero" },
    { pregunta: "¿Tienes hipertensión?", 
        tipo: "opcion", 
        opciones: {"Sí":1, "No":0} 
    },
    { pregunta: "¿Tienes enfermedad cardiovascular?", 
        tipo: "opcion", 
        opciones: {"Sí":1, "No":0} 
    },
    { pregunta: "¿Fumas?", 
        tipo: "opcion", 
        opciones: {"Actualmente":"current", 
            "Actualmente No":"not current", 
            "Anteriormente":"former",
            "Alguna vez":"ever", 
            "Nunca":"never",
            "Sin información":"No Info"} 
    }, 
    { pregunta: "Ingresa tu peso en Kilogramos (ejemplo: 75)", tipo: "numero" },
    { pregunta: "Ingresa tu altura en centimetros (ejemplo: 175)", tipo: "numero" },
    { pregunta: "Nivel de HbA1c (dejar en blanco si no sabe)", tipo: "texto" },
    { pregunta: "Nivel de glucosa en sangre (dejar en blanco si no sabe)", tipo: "texto" },
    
];

let respuestas = []; // Guardará las respuestas en formato 1 y 0 o texto
let preguntaActual = 0; // Índice de la pregunta actual

//Funcion que se ejecuta cuando se carga la página para mostrar la pregunta inicial
function iniciarChat() {
    mostrarPregunta();
}

//funcion que hace que el scroll siempre este en la pregunta actual.
function scrollToBottom() {
    const chatBox = document.getElementById("div-chatbot");
    chatBox.scrollTop = chatBox.scrollHeight;
}

//Funcion que se ejecuta cuando la ppersona empieza a responder y muestra la pregunta actual
function mostrarPregunta() {
    const chatBox = document.getElementById("chat-box");
    let preguntaObj = preguntasChatbot[preguntaActual];

    let div = document.createElement("div");
    div.className = "bot-message";
    div.innerHTML = `<strong>🤖 Chatbot:</strong> ${preguntaObj.pregunta}`;
    chatBox.appendChild(div);

    scrollToBottom();// Asegurar que el scroll baje al último mensaje

    let input = document.getElementById("user-input");
    input.value = ""; // Limpiar input

    let botonEnviar = document.querySelector(".input-container button");
    botonEnviar.onclick = () => guardarRespuesta(); // Asignar evento

    if (preguntaObj.tipo === "opcion") {
        // Si la pregunta es de opción, ocultamos el input y mostramos botones
        //document.querySelector(".input-container").style.display = "none";

        let opcionesDiv = document.createElement("div");
        opcionesDiv.className = "options-container";

        for (let [texto, valor] of Object.entries(preguntaObj.opciones)) {
            let boton = document.createElement("button");
            boton.innerText = texto;
            boton.onclick = () =>{
                guardarRespuesta(valor, texto);
                opcionesDiv.remove(); // Ocultar botones después de la selección de la respuesta
            } 
            opcionesDiv.appendChild(boton);
        }
        chatBox.appendChild(opcionesDiv);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

//Funcion que se ejecuta cuando la persona termina de responder y muestra un resumen de las respuestas
function mostrarRespuestaFinal(mensaje) {
    const chatBox = document.getElementById("chat-box");
    let div = document.createElement("div");
    div.className = "bot-message";

    let resumen = "<br><strong>🤖 Chatbot:</strong> 📋 Resumen de tus respuestas:<br><br>";
    //recorre cada pregunta y sus respuestas y las muestra al usuario
    preguntasChatbot.forEach((preg, index) => {
        resumen += `<strong>📌 ${preg.pregunta}</strong>: ${respuestas[index]}<br>`;
    });

    //Trae la respuesta de la funcion recibir_respuestas del backend y las muestra al usuario
    div.innerHTML = resumen + `<br> ${mensaje.replace(/\n/g, "<br>")}`;
    chatBox.appendChild(div);

    scrollToBottom();// Asegurar que el scroll baje al último mensaje

    chatBox.scrollTop = chatBox.scrollHeight;
}

//Funcion que guarda las respuestas de la persona
function guardarRespuesta(respuesta = null, textoRespuesta = null) {

    //Se verifica que la persona haya respondido todas las preguntas y no sobrepase la cantidad de preguntas
    if (preguntaActual >= preguntasChatbot.length) {
        console.warn("No hay más preguntas.");
        return;
    }

    let preguntaObj = preguntasChatbot[preguntaActual];

    console.log("Objeto pregunta actual:", preguntaObj); //Depuracion

    //Verificamos si el elemento existe
    if (!preguntaObj) {
        console.error("Error: preguntaObj es undefined.");
        return;
    }

    console.log(`Guardando respuesta para: ${preguntaObj.pregunta}`);//Depuracion

    //Verificamos el tipo de pregunta si es tipo numero o texto
    if (preguntaObj.tipo === "numero") {
        let input = document.getElementById("user-input");
        let numero = parseFloat(input.value.trim()); //convertimos el texto a numero

        //Verificamos si la persona no ingresa un numero y es una pregunta de glucosa o HbA1c ya que no son obligatorias
        if (numero === "" && (preguntaObj.pregunta.includes("HbA1c") || preguntaObj.pregunta.includes("glucosa"))) {
            respuesta = "";
            textoRespuesta = "(No proporcionado)";
        } else { //Si la persona no ingresa un numero y no es una pregunta de glucosa o HbA1c
            numero = parseFloat(numero); //convertimos el texto a numero
            if (isNaN(numero)) {
                alert("Por favor ingresa un número válido.");
                return;
            }
            respuesta = numero;
            textoRespuesta = numero;
        }
    } else if (preguntaObj.tipo === "texto") { //verificamos si la persona no ingresa un texto
        let input = document.getElementById("user-input");
        respuesta = input.value.trim(); //obtenemos el texto ingresado
        //Verificamos si la persona no ingresa un texto y es una pregunta de glucosa o HbA1c ya que no son obligatorias
        if (respuesta === "" && (preguntaObj.pregunta.includes("HbA1c") || preguntaObj.pregunta.includes("glucosa"))) {
            textoRespuesta = "(No proporcionado)";
        } else if (respuesta === "") {
            return;
        } else {
            textoRespuesta = respuesta;
        }
    }

    console.log("Respuesta guardada:", respuesta);
    respuestas.push(respuesta);

    // Eliminar botones de opciones si existen
    let opcionesContainer = document.querySelector(".options-container");
    if (opcionesContainer) {
        opcionesContainer.remove(); // Elimina el contenedor con los botones
    }

    // Mostrar respuesta en el chat
    const chatBox = document.getElementById("chat-box");
    let userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.innerHTML = `<strong>👤 ${respuestas[0]}:</strong> ${textoRespuesta}`;
    chatBox.appendChild(userDiv);

    scrollToBottom();// Asegurar que el scroll baje al último mensaje

    preguntaActual++; // Incrementar el contador de preguntas

    //verificamos si la pregunta actual es menor a la cantidad de preguntas
    if (preguntaActual < preguntasChatbot.length) {
        setTimeout(mostrarPregunta, 500);
    } else { //si la pregunta actual es igual a la cantidad de preguntas se envian los datos al servidor
        enviarDatosAlServidor();
    }
}

// Función para mostrar mensaje de bienvenida al cargar el chatbot
function mostrarMensajeBienvenida() {
    const chatBox = document.getElementById("chat-box");

    if (!chatBox) {
        console.error("No se encontró el contenedor del chat.");
        return;
    }

    let bienvenida = `
        <div class="bot-message">
            <strong>🔮 ¡Bienvenido a Predice! </strong><br>
            Tu salud es lo más importante, y Predice está aquí para ayudarte a estimar tu riesgo de desarrollar diabetes en solo unos minutos. <br><br>

            <strong>💡 ¿Cómo funciona?</strong><br>
            🔹 Responde algunas preguntas sobre tu salud y estilo de vida.<br>
            🔹 Obtén un porcentaje de riesgo basado en tu información.<br>
            🔹 Recibe recomendaciones personalizadas para prevenir o manejar la diabetes.<br><br>

            📊 Toma el control de tu bienestar. ¡Comienza ahora y descubre qué medidas puedes tomar para cuidar tu salud! 💙<br><br>
            <strong>Antes de comenzar, dime ¿cuál es tu nombre? 😊</strong>
        </div>
    `;

    chatBox.innerHTML = bienvenida; // Agrega el mensaje en el chat
}

// Ejecutar la función al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    cargarMensajeBienvenida();
});

//Funcion que se ejecuta cuando la persona termina de responder todas las preguntas y envia los datos al servidor
function enviarDatosAlServidor() {
    console.log("Respuestas finales:", respuestas);
    // Enviar los datos al servidor
    fetch("http://127.0.0.1:9000/formulario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ respuestas: respuestas })
    })
    .then(response => response.json())
    .then(data => {//verificamos si hubo un error
        if (data.error) {
            console.error("Error del servidor:", data.error);
        }else{
            mostrarRespuestaFinal(data.reply);
        }
    })
    .catch(error => console.error("Error al enviar los datos:", error));
}
