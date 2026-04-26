import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def clean_window(root, no=None):
    for widget in root.winfo_children():
        if no and widget in no:
            continue
        widget.destroy()

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

class class_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.title("FamilyDataBase - Loading")
        self.sideframe = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        self.destroy()
        exit()

    def start3(self, ip, user, function_of_log_out, upload, take, files):
        clean_window(self)
        self.geometry("700x500")
        self.title("FamilyDataBase - v1.2.0")

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        
        def get_files(actual_user):
            result = files(actual_user, ip)
            print(f"[DEBUG] files received: {result}")
            return result if result else ["No Files Available"]

        def take_panel(frame, actual_user):
            clean_window(frame)

            title = ctk.CTkLabel(frame, text="Take File from Server",
                                 font=ctk.CTkFont(size=16, weight="bold"))
            title.pack(pady=(20, 5), padx=10)

            file_list = get_files(actual_user)
            file_box = ctk.CTkComboBox(frame, values=file_list, width=280)
            file_box.pack(pady=10, padx=10)

            def do_take():
                selected = file_box.get()
                if not selected or selected == "No Files Available":
                    messagebox.showwarning("Family Data Base", "Please select a valid file.")
                    return
                take(actual_user, selected, ip)

            download_btn = ctk.CTkButton(frame, text="Download", command=do_take)
            download_btn.pack(pady=10, padx=10)

            def refresh():
                new_list = get_files(actual_user)
                file_box.configure(values=new_list)
                file_box.set(new_list[0])

            refresh_btn = ctk.CTkButton(frame, text="Refresh List",
                                        fg_color="#1f538d", hover_color="#14375e",
                                        command=refresh)
            refresh_btn.pack(pady=5, padx=10)

        def put_panel(frame, actual_user):
            clean_window(frame)

            title = ctk.CTkLabel(frame, text="Put File to Server",
                                 font=ctk.CTkFont(size=16, weight="bold"))
            title.pack(pady=(20, 5), padx=10)

            path_var = ctk.StringVar(value="No file selected")
            path_label = ctk.CTkLabel(frame, textvariable=path_var,
                                      wraplength=300, justify="center")
            path_label.pack(pady=5, padx=10)

            selected_path = {"value": None}

            def browse():
                filepath = filedialog.askopenfilename(title="Select a file")
                if filepath:
                    selected_path["value"] = filepath
                    path_var.set(filepath)

            browse_btn = ctk.CTkButton(frame, text="Browse File...", command=browse)
            browse_btn.pack(pady=10, padx=10)

            def do_upload():
                if not selected_path["value"]:
                    messagebox.showwarning("Family Data Base", "Please select a file first.")
                    return
                upload(actual_user, selected_path["value"], ip)

            upload_btn = ctk.CTkButton(frame, text="Upload", command=do_upload)
            upload_btn.pack(pady=10, padx=10)

        self.sideframe = ctk.CTkFrame(self, fg_color="#0d003a")
        self.sideframe.grid(column=0, row=0, sticky="nsew")

        self.mainframe = ctk.CTkFrame(self)
        self.mainframe.grid(column=1, row=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        put_button = ctk.CTkButton(self.sideframe, text="Put File",
                                   command=lambda: put_panel(self.mainframe, user))
        put_button.pack(pady=10, padx=10)

        take_button = ctk.CTkButton(self.sideframe, text="Take File",
                                    command=lambda: take_panel(self.mainframe, user))
        take_button.pack(pady=10, padx=10)

        log_out_button = ctk.CTkButton(self.sideframe, text="Log Out",
                                       command=lambda: function_of_log_out(self),
                                       fg_color="#991d1d",
                                       text_color="#000000",
                                       hover_color="#4B1313")
        log_out_button.pack(pady=10, padx=10, side="bottom")

        visible_ip = "localhost" if ip == "127.0.0.1" else ip

        user_label = ctk.CTkLabel(self.sideframe, text=f"Server IP: {visible_ip}",
                                  font=ctk.CTkFont(size=15, weight="bold"))
        user_label.pack(pady=5, padx=10, side="bottom")

        ip_label = ctk.CTkLabel(self.sideframe, text=f"Actual User: {user}",
                                font=ctk.CTkFont(size=15, weight="bold"))
        ip_label.pack(pady=5, padx=10, side="bottom")


    def start2(self, login, user, password):
        clean_window(self)
        ip_label = ctk.CTkLabel(self, text="Enter IPv4's Server")
        ip_label.grid(row=1, column=1)
        ip_entry = ctk.CTkEntry(self)
        ip_entry.grid(row=2, column=1)
        connect_button = ctk.CTkButton(self, text="Connect to the Server",
            command=lambda: login(ip_entry.get(), user, password)
            )
        connect_button.grid(row=4, column=1)

    def start1(self, login):
        clean_window(self)
        self.geometry("300x200")
        self.title("Login Screen")
        self.resizable(False, False)

        self.rowconfigure((0,1,2,3,4), weight=1)
        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, weight=2)

        user_entry = ctk.CTkEntry(self, placeholder_text="Enter your User")
        user_entry.grid(row=1, column=1, sticky="ew", padx=10)

        password_entry = ctk.CTkEntry(self, placeholder_text="Enter your Password", show="*")
        password_entry.grid(row=3, column=1, sticky="ew", padx=10)

        def prestart_phase2():
            user = user_entry.get()
            password = password_entry.get()
            if user and password:
                self.start2(login, user, password)
            else:
                error("User/Password")

        login_button = ctk.CTkButton(self, text="Login", command=prestart_phase2)
        login_button.grid(row=4, column=1, pady=10)

def test_login():
    print("hello")

if __name__ == "__main__":
    gui = class_GUI()
    gui.start1(test_login)
    gui.mainloop()