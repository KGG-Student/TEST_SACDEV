import sqlite3
import os

# Ensure the database folder exists
os.makedirs('database', exist_ok=True)

# Connect to the database
db_path = 'database/db_script.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create organizations table
c.execute('''
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        mission TEXT,
        vision TEXT,
        status TEXT
    )
''')

# Create members table
c.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        org_id INTEGER,
        full_name TEXT NOT NULL,
        position TEXT,
        email TEXT,
        contact_no TEXT,
        sex TEXT,
        qpi REAL,
        course TEXT,
        year_level TEXT,
        college TEXT,
        FOREIGN KEY (org_id) REFERENCES organizations(id) ON DELETE CASCADE
    )
''')

# Dummy data
organizations = [
    {
        'name': 'Tech Innovators',
        'description': 'A student org focused on technology and innovation.',
        'mission': 'To innovate and inspire through technology.',
        'vision': 'A future empowered by student-led tech solutions.',
        'status': 'Active',
        'members': [
            ('Alice Cruz', 'President', 'alice@example.com', '09170000001', 'Female', 3.6, 'Computer Science', '3rd', 'College of Engineering'),
            ('Ben Torres', 'Vice President', 'ben@example.com', '09170000002', 'Male', 3.4, 'Information Systems', '2nd', 'College of Engineering'),
            ('Cara Lim', 'Secretary', 'cara@example.com', '09170000003', 'Female', 3.8, 'Software Engineering', '4th', 'College of Engineering'),
            ('Dino Reyes', 'Treasurer', 'dino@example.com', '09170000004', 'Male', 3.2, 'Computer Engineering', '1st', 'College of Engineering'),
            ('Elaine Go', 'Auditor', 'elaine@example.com', '09170000005', 'Female', 3.7, 'Information Technology', '3rd', 'College of Engineering')
        ]
    },
    {
        'name': 'Biz Leaders Guild',
        'description': 'An organization for aspiring business leaders.',
        'mission': 'To develop leadership and business acumen.',
        'vision': 'A generation of visionary entrepreneurs.',
        'status': 'Pending',
        'members': [
            ('Francis Uy', 'President', 'francis@example.com', '09170000006', 'Male', 3.9, 'Business Administration', '4th', 'College of Business'),
            ('Grace Tan', 'VP External', 'grace@example.com', '09170000007', 'Female', 3.5, 'Accounting', '2nd', 'College of Business'),
            ('Harold Ong', 'VP Internal', 'harold@example.com', '09170000008', 'Male', 3.6, 'Finance', '3rd', 'College of Business'),
            ('Isabelle Chua', 'Secretary', 'isabelle@example.com', '09170000009', 'Female', 3.3, 'Marketing', '1st', 'College of Business'),
            ('Jake Yu', 'PRO', 'jake@example.com', '09170000010', 'Male', 3.4, 'Entrepreneurship', '2nd', 'College of Business')
        ]
    },
    {
        'name': 'Arts & Culture Circle',
        'description': 'Celebrating arts, heritage, and creative expression.',
        'mission': 'To enrich the university through the arts.',
        'vision': 'A vibrant cultural community of students.',
        'status': 'Active',
        'members': [
            ('Kyla Santos', 'President', 'kyla@example.com', '09170000011', 'Female', 3.8, 'Fine Arts', '4th', 'College of Arts and Sciences'),
            ('Leo Bautista', 'VP Cultural Affairs', 'leo@example.com', '09170000012', 'Male', 3.2, 'Performing Arts', '3rd', 'College of Arts and Sciences'),
            ('Mara Diaz', 'Secretary', 'mara@example.com', '09170000013', 'Female', 3.6, 'Literature', '2nd', 'College of Arts and Sciences'),
            ('Nico Ramos', 'Treasurer', 'nico@example.com', '09170000014', 'Male', 3.3, 'Media Arts', '1st', 'College of Arts and Sciences'),
            ('Olive Velasco', 'Curator', 'olive@example.com', '09170000015', 'Female', 3.9, 'Art History', '3rd', 'College of Arts and Sciences')
        ]
    }
]

# Insert organizations and their members
for org in organizations:
    c.execute('''
        INSERT INTO organizations (name, description, mission, vision, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (org['name'], org['description'], org['mission'], org['vision'], org['status']))
    
    org_id = c.lastrowid  # Get the ID of the organization just inserted
    
    for member in org['members']:
        c.execute('''
            INSERT INTO members (
                org_id, full_name, position, email, contact_no,
                sex, qpi, course, year_level, college
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (org_id, *member))

# Finalize changes and close connection
conn.commit()
conn.close()

print("✅ Successfully created and populated the database with 3 organizations and 15 members.")
