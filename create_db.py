import sqlite3
import os

# Make sure the directory exists
if not os.path.exists('database'):
    os.makedirs('database')

# Connect to SQLite database
conn = sqlite3.connect('database/users.db')
c = conn.cursor()

# Create users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# Create organizations table
c.execute('''
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        mission TEXT,
        vision TEXT,
        status TEXT DEFAULT 'Pending'
    )
''')

# Create members table
c.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        org_id INTEGER,
        full_name TEXT,
        position TEXT,
        email TEXT,
        contact_no TEXT,
        sex TEXT,
        qpi REAL,
        course TEXT,
        year_level TEXT,
        college TEXT,
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )
''')

# Create documents table
c.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        org_id INTEGER,
        title TEXT,
        file_path TEXT,
        tag TEXT,
        academic_year TEXT,
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )
''')

# Optional: Insert default admin/SACDEV user
c.execute('''
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES (?, ?, ?)
''', ('sacdev_admin', 'admin123', 'sacdev'))

# Optional: Insert default RRC user
c.execute('''
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES (?, ?, ?)
''', ('rrc_user', 'rrc123', 'rrc'))

conn.commit()
conn.close()

print("✅ Database and tables created successfully.")
