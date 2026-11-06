"""Tkinter screens: login, register, and the main menu shell."""
import tkinter as tk
from tkinter import messagebox, ttk

import auth


class App(tk.Tk):
    """Main window. Holds all screens stacked on top of each other."""

    def __init__(self):
        super().__init__()
        self.title("SIA 2 Lab Project")
        self.geometry("420x360")
        self.minsize(380, 340)
        self.current_user = None

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.frames = {}
        for screen in (LoginFrame, RegisterFrame, MainFrame):
            frame = screen(container, self)
            self.frames[screen] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(LoginFrame)

    def show(self, screen):
        """Bring one screen to the front."""
        frame = self.frames[screen]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=30)
        self.app = app
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Login", font=("Arial", 20, "bold")).grid(pady=(0, 20))

        ttk.Label(self, text="Username").grid(sticky="w")
        self.username = ttk.Entry(self)
        self.username.grid(sticky="ew", pady=(0, 10))

        ttk.Label(self, text="Password").grid(sticky="w")
        self.password = ttk.Entry(self, show="*")
        self.password.grid(sticky="ew", pady=(0, 20))

        ttk.Button(self, text="Log in", command=self.login).grid(sticky="ew")
        ttk.Button(
            self, text="Create an account", command=lambda: app.show(RegisterFrame)
        ).grid(sticky="ew", pady=(10, 0))

        # Pressing Enter in either box also logs in.
        self.username.bind("<Return>", lambda e: self.login())
        self.password.bind("<Return>", lambda e: self.login())

    def on_show(self):
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.username.focus()

    def login(self):
        ok, message = auth.login_user(self.username.get(), self.password.get())
        if ok:
            self.app.current_user = self.username.get().strip()
            self.app.show(MainFrame)
        else:
            messagebox.showerror("Login failed", message)
            self.password.delete(0, tk.END)


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=30)
        self.app = app
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Register", font=("Arial", 20, "bold")).grid(pady=(0, 20))

        ttk.Label(self, text="Username").grid(sticky="w")
        self.username = ttk.Entry(self)
        self.username.grid(sticky="ew", pady=(0, 10))

        ttk.Label(self, text="Password").grid(sticky="w")
        self.password = ttk.Entry(self, show="*")
        self.password.grid(sticky="ew", pady=(0, 10))

        ttk.Label(self, text="Confirm password").grid(sticky="w")
        self.confirm = ttk.Entry(self, show="*")
        self.confirm.grid(sticky="ew", pady=(0, 20))

        ttk.Button(self, text="Create account", command=self.register).grid(sticky="ew")
        ttk.Button(
            self, text="Back to login", command=lambda: app.show(LoginFrame)
        ).grid(sticky="ew", pady=(10, 0))

        self.confirm.bind("<Return>", lambda e: self.register())

    def on_show(self):
        for entry in (self.username, self.password, self.confirm):
            entry.delete(0, tk.END)
        self.username.focus()

    def register(self):
        if self.password.get() != self.confirm.get():
            messagebox.showerror("Register", "Passwords do not match.")
            return
        ok, message = auth.register_user(self.username.get(), self.password.get())
        if ok:
            messagebox.showinfo("Register", message)
            self.app.show(LoginFrame)
        else:
            messagebox.showerror("Register", message)


class MainFrame(ttk.Frame):
    """Placeholder main screen. The chosen utility(ies) will go here."""

    def __init__(self, parent, app):
        super().__init__(parent, padding=30)
        self.app = app
        self.columnconfigure(0, weight=1)

        self.welcome = ttk.Label(self, text="", font=("Arial", 16, "bold"))
        self.welcome.grid(pady=(0, 10))

        ttk.Label(self, text="Utilities will go here.").grid(pady=(0, 20))

        ttk.Button(self, text="Log out", command=self.logout).grid(sticky="ew")

    def on_show(self):
        self.welcome.config(text=f"Welcome, {self.app.current_user}!")

    def logout(self):
        self.app.current_user = None
        self.app.show(LoginFrame)