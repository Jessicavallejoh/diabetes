//----------------------------------------------------------------------------------------
//function cargarSeccion(seccion):  Función para cargar el contenido de las secciones con 
//AJAX que recibe como parametro la variable 'seccion' que contiene la sección que se desea cargar
//y devuelve el contenido de la sección
function cargarSeccion(seccion) {
    // Verifica que la función sea llamada correctamente
    console.log('Cargando sección:', seccion);  
    
    // Crear el objeto XMLHttpRequest
    var xhr = new XMLHttpRequest();  

    // Configura la solicitud para obtener el archivo HTML correspondiente a la seccion
    xhr.open('GET', '../html/' + seccion + '.html', true);  

    // Maneja la respuesta de la solicitud. el contenido del archivo HTML solicitado 
    // se insertará en el div con id='contenido' del archivo index.html si la solicitud es exitosa
    xhr.onload = function() {
        // Si la solicitud es exitosa (código de estado 200)
        if (xhr.status === 200) {  
            // Insertar el contenido en el div con id "contenido"
            document.getElementById('contenido').innerHTML = xhr.responseText;  
        } else {
            // En caso de error
            document.getElementById('contenido').innerHTML = 'Error al cargar la sección';  
        }
    };

    //Si ocurre un error durante la solicitud (por ejemplo, si no se puede acceder al archivo),
    //se mostrará un mensaje de error.
    xhr.onerror = function() {
        document.getElementById('contenido').innerHTML = 'Error de conexión';  // En caso de error en la conexión
    };

    // Enviar la solicitud
    xhr.send();
}


// Cargar "inicio.html" automáticamente cuando la página index carga
document.addEventListener("DOMContentLoaded", () => {
    cargarSeccion("inicio");
});