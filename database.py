import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('db/classplus.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT
    )
''')

# Create Notes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notes (
        note_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        content TEXT,
        type TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
''')

# Create CalendarEvents table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CalendarEvents (
        event_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()
