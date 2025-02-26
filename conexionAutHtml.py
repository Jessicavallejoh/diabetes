"""En este archivo se encuentra la funcion que permite abrir de manera automatica
el archivo HTML
subprocess: que permite ejecutar comandos del sistema operativo desde Python.
webbroser: permite abrir automáticamente una página web en el navegador predeterminado.
time: permite manejar pausas y tiempos de espera
treading: permite ejecutar funciones en segundo plano sin bloquear el código principal."""

#--------------------------Importamos librerias------------------------------
import subprocess
#import uvicorn
import webbrowser 
import time
import threading

#--------------------------Abrir HTML automaticamente-------------------------

# Configuración del puerto y la direccion del host
PORT_HTML = 5500  # Puedes cambiarlo según necesites
PORT_UVICORN = 9000
# Configura el puerto del Live Server (por defecto es 5500)
LIVE_SERVER_PORT = 5500
#HOST = "127.0.0.1"

# Función para abrir el navegador automáticamente
def open_browser():
    """Espera y abre la página en el navegador Live Server."""
    time.sleep(20) # Espera 20 segundos para dar tiempo a que el servidor inicie
    url = f"http://127.0.1.1:{LIVE_SERVER_PORT}/src/html/index.html" # Ruta del archivo HTML
    webbrowser.open(url)

# Funcion para iniciar el servidor
def start_server():
    # Iniciar el navegador en un hilo separado
    threading.Thread(target=open_browser).start()
    
    # Iniciar el servidor Uvicorn
    #uvicorn.run(app, host="127.0.0.1", port=port, reload=True)
    
    # Ejecuta el servidor Uvicorn con las opciones dadas
    subprocess.run(["uvicorn", "main:app", "--reload", "--log-level", "debug", "--host", "127.0.0.1", "--port", str(PORT_UVICORN)])
    
if __name__ == "__main__":
    start_server()