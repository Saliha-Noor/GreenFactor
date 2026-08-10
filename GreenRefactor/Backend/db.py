import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "greenrefactor.db")

def get_connection():
    # check_same_thread=False allows FastAPI to use this across async workers
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        name TEXT,
                        role TEXT,
                        organization TEXT,
                        tdp_watts TEXT,
                        password_hash TEXT,
                        password_salt TEXT)''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        token TEXT PRIMARY KEY,
                        email TEXT,
                        expires_at REAL)''')
        
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", ("dev@greenrefactor.org",))
        if not cursor.fetchone():
            import auth
            pw_hash, pw_salt = auth.hash_password("greenrefactor-dev")
            conn.execute("INSERT INTO users (email, name, role, organization, tdp_watts, password_hash, password_salt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        ("dev@greenrefactor.org", "Dr. Alex Vance", "Lead Researcher", "Green Compute Initiative", "15", pw_hash, pw_salt))
        conn.commit()

# Automatically init DB when imported
init_db()
