import sqlite3
import bcrypt

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# CREATE USERS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password BLOB
)
""")

conn.commit()

# =========================
# CREATE USER
# =========================

def create_user(username, password):

    # =========================
    # VALIDATION
    # =========================

    username = username.strip()

    if len(username) < 3:
        return False, "Username too short"

    if len(password) < 6:
        return False, "Password must be at least 6 characters"

    # =========================
    # HASH PASSWORD
    # =========================

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    # =========================
    # INSERT USER
    # =========================

    try:

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (
                username,
                hashed_password
            )
        )

        conn.commit()

        return True, "Account created successfully"

    except sqlite3.IntegrityError:

        return False, "Username already exists"

    except Exception as e:

        return False, str(e)

# =========================
# LOGIN USER
# =========================

def login_user(username, password):

    try:

        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        result = cursor.fetchone()

        # =========================
        # USER EXISTS
        # =========================

        if result:

            stored_password = result[0]

            if bcrypt.checkpw(
                password.encode(),
                stored_password
            ):

                return True

        return False

    except:

        return False

# =========================
# CHECK USER EXISTS
# =========================

def user_exists(username):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()

    return result is not None

# =========================
# GET ALL USERS
# =========================

def get_all_users():

    cursor.execute(
        """
        SELECT username
        FROM users
        """
    )

    users = cursor.fetchall()

    return [user[0] for user in users]

# =========================
# DELETE USER
# =========================

def delete_user(username):

    try:

        cursor.execute(
            """
            DELETE FROM users
            WHERE username=?
            """,
            (username,)
        )

        conn.commit()

        return True

    except:

        return False

# =========================
# CLOSE DATABASE
# =========================

def close_connection():

    conn.close()