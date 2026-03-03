from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

def start1(on_connect):
    global root
    root = Tk()
    root.geometry("300x200")
    root.title("Family Data Base")
    root.config(bg="#3F4D6C")

    Label(root, text="Welcome to Family Data Base!", font=("Arial", 10), bg="#3F4D6C", fg="white").place(x=150, y=15, anchor=CENTER)
    Label(root, text="Enter the server's IPv4", bg="#3F4D6C", fg="white").place(x=150, y=50, anchor=CENTER)

    entry_ip = Entry(root)
    entry_ip.place(x=150, y=70, anchor=CENTER)

    def connect():
        ip = entry_ip.get().strip()
        if ip == "":
            messagebox.showerror("Family Data Base", "[Error 2]: You must enter a valid IPv4 address")
        else:
            start2(on_connect, ip)

    Button(root, text="Continue", command=connect).place(x=150, y=120, anchor=CENTER)
    root.bind("<KeyPress-Return>", lambda e: connect())
    root.mainloop()


def start2(on_login, ip):
    global root
    global username
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text=f"Connecting to {ip}", bg="#3F4D6C", fg="white").place(x=150, y=20, anchor=CENTER)

    Label(root, text="Enter your username", bg="#3F4D6C", fg="white").place(x=150, y=60, anchor=CENTER)
    entry_username = Entry(root)
    entry_username.place(x=150, y=80, anchor=CENTER)

    Label(root, text="Enter your password", bg="#3F4D6C", fg="white").place(x=150, y=110, anchor=CENTER)
    entry_password = Entry(root, show="*")
    entry_password.place(x=150, y=130, anchor=CENTER)

    def submit_login():
        global username
        username = entry_username.get()
        password = entry_password.get()
        if username.strip() == "" or password.strip() == "":
            messagebox.showerror("Family Data Base", "[Error 4]: Username and password are required")
            return
        on_login(ip, username, password)

    Button(root, text="Login", command=submit_login).place(x=150, y=160, anchor=CENTER)
    root.bind("<KeyPress-Return>", lambda e: submit_login())


def start3(on_download, on_upload):
    global root
    global username
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="User/destination folder (required when uploading)", bg="#3F4D6C", fg="white").place(x=5, y=5)
    Label(root, text="Target file (required when downloading)", bg="#3F4D6C", fg="white").place(x=5, y=45)

    entry_user = Entry(root)
    entry_user.place(x=5, y=25)
    entry_file = Entry(root)
    entry_file.place(x=5, y=65)

    def download():
        user = entry_user.get().strip()
        file = entry_file.get().strip()

        if username != "admin":
            if user == "":
                messagebox.showerror("Family Data Base", "[Error 8]: You must enter a username")
                return
            if username != user and user != "global":
                messagebox.showerror("Family Data Base", "[Error 9]: You cannot do this with your username")
                return
            if file == "":
                messagebox.showerror("Family Data Base", "[Error 10]: You must enter a file name")
                return

        on_download(user, file)

    def upload():
        global username
        user = entry_user.get().strip()

        if user == "":
            messagebox.showerror("Family Data Base", "[Error 8]: You must enter a username")
            return
        if user != username and user != "global":
            messagebox.showerror("Family Data Base", "[Error 9]: You cannot do this with your username")
            return

        filepath = filedialog.askopenfilename(title="Select a file to upload to the server")
        if filepath:
            on_upload(user, filepath)

    Button(root, text="Download (GET)", command=download).place(x=10, y=100)
    Button(root, text="Upload (PUT)", command=upload).place(x=130, y=100)


def error(code: str) -> None:
    messages = {
        "Timeout":      "[Error 1]: Connection timed out",
        "User/Password":"[Error 3]: Invalid username or password",
        "InvalidAddr":  "[Error 5]: Invalid IPv4 address",
        "ServerDown":   "[Error 6]: Server is not listening on that port or is offline",
        "FileNotFound": "[Error 7]: File not found",
    }
    msg = messages.get(code, "[Error ???]: Unspecified error")
    messagebox.showerror("Family Data Base", msg)


def info(msg: str) -> None:
    messagebox.showinfo("Family Data Base", msg)