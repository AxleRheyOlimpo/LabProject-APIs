"""Run this file to start the app."""
from db import init_db
from gui import App


def main():
    init_db()
    App().mainloop()


if __name__ == "__main__":
    main()