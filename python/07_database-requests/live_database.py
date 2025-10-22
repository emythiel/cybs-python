# Make a program that connects to a live database.
# It should get all the results from the table "students" and print them.

from dotenv import load_dotenv
import os
from pathlib import Path
import mysql.connector

ENV_PATH = Path.cwd() / '.env'
load_dotenv(dotenv_path=ENV_PATH)

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')

def read_from_db():
    try:
        with mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        ) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM students')
            data = cur.fetchall()
            if not len(data):
                print('Table is empty!')
            else:
                print(data)
    except mysql.connector.errors.ProgrammingError as e:
        if e.errno == 1142:
            print('[ERROR]: The table does not exist!')
        else:
            print(f'[ERROR]: {getattr(e, 'msg', None)}')
    except mysql.connector.Error as e:
        print(f'[ERROR]: MySQL error: {e}')

read_from_db()
