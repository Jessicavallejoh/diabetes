# Equipo 13
Jessica Vallejo  
Wilder Alexander Restrepo  
Yenifer Barco Castrillón  

## Instrucciones para ejecutar el proyecto.

* **1. Tener instalado ollama 3.2 :** [Ollama 3.2](https://ollama.com/library/llama3.2)<br>
     - **1.1.** Descarga la version 3.2 que pesa 2GB<br>
     - **1.2.** Ejecuta el archivo y espera a que termine la instalación<br>
     - **1.3.** Abre una terminal o CMD como administrador y ejecuta este comando: ```ollama run llama3.2```<br>
     - **1.4.** Cuando termine de descargar los paquetes, cierra el CMD<br>
     - **1.5.** Revisa que no este activo el ollama, en caso de  estar activo para el proceso.<br>
     - **1.6.** Ejecuta el comando ollama server en cmd como administrador, esto iniciara el servicio de ollama<br><br>
   
* **2. Abrir el proyecto en Visual Studio y abrir la terminal.** <br>
     En este caso se puede ejecutar el proyecto de varias formas:<br>
     
     - **2.1.** Ejecuta el comando: ```uvicorn main:app --reload --port 9000 --log-level debug```
          Este te permite ejecutar el archivo main y luego, debes ir a la carpeta **/src/Html/index.html** das clic derecho sobre el archivo y escoges la opcion "Abrir con Live Server"<br>
     - **2.2.** Ejecuta el comado: ```python main.py```
          Esto es posibles ya que en el proyecto se encuentra un archivo donde se especifican los puertos y rutas a abrir al ejecutar el proyecto.<br>
     - **2.3.** Ejecutar desde el boton de Visual Studio:
          Esto es posibles ya que en el proyecto se encuentra un archivo donde se especifican los puertos y rutas a abrir al ejecutar el proyecto.<br><br>

## Estructura del proyecto.<br>
El proyecto tiene la siguiente estructura:<br>

**Carpeta principal del Proyecto:** diabetes<br><br>

**Archivos sin carpeta**<br>
- ||--> **main.py**: Contiene las funcioes necesarias para el chatbot.<br>
- ||--> **ollama.py**: Contiene la conexion con ollama y la estructura de la generacion de recomendaciones al final retorna una respuesta.<br>
- ||--> **prediction.py**: Contiene todo el modelo de prediccion que utiliza el chatbot.<br>
- ||--> **conexionAutHtml.py**: Contiene la funcion que permite abrir de manera automatica el archivo HTML.<br>
- ||--> **filtros.py**: Contiene las funciones necesarias para la creacion de los filtros<br><br>

**Carpetas**<br>
- ||--> **Dataset**: Contiene los archivos .csv con la informacion relevante de la enfermedad.<br>
-	||--> **src**: Contiene todos los archivos necesarios para la ejecucion de la pagina web y la conexion de la pagina con FastAPI<br>
    -  ||---> **css**: Contiene los archivos con los estilos .css de la pagina web.<br>
    -	||---> **fonts**: Contiene el archivo con el tipo de letra utilizada en el proyecto, en este caso Monserrat.<br>
    -	||---> **html**: Contiene los archivos .html que da la estructura de la pagina web.<br>
    -	||---> **img**: Contiene todas las imagenes utilizadasen la página web html.<br>
    -	||---> **js**: Contiene los archivos de javascript necesarios para conectar el HTML con el cahtboot.<br>
    -	||---> **json**: Contiene los archivos .json <br>

