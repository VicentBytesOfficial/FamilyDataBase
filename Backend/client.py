import socket
import os
import pathlib
import sys

def get_base_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable).parent.parent
    else:
        return pathlib.Path(__file__).parent.parent

PORT = 5000
BASE_DIR = get_base_path() 
DATA_CLIENT = BASE_DIR / "Backend" / "database" / "client"
DATA_CLIENT.mkdir(parents=True, exist_ok=True) 

class ApiCliente:
    """
    Agrupamos las funciones en una clase para PyWebView. 
    """

    def send_file_request(self, user, file, ip="127.0.0.1"):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, PORT))

            client_socket.send(f"GET;{user};{file}\n".encode())

            filesize_str = b""
            while not filesize_str.endswith(b"\n"):
                chunk = client_socket.recv(1)
                if not chunk:
                    break
                filesize_str += chunk
            filesize_str = filesize_str.decode().strip()

            if filesize_str == "ERROR":
                client_socket.close()
                return {"success": False, "error": "FileNotFound", "message": f"El archivo {file} no existe en el servidor."}
            else:
                filesize = int(filesize_str)
                received = b""

                while len(received) < filesize:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    received += data

                filepath = os.path.join(DATA_CLIENT, file)
                with open(filepath, "wb") as f:
                    f.write(received)

                client_socket.close()
                return {
                    "success": True, 
                    "message": f"Archivo guardado exitosamente.", 
                    "filepath": filepath
                }

        except Exception as e:
            print(f"[LOG Backend] Error en send_file_request: {e}")
            return {"success": False, "error": "ConnectionError", "message": str(e)}

    def upload_file(self, user, filepath, ip="127.0.0.1"):
        try:
            file = os.path.basename(filepath)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, PORT))

            client_socket.send(f"PUT;{user};{file}\n".encode())

            filesize = os.path.getsize(filepath)
            client_socket.send(str(filesize).encode() + b"\n")

            with open(filepath, "rb") as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    client_socket.sendall(bytes_read)

            respuesta = b""
            while not respuesta.endswith(b"\n"):
                chunk = client_socket.recv(1)
                if not chunk:
                    break
                respuesta += chunk
            respuesta = respuesta.decode().strip()

            client_socket.close()

            if respuesta == "OK":
                return {"success": True, "message": f"Archivo {file} subido correctamente."}
            else:
                return {"success": False, "error": "ServerError", "message": "El servidor rechazó el archivo."}

        except Exception as e:
            print(f"[LOG Backend] Error en upload_file: {e}")
            return {"success": False, "error": "ConnectionError", "message": str(e)}

    def login(self, ip, usuario, password):
        if ip == "localhost":
            ip = "127.0.0.1"
            
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Limite de 3 segundos
            client_socket.settimeout(3.0)
            client_socket.connect((ip, PORT))
            
            # Quitamos limite tras conectar
            client_socket.settimeout(None)

            client_socket.send(f"LOGIN;{usuario};{password}\n".encode())
            
            respuesta = b""
            while not respuesta.endswith(b"\n"):
                chunk = client_socket.recv(1)
                if not chunk:
                    break
                respuesta += chunk
            respuesta = respuesta.decode().strip()
            client_socket.close()

            if respuesta == "OK":
                return {"success": True}
            else:
                return {"success": False, "error": "AuthFailed", "message": "Usuario o contraseña incorrectos."}

        except socket.timeout:
            # Esta es la pieza clave para que el timeout no se confunda con un error general
            print(f"[LOG Backend] Timeout intentando conectar a {ip}")
            return {"success": False, "error": "Timeout", "message": "El servidor tardó mucho en responder (Timeout)."}
            
        except Exception as e:
            print(f"[LOG Backend] Error en login: {e}")
            return {"success": False, "error": "ConnectionError", "message": "No se pudo conectar al servidor."}