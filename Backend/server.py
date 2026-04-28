import socket
import json
import pathlib
import sys
import threading
import logging

# ==========================================
# 1. CONFIGURACIÓN DEL SERVIDOR
# ==========================================

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096 # 4KB por chunk (óptimo para red y disco)

# Configuración de Logging (reemplaza a los print básicos)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_base_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable).parent.parent
    else:
        return pathlib.Path(__file__).parent.parent

BASE_DIR = get_base_path() / "Backend" / "database"
USERS_FILE = BASE_DIR / "users.json"

# Inicialización de directorios
BASE_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "global").mkdir(exist_ok=True)

if not USERS_FILE.exists():
    USERS_FILE.write_text("[]", encoding="utf-8")


# ==========================================
# 2. FUNCIONES DE LÓGICA Y DATOS
# ==========================================

def validate_login(username: str, password: str) -> bool:
    """Verifica si el usuario y contraseña coinciden en el archivo JSON."""
    try:
        users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
        return any(u.get("username") == username and u.get("password") == password for u in users)
    except (json.JSONDecodeError, OSError) as e:
        logging.error(f"No se pudo leer el archivo de usuarios: {e}")
        return False

def recv_line(conn: socket.socket) -> str:
    """Lee byte a byte hasta encontrar un salto de línea (\n)."""
    buffer = b""
    while True:
        chunk = conn.recv(1)
        if not chunk or chunk == b"\n":
            break
        buffer += chunk
    return buffer.decode(errors='ignore').strip()


# ==========================================
# 3. TRANSFERENCIA DE ARCHIVOS
# ==========================================

def send_file(conn: socket.socket, username: str, filename: str) -> None:
    """Envía un archivo del servidor al cliente (Descarga)."""
    filename = pathlib.Path(filename).name # Previene Path Traversal
    filepath = BASE_DIR / username / filename

    if not filepath.exists():
        conn.send(b"ERROR\n")
        logging.warning(f"Archivo no encontrado: '{filename}' en {username}/")
        return

    # 1. Enviar el tamaño del archivo primero
    filesize = filepath.stat().st_size
    conn.send(str(filesize).encode() + b"\n")

    # 2. Leer del disco y enviar por red en chunks (No satura la RAM)
    with open(filepath, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            conn.sendall(chunk)

    logging.info(f"Archivo enviado: '{filename}' desde {username}/")

def receive_file(conn: socket.socket, username: str, filename: str) -> None:
    """Recibe un archivo del cliente y lo guarda directo a disco (Subida)."""
    filename = pathlib.Path(filename).name
    dest_dir = BASE_DIR / username
    dest_dir.mkdir(exist_ok=True)

    # 1. Leer el tamaño que nos dice el cliente que va a enviar
    filesize_str = recv_line(conn)
    if not filesize_str.isdigit():
        conn.send(b"ERROR\n")
        logging.error(f"Tamaño de archivo inválido recibido: '{filesize_str}'")
        return

    filesize = int(filesize_str)
    filepath = dest_dir / filename
    bytes_received = 0

    # 2. Escribir directamente al disco en chunks (Evita sobrecarga de RAM)
    with open(filepath, "wb") as f:
        while bytes_received < filesize:
            # Calculamos cuánto falta para no leer de más y bloquear el socket
            bytes_left = filesize - bytes_received
            chunk_size = min(BUFFER_SIZE, bytes_left)
            
            data = conn.recv(chunk_size)
            if not data:
                break # El cliente cerró la conexión abruptamente
            
            f.write(data)
            bytes_received += len(data)

    # 3. Verificar si recibimos todo
    if bytes_received < filesize:
        conn.send(b"ERROR\n")
        logging.error(f"Archivo incompleto: {bytes_received}/{filesize} bytes de '{filename}'")
        # Opcional: podrías añadir filepath.unlink() aquí para borrar el archivo corrupto
        return

    conn.send(b"OK\n")
    logging.info(f"Archivo guardado: '{filename}' en {dest_dir}/")


# ==========================================
# 4. MANEJO DE CONEXIONES Y RUTEO
# ==========================================

def handle_connection(conn: socket.socket, addr) -> None:
    """Maneja la conexión de UN cliente específico."""
    try:
        data = recv_line(conn)
        if not data:
            return # Conexión vacía o ping

        parts = data.split(";")
        command = parts[0]

        if command == "LOGIN" and len(parts) == 3:
            _, username, password = parts
            if validate_login(username, password):
                conn.send(b"OK\n")
                logging.info(f"Login exitoso: {username} ({addr[0]})")
            else:
                conn.send(b"FAIL\n")
                logging.warning(f"Login fallido: {username} ({addr[0]})")

        elif command == "GET" and len(parts) == 3:
            # TODO: security -> access files of different user 
            _, username, filename = parts
            # Aseguramos que la carpeta del usuario exista (excepto 'global' que ya se crea al inicio)
            if username != "global":
                (BASE_DIR / username).mkdir(exist_ok=True)
            send_file(conn, username, filename)

        elif command == "PUT" and len(parts) == 3:
            # TODO: security -> add files without filter to every user
            _, username, filename = parts
            receive_file(conn, username, filename)

        else:
            conn.send(b"ERROR\n")
            logging.warning(f"Comando desconocido desde {addr[0]}: {data}")

    except Exception as e:
        logging.error(f"Error inesperado con {addr}: {e}")
        try:
            conn.send(b"ERROR\n")
        except:
            pass
    finally:
        # Siempre cerramos la conexión al final para no dejar sockets "fantasma"
        conn.close()

def main(config: list[str]):
    # TODO: Refact server for implement new structure project
    [ host, port ] = config
    logging.info("|---------- Iniciando Servidor ----------|")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        logging.info(f"Escuchando en {host}:{port}...")

        while True:
            # 1. El servidor se queda aquí esperando a que alguien se conecte
            conn, addr = server_socket.accept()
            logging.info(f"Nueva conexión entrante: {addr}")
            
            # 2. Creamos un HILO (Thread) independiente para atender a este cliente
            # daemon=True asegura que si cierras el servidor principal, los hilos se mueran con él.
            client_thread = threading.Thread(
                target=handle_connection, 
                args=(conn, addr),
                daemon=True 
            )
            
            # 3. Iniciamos el hilo. El bucle while vuelve inmediatamente arriba a esperar al siguiente.
            client_thread.start()

if __name__ == "__main__":
    main()