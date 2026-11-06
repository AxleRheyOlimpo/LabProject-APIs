"""Tkinter screens: login, register, and the main app shell.

Layout of the main screen:
    [ top navbar: brand | page buttons | user + log out ]
    [ page area ]
Each navbar button opens one "container" (a page). The three utility
containers are empty on purpose: build your feature inside the build()
method of its class (look for the "BUILD YOUR FEATURE HERE" comments).
"""
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

import auth

APP_NAME = "Xel's Lair"

# ---------------------------------------------------------------------------
# Look and feel. Change a color here and the whole app follows.
# Text/background pairs were chosen to pass WCAG AA contrast (4.5:1 or better).
# ---------------------------------------------------------------------------
BG = "#f6f4ef"             # warm off-white window background (softer than pure white)
CARD = "#ffffff"           # forms and cards
ACCENT = "#0b7f71"         # deep teal: main buttons
ACCENT_DARK = "#086357"    # hover / pressed / busy
AMBER = "#f5a524"          # highlight: active page underline
NAV = "#16202e"            # deep ink navbar
NAV_HOVER = "#243246"
NAV_TEXT = "#c7d0dc"
NAV_MUTED = "#9aa6b8"
TEXT = "#1b2433"
MUTED = "#5b6472"
BORDER = "#9aa3b2"         # checkbox / input outline
ERROR = "#c62828"
SUCCESS = "#1b7f3b"

# Bahnschrift ships with Windows 10/11. If it is missing, the first font
# that exists in this list is used instead.
FONT_CHOICES = ("Bahnschrift", "Segoe UI", "Arial")
FONT = "Arial"             # replaced by pick_font() once the window exists


def pick_font(root):
    """Return the first installed font from FONT_CHOICES."""
    installed = set(tkfont.families(root))
    for name in FONT_CHOICES:
        if name in installed:
            return name
    return "Arial"


def make_check_images(root):
    """Draw the checkbox pictures in code (no image files needed).

    Unchecked = empty white box. Checked = teal box with a white check mark.
    """
    size = 18
    off = tk.PhotoImage(master=root, width=size, height=size)
    off.put(BORDER, to=(0, 0, size, size))
    off.put("white", to=(1, 1, size - 1, size - 1))

    on = tk.PhotoImage(master=root, width=size, height=size)
    on.put(ACCENT, to=(0, 0, size, size))
    tick = [(4, 9), (5, 10), (6, 11), (7, 12), (8, 11), (9, 10),
            (10, 9), (11, 8), (12, 7), (13, 6)]
    for x, y in tick:
        on.put("white", to=(x, y, x + 2, y + 2))
    return off, on


