import json
import shutil
import pathlib
import sys

def get_base_path() -> pathlib.Path:
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys.executable).parent.parent
    else:
        return pathlib.Path(__file__).parent.parent

print("|----------Server Console----------|")

BASE_DIR = get_base_path() / "DataServer"
USERS_FILE = BASE_DIR / "users.json"

BASE_DIR.mkdir(exist_ok=True)
(BASE_DIR / "global").mkdir(exist_ok=True)

if not USERS_FILE.exists():
    USERS_FILE.write_text("[]", encoding="utf-8")


def load_users() -> list:
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[ERROR] Could not read users file: {e}")
        return []


def save_users(users: list) -> None:
    USERS_FILE.write_text(json.dumps(users, indent=4, ensure_ascii=False), encoding="utf-8")


def list_users() -> None:
    users = load_users()
    if not users:
        print("No users registered.")
        return
    print(f"Registered users ({len(users)}):")
    for u in users:
        print(f"  - {u.get('username')}")


def add_user(username: str, password: str) -> None:
    username = username.strip()
    users = load_users()

    if any(u.get("username") == username for u in users):
        print(f"[ERROR] User '{username}' already exists.")
        return

    users.append({"username": username, "password": password})
    save_users(users)

    (BASE_DIR / username).mkdir(exist_ok=True)
    print(f"[OK] User '{username}' added successfully.")


def remove_user(username: str) -> bool:
    username = username.strip()
    users = load_users()

    new_users = [u for u in users if u.get("username") != username]

    if len(new_users) == len(users):
        print(f"[ERROR] User '{username}' not found.")
        return False

    save_users(new_users)

    user_dir = BASE_DIR / username
    if user_dir.is_dir():
        shutil.rmtree(user_dir)
        print(f"[OK] User '{username}' and their folder have been deleted.")
    else:
        print(f"[OK] User '{username}' removed from JSON (no folder found).")

    return True


def change_password(username: str, new_password: str) -> None:
    username = username.strip()
    users = load_users()

    for u in users:
        if u.get("username") == username:
            u["password"] = new_password
            save_users(users)
            print(f"[OK] Password for '{username}' has been updated.")
            return

    print(f"[ERROR] User '{username}' not found.")


def show_help() -> None:
    print("|---Available commands---|")
    print("  list")
    print("  add <username> <password>")
    print("  remove <username>")
    print("  changepassword <username> <new_password>")
    print("  help")
    print("  exit / quit")


def start() -> None:
    while True:
        try:
            command = input(">>> ").strip().split()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "list":
            list_users()
        elif cmd == "add" and len(command) == 3:
            add_user(command[1], command[2])
        elif cmd == "remove" and len(command) == 2:
            remove_user(command[1])
        elif cmd == "changepassword" and len(command) == 3:
            change_password(command[1], command[2])
        elif cmd == "help":
            show_help()
        elif cmd in ("exit", "quit"):
            print("Exiting...")
            break
        else:
            print(f"Unknown command '{command[0]}'. Type 'help' to see available commands.")


if __name__ == "__main__":
    start()