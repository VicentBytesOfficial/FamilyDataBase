import socket
import GUI
import os
import pathlib
import sys

def get_base_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable).parent
    else:
        return pathlib.Path(__file__).parent.parent

PORT = 5000
BASE_DIR = get_base_path() 
DATA_CLIENT = BASE_DIR / "DataClient"
DATA_CLIENT.mkdir(exist_ok=True)

os.makedirs(DATA_CLIENT, exist_ok=True)

def send_file_request(user, file, ip="127.0.0.1"):
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
            GUI.error("FileNotFound")
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

            GUI.info(f"Archivo {file} recibido y guardado en {filepath}")

        client_socket.close()
    except Exception as e:
        GUI.error("None")
        print("Error en send_file_request:", e)

def upload_file(user, filepath, ip="127.0.0.1"):
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

        if respuesta == "OK":
            GUI.info(f"Archivo {file} subido correctamente al servidor en {user}/")
        else:
            GUI.error("None")

        client_socket.close()
    except Exception as e:
        GUI.error("None")
        print("Error en upload_file:", e)

def login(ip, usuario, password):
    if ip == "localhost":
        ip = "127.0.0.1"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, PORT))

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
            GUI.start3(lambda user, file: send_file_request(user, file, ip),
                       lambda user, filepath: upload_file(user, filepath, ip))
        else:
            GUI.error("User/Password")

    except Exception as e:
        GUI.error("None")
        print("Error en login:", e)

if __name__ == "__main__":
    GUI.start1(login)