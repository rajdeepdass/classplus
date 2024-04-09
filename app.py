from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random secret key for sessions

# SQLite database path
DATABASE = 'classplus.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    is_teacher INTEGER
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')
    conn.commit()
    conn.close()

create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_teacher = request.form.get('is_teacher', 0)  # 1 if checked, 0 if not
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        try:
            cur.execute('''INSERT INTO users (username, password, is_teacher) VALUES (?, ?, ?)''', (username, password, is_teacher))
            conn.commit()
            session['username'] = username
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            error = "Username already exists. Please choose another one."
            return render_template('signup.html', error=error)
        finally:
            cur.close()
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE username=? AND password=?''', (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('notes'))
        else:
            error = "Invalid username or password."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE username=?''', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('''SELECT id FROM users WHERE username=?''', (username,))
            user_id = cur.fetchone()[0]
            cur.execute('''INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)''', (user_id, title, content))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('notes'))
        else:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('''SELECT id FROM users WHERE username=?''', (username,))
            user_id = cur.fetchone()[0]
            cur.execute('''SELECT * FROM notes WHERE user_id=? ORDER BY created_at DESC''', (user_id,))
            user_notes = cur.fetchall()
            cur.close()
            conn.close()
            return render_template('notes.html', user_notes=user_notes)
    else:
        return redirect(url_for('login'))

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('''UPDATE notes SET title=?, content=? WHERE id=?''', (title, content, note_id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('notes'))
        else:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute('''SELECT * FROM notes WHERE id=?''', (note_id,))
            note = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('edit_note.html', note=note)
    else:
        return redirect(url_for('login'))

@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    if 'username' in session:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''DELETE FROM notes WHERE id=?''', (note_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('notes'))
    else:
        return redirect(url_for('login'))
    

def delete_user():
    # Handle the logic for deleting the user here
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
