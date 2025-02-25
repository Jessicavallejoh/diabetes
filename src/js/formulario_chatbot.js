/*En este archivo se encuentran todas las funciones necesarias para procesar
los datos del formulario del chatbot:

    las funciones son:
        1. iniciarChat(): se ejecuta cuando se carga la página para mostrar la pregunta inicial
        2. scrollToBottom(): funcion que hace que el scroll siempre este en la pregunta actual.
        3. mostrarPregunta(): se ejecuta cuando la persona empieza a responder
        4. mostrarRespuestaFinal(): se ejecuta cuando la persona termina de responder y muestra un resumen de las respuestas
        5. guardarRespuesta(): se ejecuta cuando la persona responde a la pregunta
        6. enviarRespuestas(): se ejecuta cuando la persona termina de responder todas las preguntas
        7. reiniciarEncuesta(): se ejecuta cuando la persona desea volver a realizar la encuesta
        8. despedida(): se ejecuta cuando la persona termina de responder todas las preguntas
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
    { pregunta: "Nivel de HbA1c (dejar en blanco si no sabe)", tipo: "numero" },
    { pregunta: "Nivel de glucosa en sangre (dejar en blanco si no sabe)", tipo: "numero" },
    
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
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar el scroll al final

    let input = document.getElementById("user-input");
    input.value = ""; // Limpiar input

    let botonEnviar = document.querySelector(".input-container button");
    botonEnviar.onclick = () => guardarRespuesta(); // Asignar evento

    //Si la pregunta es de opcion
    if (preguntaObj.tipo === "opcion") {
        // Hacer el input solo lectura y deshabilitar el botón de enviar
        input.readOnly = true;
        botonEnviar.disabled = true;

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
        scrollToBottom();// Asegurar que el scroll baje al último mensaje
        chatBox.scrollTop = chatBox.scrollHeight; // Desplazar el scroll al final
    }else{
        // Habilitar el input de texto y el botón de enviar
        input.readOnly = false;
        botonEnviar.disabled = false;
        input.focus();

        scrollToBottom();// Asegurar que el scroll baje al último mensaje
        chatBox.scrollTop = chatBox.scrollHeight; // Desplazar el scroll al final
    }
    scrollToBottom();// Asegurar que el scroll baje al último mensaje
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
    div.innerHTML = resumen + `<br> ${mensaje.replace(/\n/g, "<br>")
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")//convertir en negrita
        .replace(/^\* (.+)$/gm, '<ul>\n<li>$1</li>\n</ul>')// Convertir líneas que comienzan con "* " en listas desordenadas `<ul>
        .replace(/^\+ (.+)$/gm, '<ul>\n  <li>$1</li>\n</ul>')// Convertir líneas que comienzan con "+ " en listas anidadas `<ul>` dentro de `<li>`
        .replace(/<\/ul>\n<ul>/g, '')}`; // Unir listas consecutivas correctamente
    chatBox.appendChild(div);

    // Pregunta si desea repetir la encuesta
    let preguntaDiv = document.createElement("div");
    preguntaDiv.className = "bot-message";
    preguntaDiv.innerHTML = "<strong>🔄 ¿Te gustaría volver a realizar la encuesta?</strong>";
    chatBox.appendChild(preguntaDiv);

    // Contenedor para los botones de opción
    let opcionesDiv = document.createElement("div");
    opcionesDiv.className = "options-container";

    let botonSi = document.createElement("button");
    botonSi.innerText = "Sí, repetir";
    botonSi.onclick = () => reiniciarEncuesta();

    let botonNo = document.createElement("button");
    botonNo.innerText = "No, gracias";
    botonNo.onclick = () => despedida();

    opcionesDiv.appendChild(botonSi);
    opcionesDiv.appendChild(botonNo);
    chatBox.appendChild(opcionesDiv);

    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar el scroll al final

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
        //let numero = parseFloat(input.value.trim()); //convertimos el texto a numero
        let valorIngresado = input.value.trim(); // Obtenemos el valor ingresado como cadena


        //Verificamos si la persona no ingresa un numero y es una pregunta de glucosa o HbA1c ya que no son obligatorias
        if (valorIngresado === "" && ( preguntaObj.pregunta.includes("HbA1c") || preguntaObj.pregunta.includes("glucosa"))) {
            respuesta = null; // Usamos null en lugar de una cadena vacía
            textoRespuesta = "(No proporcionado)";
        } else if (valorIngresado === "") {
            alert("Por favor ingresa un número.");
            return;
        }else { //Si la persona no ingresa un numero y no es una pregunta de glucosa o HbA1c
            let numero = parseFloat(valorIngresado); //convertimos el texto a numero
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
            respuesta = null; // Usamos null en lugar de una cadena vacía
            textoRespuesta = "(No proporcionado)";
        } else if (respuesta === "") {
            alert("Por favor ingresa una respuesta válida.");
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

    chatBox.scrollTop = chatBox.scrollHeight;

    preguntaActual++; // Incrementar el contador de preguntas

    //verificamos si la pregunta actual es menor a la cantidad de preguntas
    if (preguntaActual < preguntasChatbot.length) {
        setTimeout(mostrarPregunta, 500);
    } else { //si la pregunta actual es igual a la cantidad de preguntas se envian los datos al servidor
        // Deshabilitar el input y el botón
        document.getElementById("user-input").style.display="true";
        document.querySelector(".input-container button").style.display="true";

        const chatBox = document.getElementById("chat-box");
        let div = document.createElement("div");
        div.className = "bot-message";
        div.innerHTML = `<strong>🤖 Chatbot:</strong> 🔍 <b>Analizando tu información...</b><br>
                        Nuestro sistema está procesando tus respuestas para estimar tu riesgo de diabetes. 
                        Esto tomará solo unos segundos.<br><br>

                        <b>⏳ Por favor, espera un momento...</b><br>
                        Pronto recibirás tu resultado junto con recomendaciones personalizadas para cuidar tu salud.
                        ¡Gracias por tu paciencia! 😊`;
        
        chatBox.appendChild(div);

        scrollToBottom();// Asegurar que el scroll baje al último mensaje

        chatBox.scrollTop = chatBox.scrollHeight;

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
    scrollToBottom();// Asegurar que el scroll baje al último mensaje

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Función para reiniciar la encuesta
function reiniciarEncuesta() {
    let input = document.getElementById("user-input");
    let botonEnviar = document.querySelector(".input-container button");

    preguntaActual = 0; //Contedor de preguntas actual en 0
    respuestas = []; //Lista de respuestas vacia
    
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = ""; // Limpiar el chat

    // Habilitar el input de texto y el botón de enviar
    input.readOnly = false;
    botonEnviar.disabled = false;
    input.focus();

    mostrarMensajeBienvenida(); // Volver a empezar la encuesta
    iniciarChat();
}

// Función para mostrar mensaje de despedida
function despedida() {
    const chatBox = document.getElementById("chat-box");
    let div = document.createElement("div");
    div.className = "bot-message";
    div.innerHTML = "<strong>🤖 Chatbot:</strong> ¡Gracias por participar! Cuida tu salud y vuelve cuando necesites. 💙";
    chatBox.appendChild(div);
    scrollToBottom();// Asegurar que el scroll baje al último mensaje
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar el scroll al final
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
