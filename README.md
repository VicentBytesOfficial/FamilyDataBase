# 🗄️ FamilyDataBase

A lightweight LAN file transfer system built with Python. Allows multiple users to upload and download files across a local network through a simple graphical interface.

> **Part of the Family Suite** — a collection of LAN tools built with Python.
> Next project: [FamilyLanChat](https://gitlab.com/tv-team) — real-time LAN chat.

[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://gitlab.com/tv-team/familydatabase/-/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

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
- [Admin User](#-admin-user)
- [Technical Info](#-technical-info)
- [Building an Executable](#-building-an-executable)
- [Known Issues](#-known-issues)
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
- 📦 Can be built as a standalone `.exe` (Windows) or `.app` (macOS) — no Python required

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
│   ├── client.png      # Icon for the client (source)
│   ├── server.png      # Icon for the server (source)
│   └── console.png     # Icon for the console (source)
├── DataClient/         # Files downloaded by the client are saved here (auto-created)
└── DataServer/         # Server-side file storage (auto-created)
    ├── users.json      # Registered users (auto-created)
    └── global/         # Shared folder accessible by all users (auto-created)
```

> **Note:** `DataClient/` and `DataServer/` are created automatically on first run. They are excluded from version control via `.gitignore`.

---

## ⚙️ Requirements

- Python 3.10 or higher
- Tkinter (included with Python on Windows and macOS)
- Both devices must be on the **same local network (LAN)**
- Port `5000` open on the server machine (not blocked by firewall)

No external libraries required — only Python's standard library.

> **Want to run it without Python?** You can build a standalone `.exe` (Windows) or `.app` (macOS) using PyInstaller. See [Building an Executable](#-building-an-executable).

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://gitlab.com/tv-team/familydatabase.git
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

> **Firewall:** Make sure port `5000` is allowed through your firewall. On Windows, you may get a prompt asking to allow access — click **Allow**.

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
| `add <username> <password>` | Add a new user and create their folder |
| `remove <username>` | Remove a user and delete all their files |
| `changepassword <username> <new_password>` | Change a user's password |
| `help` | Show available commands |
| `exit` / `quit` | Exit the console |

**Example — setting up for the first time:**

```
>>> changepassword admin mysecurepassword
[OK] Password for 'admin' has been updated.

>>> add john mypassword123
[OK] User 'john' added successfully.

>>> add mary anotherpassword
[OK] User 'mary' added successfully.

>>> list
Registered users (3):
  - admin
  - john
  - mary
```

---

### Running the Client

On any machine in the same network, run:

```bash
python Client/client.py
```

**Step 1 — Enter the server's IP:**

Type the local IP address of the server machine (e.g. `192.168.1.10`) and click **Continue**. You can also type `localhost` if you are on the same machine as the server.

**Step 2 — Login:**

Enter your username and password, then click **Login**.

**Step 3 — Transfer files:**

- **Download (GET):** Enter a username/folder and a filename, then click **Download**.
- **Upload (PUT):** Enter a username/folder, click **Upload**, and select a file from your computer.

> Files you download are saved to the `DataClient/` folder automatically, located next to the client executable or script.

#### Folder access rules:

| User type | Can access | Can upload to |
|---|---|---|
| Regular user | Their own folder + `global/` | Their own folder + `global/` |
| `admin` | All folders | All folders |

---

## 🔑 Admin User

FamilyDataBase includes a built-in **`admin`** user with elevated privileges:

- Can **download from any user's folder**, not just their own or `global/`
- Can **upload to any user's folder**
- Is the only user that can bypass folder access restrictions

**Default credentials:**
| Field | Value |
|---|---|
| Username | `admin` |
| Password | `password` |

> ⚠️ **Security warning:** Change the admin password immediately after setup using:
> ```
> >>> changepassword admin <your_new_password>
> ```
> Leaving the default password on a network exposes all files to anyone who tries to connect.

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
| External dependencies | None |

**How file transfer works:**

1. Client connects to server via TCP socket
2. Client sends a command line: `GET;username;filename` or `PUT;username;filename`
3. For downloads: server responds with filesize, then streams raw bytes
4. For uploads: client sends filesize, then streams raw bytes
5. Server responds with `OK` or `ERROR`
6. Connection closes after each operation

**How authentication works:**

1. Client sends `LOGIN;username;password`
2. Server looks up the username in `users.json` and compares the password
3. Server responds with `OK` or `FAIL`
4. If `OK`, the client UI unlocks the file transfer screen

---

## 📦 Building an Executable

FamilyDataBase can be converted into standalone executables (`.exe` on Windows, `.app` on macOS) using [PyInstaller](https://pyinstaller.org/). No Python installation required on the target machine.

**Install PyInstaller:**

```bash
pip install pyinstaller
```

**Build the client:**

```bash
pyinstaller --onefile --windowed --icon=Icons/client.ico --name="Family Data Base" Client/client.py
```

**Build the server:**

```bash
pyinstaller --onefile --icon=Icons/server.ico --name="FDB Server" Server/server.py
```

**Build the console:**

```bash
pyinstaller --onefile --icon=Icons/console.ico --name="FDB Console" Server/console.py
```

The output for each will be in the `dist/` folder. Once built, place all executables in the same folder for them to work correctly:

```
YourFolder/
├── Family Data Base.exe    # Client
├── FDB Server.exe          # Server
├── FDB Console.exe         # Admin console
├── DataClient/             # Auto-created on first client run
└── DataServer/             # Auto-created on first server run
    ├── users.json          # Auto-created
    └── global/             # Auto-created
```

> **Note:** `DataClient/` and `DataServer/` are generated automatically the first time you run the executables. You don't need to create them manually.

| Flag | Description |
|---|---|
| `--onefile` | Packages everything into a single executable |
| `--windowed` | Hides the terminal window (recommended for the client only) |
| `--icon` | Sets the application icon |
| `--name` | Sets the output executable name |

> **Note:** Build the executable on the same OS you want to run it on. Windows builds `.exe`, macOS builds `.app`.

> **Icons:** Convert your `.png` icons to `.ico` (Windows) using a tool like [icoconvert.com](https://icoconvert.com), or to `.icns` (macOS) using Preview. Place the converted files in the `Icons/` folder before building.

---

## 🐛 Known Issues

- **Passwords are stored in plain text** in `users.json`. Avoid using sensitive passwords until encryption is added in a future release.
- **No transfer progress indicator** — large files will transfer without showing progress.
- **Single connection at a time** — the server handles one client at a time. Multiple simultaneous connections are planned for a future release.

---

## 🗺️ Roadmap

- [ ] **FamilyLanChat** — Real-time LAN chat built on the same TCP foundation
- [ ] File listing (see what files are in a folder without knowing the filename)
- [ ] Transfer progress bar with speed indicator (MB/s)
- [ ] Multiple simultaneous connections (threading)
- [ ] Encrypted connections (TLS)
- [ ] Password hashing (bcrypt)
- [ ] Dark mode UI with CustomTkinter
- [ ] GitHub Actions to auto-build executables on each release

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with 🐍 by <a href="https://gitlab.com/tv-team">VicentBytes</a>
</p>
