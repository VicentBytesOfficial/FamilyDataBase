from Backend.backend import backend

from Frontend.frontend import frontend

from utils.functions import inputCheck
from Backend.config.config import initConfig

if __name__=="__main__":
    # Formato: Lista[<identificador>, <completo>] -> Obligatorio para inputCheck
    opciones_dev = ["d", "developer"]
    opciones_server = ["s", "server"]
    opciones_client = ["c", "client"]

    # Lista de listas -> Obligatorio para inputCheck
    opciones_validas = [opciones_dev, opciones_server, opciones_client]

    role = inputCheck("Select your role: [D/d] developer, [S/s] server, [C/c] client", "Please choose a valid role.", opciones_validas)
    config = initConfig(role)
    if role == "server":
        backend(config)
    elif role == "client":
        frontend()
    else:
        # Developer mode: role = developer
        backend(config)
        frontend()