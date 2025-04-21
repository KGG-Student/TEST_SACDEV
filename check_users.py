import sqlite3

conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

# Check if the users table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
table_exists = cursor.fetchone()

if table_exists:
    print("✅ 'users' table found. Showing contents:")
    for row in cursor.execute('SELECT * FROM users'):
        print(row)
else:
    print("❌ 'users' table not found!")

conn.close()
