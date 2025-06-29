import sqlite3
import hashlib

def register_user(username, password, role):
    conn = sqlite3.connect("users.db")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