def setup_style(root):
    """One place for all ttk styling."""
    global FONT
    FONT = pick_font(root)

    # Make every default widget font use it too (entry boxes, etc.).
    for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont"):
        tkfont.nametofont(name).configure(family=FONT)

    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg=BG)

    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD)

    style.configure("TLabel", background=BG, foreground=TEXT, font=(FONT, 10))
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=(FONT, 10))
    style.configure("PageTitle.TLabel", background=BG, font=(FONT, 18, "bold"))
    style.configure("Card.TLabel", background=CARD, foreground=TEXT, font=(FONT, 10))
    style.configure("CardTitle.TLabel", background=CARD, font=(FONT, 13, "bold"))
    style.configure("Title.TLabel", background=CARD, font=(FONT, 22, "bold"))
    style.configure("Sub.TLabel", background=CARD, foreground=MUTED, font=(FONT, 10))
    style.configure("Hint.TLabel", background=CARD, foreground=MUTED, font=(FONT, 9))
    style.configure("StatLabel.TLabel", background=CARD, foreground=MUTED, font=(FONT, 9))
    style.configure("StatValue.TLabel", background=CARD, foreground=TEXT, font=(FONT, 14, "bold"))
    style.configure("Error.TLabel", background=CARD, foreground=ERROR, font=(FONT, 10))
    style.configure("Success.TLabel", background=CARD, foreground=SUCCESS, font=(FONT, 10))

    style.configure("TEntry", padding=7, fieldbackground="white", bordercolor=BORDER,
                    lightcolor=BORDER, darkcolor=BORDER)
    style.map("TEntry", bordercolor=[("focus", ACCENT)], lightcolor=[("focus", ACCENT)],
              darkcolor=[("focus", ACCENT)])

    # Checkbox that shows a check mark (the default theme draws an X).
    # Keep a reference to the images, or Tk throws them away.
    root._check_off, root._check_on = make_check_images(root)
    style.element_create(
        "Lair.check", "image", root._check_off, ("selected", root._check_on),
        width=26, sticky="w",
    )
    style.layout("Card.TCheckbutton", [
        ("Checkbutton.padding", {"sticky": "nswe", "children": [
            ("Lair.check", {"side": "left", "sticky": ""}),
            ("Checkbutton.label", {"side": "left", "sticky": ""}),
        ]})
    ])
    style.configure("Card.TCheckbutton", background=CARD, foreground=TEXT, font=(FONT, 10))
    style.map("Card.TCheckbutton", background=[("active", CARD)])

    style.configure(
        "Accent.TButton", background=ACCENT, foreground="white",
        font=(FONT, 11, "bold"), padding=9, borderwidth=0, focuscolor=ACCENT,
    )
    style.map(
        "Accent.TButton",
        background=[("disabled", ACCENT_DARK), ("active", ACCENT_DARK)],
        foreground=[("disabled", "white")],
    )
    style.configure(
        "Link.TButton", background=CARD, foreground=ACCENT,
        font=(FONT, 10, "underline"), padding=2, borderwidth=0, focuscolor=CARD,
    )
    style.map(
        "Link.TButton",
        background=[("active", CARD)],
        foreground=[("active", ACCENT_DARK)],
    )


