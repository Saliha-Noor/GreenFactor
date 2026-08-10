"""
Authentication helpers: password hashing, session tokens, rate limiting.
Standard library implementations for PBKDF2-HMAC-SHA256 and secure tokens.
"""
import hashlib
import os
import re
import secrets
import time
from typing import Dict, Optional

from fastapi import Header, HTTPException

# --- Password hashing (PBKDF2-HMAC-SHA256) ---------------------------------

PBKDF2_ITERATIONS = 200_000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    """Returns (hash_hex, salt_hex). Generates a fresh random salt if not given."""
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return dk.hex(), salt.hex()


def verify_password(password: str, password_hash: str, password_salt: str) -> bool:
    salt = bytes.fromhex(password_salt)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return secrets.compare_digest(dk.hex(), password_hash)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def is_valid_password(password: str) -> bool:
    return len(password) >= 8


# --- Session tokens ---------------------------------------------------------

SESSION_TTL_SECONDS = 12 * 60 * 60  # 12 hours

import db

def create_session(email: str) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = time.time() + SESSION_TTL_SECONDS
    with db.get_connection() as conn:
        conn.execute("INSERT INTO sessions (token, email, expires_at) VALUES (?, ?, ?)", (token, email, expires_at))
        conn.commit()
    return token


def _get_session_email(token: str) -> Optional[str]:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email, expires_at FROM sessions WHERE token = ?", (token,))
        row = cursor.fetchone()
        if not row:
            return None
        if row["expires_at"] < time.time():
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
            return None
        return row["email"]


def get_current_user_email(authorization: Optional[str] = Header(default=None)) -> str:
    """FastAPI dependency: extracts and validates the bearer session token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization[len("Bearer "):].strip()
    email = _get_session_email(token)
    if not email:
        raise HTTPException(status_code=401, detail="Session expired or invalid, please log in again")
    return email


# --- Rate limiting (sliding window, per-IP) --------------------------------

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_ATTEMPTS = 10

# key -> list[timestamps]
_RATE_BUCKETS: Dict[str, list] = {}


def check_rate_limit(key: str) -> None:
    """Raises 429 if `key` (e.g. f"login:{client_ip}") has exceeded the
    allowed attempts in the current sliding window. Call this at the top
    of login/signup/reset-password before doing any real work."""
    now = time.time()
    bucket = _RATE_BUCKETS.setdefault(key, [])
    # drop anything outside the window
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS
    while bucket and bucket[0] < cutoff:
        bucket.pop(0)
    if len(bucket) >= RATE_LIMIT_MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="Too many attempts, please try again shortly")
    bucket.append(now)
