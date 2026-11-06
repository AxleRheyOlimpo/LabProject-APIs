"""Authentication logic: registration and login with salted password hashing.

No Tkinter code in here, so it can be tested on its own.
"""
import hashlib
import hmac
import os
import re
import sqlite3
from contextlib import closing

from db import get_connection

# PBKDF2 is deliberately slow to make password guessing harder.
# The iteration count is stored per user, so it can be raised later
# without breaking existing accounts. Lower it only if logins feel too slow.
ITERATIONS = 600_000

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,30}$")
MIN_PASSWORD_LENGTH = 8


def hash_password(password, salt=None, iterations=ITERATIONS):
    """Return (salt, hash). A new random salt is made if none is given."""
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return salt, digest


def register_user(username, password):
    """Create an account. Returns (success, message)."""
    username = username.strip()

    if not USERNAME_RE.match(username):
        return False, "Username must be 3-30 characters: letters, numbers, underscore."
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."

    salt, digest = hash_password(password)
    try:
        with closing(get_connection()) as conn, conn:
            conn.execute(
                "INSERT INTO users (username, salt, password_hash, iterations) "
                "VALUES (?, ?, ?, ?)",
                (username, salt, digest, ITERATIONS),
            )
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    return True, "Account created. You can log in now."


def login_user(username, password):
    """Check credentials. Returns (success, message)."""
    username = username.strip()
    if not username or not password:
        return False, "Please enter your username and password."

    with closing(get_connection()) as conn:
        row = conn.execute(
            "SELECT salt, password_hash, iterations FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None:
        # Hash anyway so a missing user takes about as long as a wrong password.
        hash_password(password)
        return False, "Invalid username or password."

    _, digest = hash_password(password, row["salt"], row["iterations"])
    if hmac.compare_digest(digest, row["password_hash"]):
        return True, "Login successful."
    return False, "Invalid username or password."