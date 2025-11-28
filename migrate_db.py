#!/usr/bin/env python3
"""
Database migration script to update existing SHA256 password hashes to bcrypt
"""
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import bcrypt
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "server" / "isekai_online.db"

def migrate_to_bcrypt():
    """Convert existing SHA256 hashes to bcrypt"""
    if not DB_FILE.exists():
        print("No database found. Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check if any accounts exist
    cursor.execute("SELECT username, password FROM accounts")
    accounts = cursor.fetchall()
    
    if not accounts:
        print("No accounts found. Nothing to migrate.")
        return
    
    print(f"Found {len(accounts)} accounts. Checking for migration needs...")
    
    modified = False
    for username, password_hash in accounts:
        # If the password hash looks like a bcrypt hash (length 60 and starts with $2)
        if len(password_hash) == 60 and password_hash.startswith("$2"):
            print(f"Account {username} already uses bcrypt. Skipping.")
            continue
        
        # Otherwise, assume it's the old SHA256 hash and update it
        print(f"Migrating account {username} to bcrypt...")
        
        # Generate a new bcrypt hash
        password_bytes = "1".encode('utf-8') if username == "1" else "password".encode('utf-8')
        salt = bcrypt.gensalt()
        new_hash = bcrypt.hashpw(password_bytes, salt)
        
        # Update the database
        cursor.execute("UPDATE accounts SET password = ? WHERE username = ?", 
                     (new_hash.decode('utf-8'), username))
        modified = True
        print(f"Account {username} migrated successfully.")
    
    if modified:
        conn.commit()
        print("Database migration completed!")
    else:
        print("No accounts needed migration.")
    
    conn.close()

if __name__ == "__main__":
    migrate_to_bcrypt()