# 🗄️ FamilyDataBase

A lightweight LAN file transfer system built with Python. Allows multiple users to upload and download files across a local network through a simple graphical interface.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Setting up the Server](#setting-up-the-server)
  - [Managing Users](#managing-users)
  - [Running the Client](#running-the-client)
- [Technical Info](#-technical-info)
- [Building an Executable](#-building-an-executable)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## ✨ Features

- 📁 Upload and download files over a local network (LAN)
- 👤 Multi-user support with username and password authentication
- 🌐 `global/` shared folder accessible by all users
- 🖥️ Simple Tkinter GUI for the client
- 🛠️ Server console for user management
- 🔒 Path traversal attack prevention

---

## 📂 Project Structure

```
FamilyDataBase/
├── Client/
│   ├── client.py       # Handles TCP connections and file transfer logic
│   └── GUI.py          # Tkinter graphical interface
├── Server/
│   ├── server.py       # TCP server, handles all client requests
│   └── console.py      # Admin console for managing users
├── Icons/
│   ├── client.png      # Icon for the client executable
│   ├── server.png      # Icon for the server executable
│   └── console.png     # Icon for the console executable
├── DataClient/         # Files downloaded by the client are saved here
└── DataServer/         # Server-side file storage
    ├── users.json      # Registered users (auto-created)
    └── global/         # Shared folder accessible by all users
```

---

## ⚙️ Requirements

- Python 3.10 or higher
- Tkinter (included with Python on Windows and macOS)
- Both devices must be on the **same local network (LAN)**

No external libraries required — only Python's standard library.

> **Want to run it without Python?** You can build a standalone `.exe` (Windows) or `.app` (macOS) using PyInstaller. See [Building an Executable](#-building-an-executable).

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/VicentBytes/FamilyDataBase.git
cd FamilyDataBase
```

2. **Verify Python is installed:**

```bash
python --version
```

That's it — no pip installs needed.

---

## 📖 Usage

### Setting up the Server

On the machine that will act as the server, run:

```bash
python Server/server.py
```

The server will start listening on port `5000`. You should see:

```
|----------Server Output----------|
Server listening on 0.0.0.0:5000...
```

> **Tip:** Find your server's local IP with `ipconfig` (Windows) or `ip a` (Linux/macOS). You'll need it to connect from the client.

---

### Managing Users

On the **server machine**, open a second terminal and run:

```bash
python Server/console.py
```

Available commands:

| Command | Description |
|---|---|
| `list` | List all registered users |
| `add <username> <password>` | Add a new user |
| `remove <username>` | Remove a user and their files |
| `changepassword <username> <new_password>` | Change a user's password |
| `help` | Show available commands |
| `exit` | Exit the console |

**Example:**

```
>>> add john mypassword123
[OK] User 'john' added successfully.

>>> list
Registered users (1):
  - john
```

> **Note:** There is a built-in `admin` user with full access to all folders. Its default password is `password`. **Change it immediately after setup using `changepassword admin <new_password>`.**

---

### Running the Client

On any machine in the same network, run:

```bash
python Client/client.py
```

**Step 1 — Enter the server's IP:**

Type the local IP address of the server machine (e.g. `192.168.1.10`) and click **Continue**.

**Step 2 — Login:**

Enter your username and password, then click **Login**.

**Step 3 — Transfer files:**

- **Download (GET):** Enter a username/folder and a filename, then click **Download**.
- **Upload (PUT):** Enter a username/folder, click **Upload**, and select a file from your computer.

> Files you download are saved to the `DataClient/` folder automatically.

#### Folder access rules:

| User type | Can access |
|---|---|
| Regular user | Their own folder + `global/` |
| `admin` | All folders |

---

## 🔧 Technical Info

| Property | Value |
|---|---|
| Protocol | TCP (raw sockets) |
| Default port | `5000` |
| Transfer format | Binary with newline-delimited headers |
| Auth storage | JSON (`DataServer/users.json`) |
| Buffer size | 4096 bytes |
| GUI framework | Tkinter |
| Python version | 3.10+ |

**How file transfer works:**

1. Client connects to server via TCP socket
2. Client sends a command line: `GET;username;filename` or `PUT;username;filename`
3. For downloads: server sends filesize, then raw bytes
4. For uploads: client sends filesize, then raw bytes
5. Server confirms with `OK` or `ERROR`

---

## 📦 Building an Executable

FamilyDataBase can be converted into standalone executables (`.exe` on Windows, `.app` on macOS) using [PyInstaller](https://pyinstaller.org/). No Python installation required on the target machine.

**Install PyInstaller:**

```bash
pip install pyinstaller
```

**Build the client:**

```bash
pyinstaller --onefile --windowed --icon=Icons/client.png --name="Family Data Base" Client/client.py
```

**Build the server:**

```bash
pyinstaller --onefile --icon=Icons/server.png --name="FDB Server" Server/server.py
```

**Build the console:**

```bash
pyinstaller --onefile --icon=Icons/console.png --name="FDB Console" Server/console.py
```

The output for each will be in the `dist/` folder.

| Flag | Description |
|---|---|
| `--onefile` | Packages everything into a single executable |
| `--windowed` | Hides the terminal window (recommended for the client only) |
| `--icon` | Sets the application icon |
| `--name` | Sets the output executable name |

> **Note:** Build the executable on the same OS you want to run it on. Windows builds `.exe`, macOS builds `.app`.

---

## 🗺️ Roadmap

- [ ] **FamilyLanChat** — Real-time LAN chat built on the same TCP foundation
- [ ] File listing (see what files are in a folder without knowing the name)
- [ ] Encrypted connections (TLS)
- [ ] Dark mode UI

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with 🐍 by <a href="https://github.com/VicentBytes">VicentBytes</a>
</p>
