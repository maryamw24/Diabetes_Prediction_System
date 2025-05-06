import sqlite3
from datetime import datetime
import json

DATABASE = "database.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            is_verified BOOLEAN DEFAULT 0,
            is_banned BOOLEAN DEFAULT 0,
            verification_code TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Create prediction_logs table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            input_data TEXT,
            prediction TEXT,
            probability REAL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """
    )

    conn.commit()
    conn.close()


def get_user_by_email(email: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "email": user[1],
            "hashed_password": user[2],
            "role": user[3],
            "is_verified": bool(user[4]),
            "is_banned": bool(user[5]),
            "verification_code": user[6],
            "created_at": user[7],
        }
    return None


def create_user(email: str, hashed_password: str, verification_code: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (email, hashed_password, verification_code) VALUES (?, ?, ?)",
        (email, hashed_password, verification_code),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def verify_user(email: str, code: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if user["verification_code"] != code:
        return False
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_verified = 1, verification_code = NULL WHERE email = ?",
        (email,),
    )
    conn.commit()
    conn.close()
    return True


def update_verification_code(email: str, code: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET verification_code = ? WHERE email = ?", (code, email)
    )
    conn.commit()
    conn.close()


def log_prediction(user_id: int, input_data: dict, prediction: str, probability: float):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prediction_logs (user_id, input_data, prediction, probability) VALUES (?, ?, ?, ?)",
        (user_id, json.dumps(input_data), prediction, probability),
    )
    conn.commit()
    conn.close()


def get_todays_logs():
    today = datetime.now().date().isoformat()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prediction_logs WHERE date(timestamp) = ?", (today,))
    logs = cursor.fetchall()
    conn.close()
    return [
        {
            "id": log[0],
            "user_id": log[1],
            "input_data": log[2],
            "prediction": log[3],
            "probability": log[4],
            "timestamp": log[5],
        }
        for log in logs
    ]


def get_new_users():
    today = datetime.now().date().isoformat()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE date(created_at) = ?", (today,))
    users = cursor.fetchall()
    conn.close()
    return [
        {
            "id": user[0],
            "email": user[1],
            "role": user[3],
            "is_verified": bool(user[4]),
            "is_banned": bool(user[5]),
        }
        for user in users
    ]


def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return [
        {
            "id": user[0],
            "email": user[1],
            "role": user[3],
            "is_verified": bool(user[4]),
            "is_banned": bool(user[5]),
        }
        for user in users
    ]


def ban_user(user_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_banned = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
