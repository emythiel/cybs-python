# Continued from first_database.py
# Make a program that can:
# 1. Read the data from a table and print it out
# 2. Inform you if the table is empty
# 3. Not crash if the table doesn't exist
# 4. Use a DELETE statement to remove a query

import sqlite3
from pathlib import Path

DB_PATH = Path.cwd() / 'first_db.sqlite'

def db_read_all():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            data = cur.execute('SELECT * FROM students ORDER BY student_id').fetchall()

            if not len(data):
                print('Table is empty!')
            else:
                for student in data:
                    print(f'Student: {student}')
    except sqlite3.OperationalError as e:
        if 'no such table' in str(e).lower():
            print('[ERROR]: the table does not exist!')
        else:
            print(f'[ERROR] An operational error occured: {e}')

def db_delete_student(student):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM students WHERE first_name= ?', (student,))
            conn.commit()
            print(f'Student "{student}" has been deleted (if they existed)')
    except sqlite3.OperationalError as e:
        if 'no such table' in str(e).lower():
            print('[ERROR]: the table does not exist!')
        else:
            print(f'[ERROR] An operational error occured: {e}')

db_read_all()
db_delete_student('Bilbo')
