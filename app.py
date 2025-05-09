from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_login import logout_user
import sqlite3
import traceback

app = Flask(__name__)
app.secret_key = 'secret123'  # Required for session and flash

DATABASE = 'database/users.db'

# --- DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('database/db_script.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- LOGIN ROUTE ---
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                          (username, password)).fetchone()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'sacdev':
                return redirect(url_for('sacdev_dashboard'))
            elif user['role'] == 'rrc':
                return redirect(url_for('rrc_dashboard'))
            else:
                return 'Unauthorized', 403
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


# --- DASHBOARD ROUTE ---
@app.route('/sacdev_dashboard', methods=['GET', 'POST'])
def sacdev_dashboard():
    if session.get('role') != 'sacdev':
        return redirect('/login')

    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()

    # Add organization
    if request.method == 'POST':
        if 'add_org' in request.form:
            name = request.form['name']
            description = request.form['description']
            mission = request.form['mission']
            vision = request.form['vision']
            status = request.form['status']
            c.execute('INSERT INTO organizations (name, description, mission, vision, status) VALUES (?, ?, ?, ?, ?)',
                      (name, description, mission, vision, status))
            conn.commit()
        elif 'delete_org' in request.form:
            org_id = request.form['org_id']
            c.execute('DELETE FROM organizations WHERE id = ?', (org_id,))
            conn.commit()

    c.execute('SELECT * FROM organizations')
    orgs = c.fetchall()
    conn.close()

    return render_template('sacdev_dashboard.html', user=session['username'], orgs=orgs)


@app.route('/rrc_dashboard')
def rrc_dashboard():
    if 'username' not in session or session.get('role') != 'rrc':
        return redirect(url_for('login'))
    
    # You can customize what data RRC should see here
    return render_template('rrc_dashboard.html', user=session['username'])

# --- LOGOUT ---
@app.route('/logout')
def logout():
    # logout_user()  
    return redirect(url_for('login'))  
# --- ORGANIZATIONS ---

@app.route('/organization/<int:org_id>', methods=['GET', 'POST'])
def view_organization(org_id):
    db = get_db()

    # Handle new member submission
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        db.execute(
    'INSERT INTO members (org_id, full_name, position) VALUES (?, ?, ?)',
    (org_id, request.form['name'], request.form['position'])
)

        db.commit()
        return redirect(url_for('view_organization', org_id=org_id))

    org = db.execute('SELECT * FROM organizations WHERE id = ?', (org_id,)).fetchone()
    members = db.execute('SELECT * FROM members WHERE org_id = ?', (org_id,)).fetchall()
    documents = db.execute('SELECT * FROM documents WHERE org_id = ?', (org_id,)).fetchall()
    return render_template('organization_view.html', org=org, members=members, documents=documents)


# ---STUDENTS ORGS--- 
@app.route('/students_orgs')
def students_orgs():
    try:
        conn = sqlite3.connect('database/db_script.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute('''
            SELECT o.name AS org_name, m.full_name, m.position, m.qpi
            FROM members m
            JOIN organizations o ON m.org_id = o.id
        ''')

        students = c.fetchall()
        conn.close()

        return render_template('students_orgs.html', students=students)

    except Exception as e:
        import traceback
        return f"<pre>{traceback.format_exc()}</pre>"





if __name__ == '__main__':
    app.run(debug=True)
