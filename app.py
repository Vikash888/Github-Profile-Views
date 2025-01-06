from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Path to the SQLite database file
DATABASE = 'views.db'

# Function to initialize the database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS views (
                id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL
            )
        ''')
        c.execute('''
            INSERT INTO views (id, count) VALUES (1, 0)
            ON CONFLICT(id) DO NOTHING
        ''')
        conn.commit()
        conn.close()

# Function to get the current view count from the database
def get_view_count():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT count FROM views WHERE id = 1')
    count = c.fetchone()[0]
    conn.close()
    return count

# Function to increment the view count in the database
def increment_view_count():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE views SET count = count + 1 WHERE id = 1')
    conn.commit()
    conn.close()

@app.route('/')
def profile():
    increment_view_count()
    views = get_view_count()
    return render_template_string('''
        <h1>Profile Page</h1>
        <p>Number of views: {{ views }}</p>
    ''', views=views)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
