# ===============================================================
# Isekai Online - SQLite Database Manager (Accounts + Players)
# ===============================================================

import sqlite3
from pathlib import Path
import bcrypt


DB_FILE = Path(__file__).resolve().parent / "isekai_online.db"


def hash_password(password: str) -> str:
    """Return bcrypt hash of a string."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


class Database:
    """SQLite helper: player persistence and account management."""

    def __init__(self):
        # Use a connection per thread approach using thread local storage
        self.connections = {}
        self.create_tables()

    def _get_connection(self):
        """Get a thread-local database connection."""
        import threading
        thread_id = threading.get_ident()
        
        if thread_id not in self.connections:
            self.connections[thread_id] = sqlite3.connect(DB_FILE)
        return self.connections[thread_id]
    
    def _execute_query(self, query, params=None):
        """Execute a query safely."""
        conn = self._get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def _commit(self):
        """Commit on current thread connection."""
        conn = self._get_connection()
        conn.commit()
    
    # -----------------------------------------------------------
    # Table Setup
    # -----------------------------------------------------------
    def create_tables(self):
        # Using _execute_query for each statement for thread safety
        self._execute_query(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                username TEXT PRIMARY KEY,
                password TEXT,
                player_id TEXT
            )
            """
        )
        self._execute_query(
            """
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
                class TEXT,
                level INTEGER,
                xp INTEGER,
                hp INTEGER,
                max_hp INTEGER
            )
            """
        )
        self._commit()

    # -----------------------------------------------------------
    # Account Management
    # -----------------------------------------------------------
    def create_account(self, username: str, password: str, player_id: str):
        """Registers a new account."""
        self.cursor.execute(
            "INSERT INTO accounts (username, password, player_id) VALUES (?, ?, ?)",
            (username, hash_password(password), player_id),
        )
        self.conn.commit()

    def account_exists(self, username: str) -> bool:
        cursor = self._execute_query("SELECT username FROM accounts WHERE username=?", (username,))
        return cursor.fetchone() is not None

    def verify_login(self, username: str, password: str):
        """Check credentials and return linked player_id if valid."""
        cursor = self._execute_query(
            "SELECT player_id, password FROM accounts WHERE username=?", (username,)
        )
        row = cursor.fetchone()
        if not row:
            return None  # username not found
        player_id, stored_hash = row
        # bcrypt needs the stored hash (which contains the salt) to verify
        password_bytes = password.encode('utf-8')
        stored_hash_bytes = stored_hash.encode('utf-8')
        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            return player_id
        return None

    # -----------------------------------------------------------
    # Player Management
    # -----------------------------------------------------------
    def save_player(self, player_id, data):
        self._execute_query(
            """
            INSERT INTO players (id, class, level, xp, hp, max_hp)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                class=excluded.class,
                level=excluded.level,
                xp=excluded.xp,
                hp=excluded.hp,
                max_hp=excluded.max_hp
            """,
            (
                player_id,
                data.get("class", "warrior"),
                data.get("lvl", 1),
                data.get("xp", 0),
                data.get("hp", 100),
                data.get("max_hp", 100),
            ),
        )
        self._commit()

    def load_player(self, player_id):
        cursor = self._execute_query("SELECT * FROM players WHERE id=?", (player_id,))
        row = cursor.fetchone()
        if not row:
            return None
        (_, cls, lvl, xp, hp, max_hp) = row
        return {
            "class": cls,
            "lvl": lvl,
            "xp": xp,
            "hp": hp,
            "max_hp": max_hp,
        }

    def delete_player(self, player_id):
        self._execute_query("DELETE FROM players WHERE id=?", (player_id,))
        self._commit()

    def close(self):
        """Close all thread connections."""
        for conn in self.connections.values():
            try:
                conn.close()
            except Exception:
                pass
        self.connections.clear()


if __name__ == "__main__":
    # Simple manual test of accounts and players
    db = Database()
    username = "Hero42"
    password = "swordfish"
    if not db.account_exists(username):
        db.create_account(username, password, "abcd")
        print("Account created for", username)
    pid = db.verify_login(username, password)
    print("Login verified, player_id=", pid)
    db.save_player(pid, {"class": "warrior", "lvl": 5, "xp": 80, "hp": 120, "max_hp": 120})
    player = db.load_player(pid)
    print("Loaded:", player)
    db.close()