class App(tk.Tk):
    """Main window. Holds all screens stacked on top of each other."""

    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.current_user = None
        setup_style(self)

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

    def center(self, width, height):
        """Resize the window and put it near the middle of the screen."""
        self.update_idletasks()
        width = min(width, self.winfo_screenwidth() - 40)
        height = min(height, self.winfo_screenheight() - 80)
        x = (self.winfo_screenwidth() - width) // 2
        y = max((self.winfo_screenheight() - height) // 3, 0)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show(self, screen, message=None, kind="error"):
        """Bring one screen to the front. Each screen picks its own window size."""
        frame = self.frames[screen]
        self.minsize(*frame.min_size)
        self.center(*frame.size)
        if hasattr(frame, "on_show"):
            frame.on_show()
        if message and hasattr(frame, "set_message"):
            frame.set_message(message, kind)
        frame.tkraise()


# ---------------------------------------------------------------------------
# Login and register
# ---------------------------------------------------------------------------
class AuthFrame(ttk.Frame):
    """Shared layout for the login and register screens: a centered white card."""

    size = (440, 520)
    min_size = (400, 480)

    def __init__(self, parent, app, title, subtitle=None):
        super().__init__(parent)
        self.app = app
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.card = ttk.Frame(self, style="Card.TFrame", padding=(32, 28))
        self.card.grid(row=0, column=0, padx=24, pady=24)

        ttk.Label(self.card, text=title, style="Title.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(self.card, text=subtitle, style="Sub.TLabel").pack(anchor="w", pady=(2, 0))

        # Messages appear here (errors in red, success in green) instead of popups.
        self.message = ttk.Label(
            self.card, text="", style="Error.TLabel", wraplength=300, justify="left"
        )
        self.message.pack(anchor="w", pady=(12, 6))

        self.password_entries = []

    def add_field(self, label, secret=False):
        ttk.Label(self.card, text=label, style="Card.TLabel").pack(anchor="w")
        entry = ttk.Entry(self.card, width=34, show="*" if secret else "")
        entry.pack(fill="x", pady=(2, 12))
        if secret:
            self.password_entries.append(entry)
        return entry

    def add_show_password(self):
        """A 'Show password' checkbox for every password box added so far."""
        self.show_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.card, text="Show password", variable=self.show_var,
            command=self._apply_show, style="Card.TCheckbutton", cursor="hand2",
        ).pack(anchor="w", pady=(0, 14))

    def _apply_show(self):
        for entry in self.password_entries:
            entry.config(show="" if self.show_var.get() else "*")

    def set_message(self, text, kind="error"):
        self.message.config(
            text=text, style="Success.TLabel" if kind == "success" else "Error.TLabel"
        )

    def reset(self, *entries):
        """Clear boxes, hide old messages, and hide passwords again."""
        for entry in entries:
            entry.delete(0, tk.END)
        self.set_message("")
        self.show_var.set(False)
        self._apply_show()
        entries[0].focus()

    @staticmethod
    def busy(button, text):
        """Show a 'working' state. Password hashing takes a moment on slow laptops."""
        button.config(text=text, state="disabled")
        button.update_idletasks()


class LoginFrame(AuthFrame):
    def __init__(self, parent, app):
        super().__init__(parent, app, "Welcome")

        self.username = self.add_field("Username")
        self.password = self.add_field("Password", secret=True)
        self.add_show_password()

        self.button = ttk.Button(
            self.card, text="Log in", style="Accent.TButton",
            command=self.login, cursor="hand2",
        )
        self.button.pack(fill="x")

        row = ttk.Frame(self.card, style="Card.TFrame")
        row.pack(pady=(14, 0))
        ttk.Label(row, text="No account yet?", style="Sub.TLabel").pack(side="left")
        ttk.Button(
            row, text="Create one", style="Link.TButton", cursor="hand2",
            command=lambda: app.show(RegisterFrame),
        ).pack(side="left")

        # Enter on the username box jumps to the password; Enter on the password logs in.
        self.username.bind("<Return>", lambda e: self.password.focus())
        self.password.bind("<Return>", lambda e: self.login())

    def on_show(self):
        self.reset(self.username, self.password)

    def login(self):
        username = self.username.get().strip()
        if not username or not self.password.get():
            self.set_message("Please enter your username and password.")
            return

        self.set_message("")
        self.busy(self.button, "Logging in...")
        ok, message = auth.login_user(username, self.password.get())
        self.button.config(text="Log in", state="normal")

        if ok:
            self.app.current_user = username
            self.app.show(MainFrame)
        else:
            self.set_message(message)
            self.password.delete(0, tk.END)
            self.password.focus()


class RegisterFrame(AuthFrame):
    size = (440, 660)       # taller than login: it has an extra field and a hint
    min_size = (400, 620)

    def __init__(self, parent, app):
        super().__init__(parent, app, "Create account", "It only takes a few seconds")

        self.username = self.add_field("Username")
        self.password = self.add_field("Password", secret=True)
        self.confirm = self.add_field("Confirm password", secret=True)
        self.add_show_password()

        ttk.Label(
            self.card,
            text="Username: 3-30 letters, numbers or _   |   Password: 8+ characters",
            style="Hint.TLabel", wraplength=300, justify="left",
        ).pack(anchor="w", pady=(0, 12))

        self.button = ttk.Button(
            self.card, text="Create account", style="Accent.TButton",
            command=self.register, cursor="hand2",
        )
        self.button.pack(fill="x")

        ttk.Button(
            self.card, text="Back to login", style="Link.TButton", cursor="hand2",
            command=lambda: app.show(LoginFrame),
        ).pack(pady=(10, 0))

        self.username.bind("<Return>", lambda e: self.password.focus())
        self.password.bind("<Return>", lambda e: self.confirm.focus())
        self.confirm.bind("<Return>", lambda e: self.register())

    def on_show(self):
        self.reset(self.username, self.password, self.confirm)

    def register(self):
        if self.password.get() != self.confirm.get():
            self.set_message("Passwords do not match.")
            self.confirm.delete(0, tk.END)
            self.confirm.focus()
            return

        username = self.username.get().strip()
        self.set_message("")
        self.busy(self.button, "Creating account...")
        ok, message = auth.register_user(username, self.password.get())
        self.button.config(text="Create account", state="normal")

        if ok:
            # Go back to login with a green message and the username already filled in.
            login = self.app.frames[LoginFrame]
            self.app.show(LoginFrame, message=message, kind="success")
            login.username.insert(0, username)
            login.password.focus()
        else:
            self.set_message(message)


# ---------------------------------------------------------------------------
# Main screen: top navbar + pages ("containers")
# ---------------------------------------------------------------------------
class FeaturePage(ttk.Frame):
    """A container for one feature: a title, a short description, and an empty body."""

    title = ""
    description = ""

    def __init__(self, parent, app):
        super().__init__(parent, padding=28)
        self.app = app
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text=self.title, style="PageTitle.TLabel").grid(row=0, sticky="w")
        ttk.Label(
            self, text=self.description, style="Muted.TLabel",
            wraplength=700, justify="left",
        ).grid(row=1, sticky="w", pady=(2, 16))

        self.body = ttk.Frame(self, style="Card.TFrame", padding=24)
        self.body.grid(row=2, sticky="nsew")
        self.build(self.body)

    def build(self, body):
        """Placeholder. Subclasses replace this with the real feature."""
        box = ttk.Frame(body, style="Card.TFrame")
        box.pack(expand=True)  # centers the two labels together
        ttk.Label(box, text=f"{self.title} goes here", style="CardTitle.TLabel").pack(pady=(0, 2))
        ttk.Label(box, text="This container is ready for your widgets.", style="Sub.TLabel").pack()


