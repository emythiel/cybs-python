# - Create a local database using sqlite3 module.
# - Create a table for "students" with appropriate data structure.
# - Insert 3 entries into your new table.
#
# User error handling where appropriate and remember to close connection.
# Bonus: Make error handling for invalid entries. Eg: Trying to insert the same value into a unique field.

import sqlite3
from pathlib import Path

DB_PATH = Path.cwd() / 'first_db.sqlite'

def create_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        db_query = '''CREATE TABLE IF NOT EXISTS students (
                      student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT NOT NULL,
                      last_name TEXT NOT NULL
                      )'''
        cur.execute(db_query)
        conn.commit()

def populate_db():
    students = [('John', 'Doe'), ('Jane', 'Doe'), ('Bilbo', 'Baggins')]

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        db_query = 'INSERT INTO students (first_name, last_name) VALUES (?, ?)'

        for first_name, last_name in students:
            try:
                cur.execute(db_query, (first_name, last_name))
            except sqlite3.IntegrityError as e:
                print(f'Error inserting ({first_name}, {last_name}): {e}')

        conn.commit()

create_db()
populate_db()
