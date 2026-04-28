import socket
import GUI
import os
import pathlib
import sys
import json

def get_base_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable).parent.parent
    else:
        return pathlib.Path(__file__).parent.parent


PORT = 5000
BASE_DIR = get_base_path() 
DATA_CLIENT = pathlib.Path.home() / "DataClient"
DATA_CLIENT.mkdir(exist_ok=True)

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

            clean_name = os.path.basename(file)  
            filepath = os.path.join(DATA_CLIENT, clean_name)
            with open(filepath, "wb") as f:
                f.write(received)

            GUI.info(f"File {file} received and saved in {filepath}")

        client_socket.close()
    except Exception as e:
        GUI.error("None")
        print("Error in send_file_request:", e)

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
            GUI.info(f"File {file} uploaded successfully to {user}/")
        else:
            GUI.error("None")

        client_socket.close()
    except Exception as e:
        GUI.error("None")
        print("Error in upload_file:", e)

def availables_files(user, ip="127.0.0.1", password=""):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, PORT))
        client_socket.send(f"FILES;{user};{password};request\n".encode())

        response = b""
        while not response.endswith(b"\n"):
            chunk = client_socket.recv(1)
            if not chunk:
                break
            response += chunk

        response = response.decode().strip()
        client_socket.close()
        
        partes = response.split(";")
        if partes[0] == "FILES":
            result = [f for f in partes[1:] if f] 
            return result
        return []
    except Exception as e:
        print("Error in availables_files:", e)
        return []
    
def availables_users(user, ip="127.0.0.1", password=""):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, PORT))
        client_socket.send(f"USERS;{user};{password};request\n".encode())

        response = b""
        while not response.endswith(b"\n"):
            chunk = client_socket.recv(1)
            if not chunk:
                break
            response += chunk

        response = response.decode().strip()
        client_socket.close()
        
        partes = response.split(";")
        if partes[0] == "USERS":
            result = [f for f in partes[1:] if f] 
            return result
        return []
    except Exception as e:
        print("Error in availables_users:", e)
        return []

def login(ip, usuario, password, gui):
    if ip == "localhost":
        ip = "127.0.0.1"
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, PORT))
        mensaje = f"LOGIN;{usuario};{password}\n"
        print(repr(mensaje)) 
        client_socket.send(mensaje.encode())
        respuesta = b""
        while not respuesta.endswith(b"\n"):
            chunk = client_socket.recv(1)
            if not chunk:
                break
            respuesta += chunk
        print(repr(respuesta))  
        respuesta = respuesta.decode().strip()
        client_socket.close()
        if respuesta.strip().upper() == "OK":
            with open(os.path.join(BASE_DIR / "login.json"), "w") as f:
                json.dump({"ip": ip, "user": usuario, "password": password}, f)

            gui.start3(
                ip,
                usuario,
                log_out,
                lambda u, fp, i: upload_file(u, fp, i),       
                lambda u, f, i: send_file_request(u, f, i), 
                lambda u, i: availables_files(u, i, password),
                lambda u, i: availables_users(u, i, password)
            )
        else:
            GUI.error("User/Password")
    except ConnectionRefusedError:
        GUI.error("ServerDown")
        gui.start1(lambda ip, u, p: login(ip, u, p, gui))
    except TimeoutError:
        GUI.error("Timeout")
        gui.start1(lambda ip, u, p: login(ip, u, p, gui))
    except Exception as e:
        GUI.error("None")
        print("Error in login:", e)
        gui.start1(lambda ip, u, p: login(ip, u, p, gui))

def log_out(gui):
    login_file = BASE_DIR / "login.json"
    if login_file.exists():
        login_file.unlink()
    gui.start1(lambda ip, u, p: login(ip, u, p, gui))
        
if __name__ == "__main__":
    gui = GUI.class_GUI()
    login_file = BASE_DIR / "login.json"

    file = None
    if login_file.exists():
        try:
            with open(login_file, "r") as f:
                file = json.load(f)
        except (json.JSONDecodeError, ValueError):
            file = None

    if file:
        login(file["ip"], file["user"], file["password"], gui)  
    else:
        gui.start1(lambda ip, u, p: login(ip, u, p, gui))

    gui.mainloop()