class ShortenerPage(FeaturePage):
    title = "URL Shortener"
    description = "Paste a long link, get a short one, and keep a history of your links."

    # def build(self, body):
    #     # BUILD YOUR FEATURE HERE: put your widgets inside `body`.
    #     ...


class MessagingPage(FeaturePage):
    title = "SMS and Email"
    description = "Send a text message or an email from inside the app."

    # def build(self, body):
    #     # BUILD YOUR FEATURE HERE: put your widgets inside `body`.
    #     ...


class FakeDataPage(FeaturePage):
    title = "Fake Data Generator"
    description = "Generate records with 10 fields (at least 10 records) and save them."

    # def build(self, body):
    #     # BUILD YOUR FEATURE HERE: put your widgets inside `body`.
    #     ...


# One entry per tool on the Home page: (page key, name, description, [(stat label, starting value), ...])
# The stat numbers are placeholders. Later, call HomePage.set_stat() to show real values.
TOOLS = [
    ("shortener", "URL Shortener", "Turn long links into short ones.",
     [("Links created", "0"), ("Last link", "-")]),
    ("messaging", "SMS and Email", "Send texts and emails from the app.",
     [("Messages sent", "0"), ("Last sent", "-")]),
    ("fakedata", "Fake Data", "Generate and store sample records.",
     [("Records saved", "0"), ("Last batch", "-")]),
]


