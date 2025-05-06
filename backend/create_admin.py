import sqlite3
from app.core.security import get_password_hash
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_admin_user(conn, cursor):
    cursor.execute("DELETE FROM users WHERE email = ?", ("admin@example.com",))

    hashed_password = get_password_hash("adminpassword")
    cursor.execute(
        "INSERT INTO users (email, hashed_password, role, is_verified) VALUES (?, ?, ?, ?)",
        ("admin@example.com", hashed_password, "admin", 1),
    )
    conn.commit()
    logger.info("Admin user created: admin@example.com / adminpassword")


conn = sqlite3.connect("database.db")
cursor = conn.cursor()
max_retries = 5
retry_delay = 2  # seconds

for attempt in range(max_retries):
    try:
        create_admin_user(conn, cursor)
        break
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e).lower():
            logger.warning(
                f"Database locked, attempt {attempt + 1}/{max_retries}. Retrying in {retry_delay} seconds..."
            )
            time.sleep(retry_delay)
        else:
            logger.error(f"Database error: {e}")
            conn.rollback()
            raise
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        conn.rollback()
        raise
else:
    logger.error("Failed to create admin user after maximum retries.")
    conn.rollback()

conn.close()
