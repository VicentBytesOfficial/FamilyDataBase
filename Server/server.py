import socket
import os
import json
import pathlib
import sys

def get_base_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable).parent
    else:
        return pathlib.Path(__file__).parent.parent

print("|----------Server Output----------|")

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096

BASE_DIR = get_base_path() / "DataServer"
USERS_FILE = BASE_DIR / "users.json"

BASE_DIR.mkdir(exist_ok=True)
(BASE_DIR / "global").mkdir(exist_ok=True)

if not USERS_FILE.exists():
    USERS_FILE.write_text("[]", encoding="utf-8")


def validate_login(username: str, password: str) -> bool:
    """Checks if the username and password match a user in the JSON file."""
    try:
        users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
        return any(u.get("username") == username and u.get("password") == password for u in users)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[ERROR] Could not read users file: {e}")
        return False


def recv_line(conn: socket.socket) -> str:
    """Receives data byte by byte until newline. Returns decoded string."""
    buffer = b""
    while True:
        chunk = conn.recv(1)
        if not chunk or chunk == b"\n":
            break
        buffer += chunk
    return buffer.decode().strip()


def send_file(conn: socket.socket, username: str, filename: str) -> None:
    """Sends a file from the server to the client."""
    # Prevent path traversal attacks (e.g. filename = "../../etc/passwd")
    filename = pathlib.Path(filename).name
    filepath = BASE_DIR / username / filename

    print(f"[GET] Looking for file: {filepath}")

    if not filepath.exists():
        conn.send(b"ERROR\n")
        print(f"[ERROR] File '{filename}' not found in {username}/")
        return

    filesize = filepath.stat().st_size
    conn.send(str(filesize).encode() + b"\n")

    with open(filepath, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            conn.sendall(chunk)

    print(f"[OK] File '{filename}' sent from {username}/")


def receive_file(conn: socket.socket, username: str, filename: str) -> None:
    """Receives a file from the client and saves it on the server."""
    # Prevent path traversal attacks
    filename = pathlib.Path(filename).name
    dest_dir = BASE_DIR / username
    dest_dir.mkdir(exist_ok=True)

    filesize_str = recv_line(conn)

    if not filesize_str.isdigit():
        conn.send(b"ERROR\n")
        print(f"[ERROR] Invalid file size received: '{filesize_str}'")
        return

    filesize = int(filesize_str)
    received = b""

    while len(received) < filesize:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        received += data

    if len(received) < filesize:
        conn.send(b"ERROR\n")
        print(f"[ERROR] Incomplete file received: {len(received)}/{filesize} bytes")
        return

    filepath = dest_dir / filename
    filepath.write_bytes(received)
    conn.send(b"OK\n")
    print(f"[OK] File '{filename}' saved to {dest_dir}/")


def handle_connection(conn: socket.socket, addr) -> None:
    """Handles a single client connection."""
    try:
        data = recv_line(conn)

        if not data:
            conn.send(b"ERROR\n")
            return

        parts = data.split(";")
        command = parts[0]

        if command == "LOGIN" and len(parts) == 3:
            _, username, password = parts
            response = b"OK\n" if validate_login(username, password) else b"FAIL\n"
            conn.send(response)
            print(f"[LOGIN] {username} -> {'OK' if response == b'OK\n' else 'FAIL'}")

        elif command == "GET" and len(parts) == 3:
            _, username, filename = parts
            if username != "global":
                (BASE_DIR / username).mkdir(exist_ok=True)
            send_file(conn, username, filename)

        elif command == "PUT" and len(parts) == 3:
            _, username, filename = parts
            receive_file(conn, username, filename)

        else:
            conn.send(b"ERROR\n")
            print(f"[ERROR] Unknown command: {data}")

    except Exception as e:
        print(f"[ERROR] Unexpected error from {addr}: {e}")
        try:
            conn.send(b"ERROR\n")
        except:
            pass
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"[CONNECTION] From {addr}")
            handle_connection(conn, addr)


if __name__ == "__main__":
    main()