class HomePage(ttk.Frame):
    """Landing page: a greeting and one wide row per tool."""

    def __init__(self, parent, app, open_page):
        super().__init__(parent, padding=28)
        self.columnconfigure(0, weight=1)
        self.stats = {}  # (page key, stat label) -> the Label showing the value

        self.greeting = ttk.Label(self, text="", style="PageTitle.TLabel")
        self.greeting.grid(row=0, sticky="w")
        ttk.Label(self, text="Pick a tool to get started.", style="Muted.TLabel").grid(
            row=1, sticky="w", pady=(2, 18)
        )

        for row, (key, name, blurb, stats) in enumerate(TOOLS, start=2):
            card = ttk.Frame(self, style="Card.TFrame", padding=(22, 18))
            card.grid(row=row, sticky="ew", pady=(0, 12))
            card.columnconfigure(0, weight=1)
            # Fixed-width stat columns so the numbers line up from row to row.
            for col in range(1, len(stats) + 1):
                card.columnconfigure(col, minsize=130)

            info = ttk.Frame(card, style="Card.TFrame")
            info.grid(row=0, column=0, sticky="w")
            ttk.Label(info, text=name, style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(info, text=blurb, style="Sub.TLabel").pack(anchor="w", pady=(3, 0))

            for col, (label, start) in enumerate(stats, start=1):
                box = ttk.Frame(card, style="Card.TFrame")
                box.grid(row=0, column=col, sticky="w")
                ttk.Label(box, text=label, style="StatLabel.TLabel").pack(anchor="w")
                value = ttk.Label(box, text=start, style="StatValue.TLabel")
                value.pack(anchor="w")
                self.stats[(key, label)] = value

            ttk.Button(
                card, text="Open", style="Accent.TButton", cursor="hand2",
                command=lambda k=key: open_page(k),
            ).grid(row=0, column=len(stats) + 1)

    def set_user(self, username):
        self.greeting.config(text=f"Welcome, {username}!")

    def set_stat(self, key, label, value):
        """Update a number on the Home page, e.g. set_stat("shortener", "Links created", 5)."""
        self.stats[(key, label)].config(text=str(value))


class MainFrame(ttk.Frame):
    """Navbar across the top, the selected page underneath."""

    size = (1000, 640)
    min_size = (880, 560)

    LABELS = {
        "home": "Home",
        "shortener": "URL Shortener",
        "messaging": "SMS and Email",
        "fakedata": "Fake Data",
    }

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # ----- navbar -----
        nav = tk.Frame(self, bg=NAV, height=58)
        nav.grid(row=0, sticky="ew")
        nav.pack_propagate(False)  # keep the navbar a fixed height

        tk.Label(
            nav, text=APP_NAME, bg=NAV, fg="white", font=(FONT, 15, "bold"),
        ).pack(side="left", padx=(24, 28))

        # Right side first, so it stays pinned to the edge.
        logout = tk.Button(
            nav, text="Log out", command=self.logout, relief="flat", bd=0,
            bg=NAV, fg="white", font=(FONT, 10), padx=14, pady=6,
            activebackground=NAV_HOVER, activeforeground="white",
            cursor="hand2", highlightthickness=0,
        )
        logout.pack(side="right", padx=(8, 20))
        logout.bind("<Enter>", lambda e: logout.config(bg=NAV_HOVER))
        logout.bind("<Leave>", lambda e: logout.config(bg=NAV))
        self.user_label = tk.Label(nav, text="", bg=NAV, fg=NAV_MUTED, font=(FONT, 10))
        self.user_label.pack(side="right")

        # ----- pages -----
        area = ttk.Frame(self)
        area.grid(row=1, sticky="nsew")
        area.columnconfigure(0, weight=1)
        area.rowconfigure(0, weight=1)

        self.home = HomePage(area, app, self.open)
        self.pages = {
            "home": self.home,
            "shortener": ShortenerPage(area, app),
            "messaging": MessagingPage(area, app),
            "fakedata": FakeDataPage(area, app),
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

        # ----- navbar buttons (one per page) -----
        self.buttons = {}
        self.bars = {}
        for key, label in self.LABELS.items():
            self._nav_item(nav, key, label)

    def _nav_item(self, nav, key, label):
        """One navbar button with a thin underline that lights up when selected."""
        wrap = tk.Frame(nav, bg=NAV)
        wrap.pack(side="left", fill="y")

        bar = tk.Frame(wrap, bg=NAV, height=3)
        bar.pack(side="bottom", fill="x")
        btn = tk.Button(
            wrap, text=label, command=lambda: self.open(key), relief="flat", bd=0,
            bg=NAV, fg=NAV_TEXT, font=(FONT, 11), padx=18,
            activebackground=NAV_HOVER, activeforeground="white",
            cursor="hand2", highlightthickness=0,
        )
        btn.pack(fill="both", expand=True)

        btn.bind("<Enter>", lambda e: self._hover(key, True))
        btn.bind("<Leave>", lambda e: self._hover(key, False))
        self.buttons[key] = btn
        self.bars[key] = bar

    def _hover(self, key, inside):
        if key != self.current:  # don't recolor the selected item
            self.buttons[key].config(bg=NAV_HOVER if inside else NAV)

    def open(self, key):
        """Show one page and highlight its navbar button."""
        self.current = key
        self.pages[key].tkraise()
        for name, btn in self.buttons.items():
            active = name == key
            btn.config(bg=NAV, fg="white" if active else NAV_TEXT)
            self.bars[name].config(bg=AMBER if active else NAV)

    def on_show(self):
        self.user_label.config(text=f"Signed in as {self.app.current_user}")
        self.home.set_user(self.app.current_user)
        self.open("home")

    def logout(self):
        self.app.current_user = None
        self.app.show(LoginFrame, message="You have been logged out.", kind="success")