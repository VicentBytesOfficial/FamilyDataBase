import os
import webview

# Importamos la clase de tu backend (Respondiendo a tu pregunta)
from Backend.client import ApiCliente

def frontend():
    """
    Frontend entrypoint that recieve the class of the API (default: ApiCliente)
    """
    
    # 1. Instanciamos el backend. 
    # Al instanciarlo aquí, esta sesión del backend está viva mientras
    # la ventana visual esté abierta.
    api = ApiCliente()

    # 2. Construimos la ruta absoluta al archivo HTML.
    # __file__ apunta a "Frontend/main.py", por lo que dirname saca la carpeta "Frontend/"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "web", "index.html")

    # 3. Creamos la ventana de la aplicación.
    ventana = webview.create_window(
        title="Family Data Base",
        url=html_path,     # Cargamos el diseño web
        js_api=api,        # ¡Magia! Inyectamos el backend al frontend
        width=800,
        height=600,
        background_color="#3F4D6C", # Mantenemos el color azul oscuro de fondo original
        min_size=(400, 300)
    )

    # 4. Arrancamos el motor web (esto reemplaza a root.mainloop() de Tkinter)
    webview.start()