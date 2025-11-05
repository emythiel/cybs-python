# Mandatory 02 - Programming
# Emily, Natasha, Sigurd, Thomas

from pathlib import Path
import sqlite3
import sys

import requests

# Declare constants
BASE_URL = 'http://209.38.211.219'
STUDENT_EMAIL = 'emko1000@stud.ek.dk'

DB_PATH = Path.cwd() / 'database.sqlite3'
DB_TABLE = 'incident_reports_nice'


# Main Code

def fetch_token(url: str, email: str) -> str:
    """
    Fetches a token from provided url, using the provided email to authenticate.
    Args:
        url (str): API URL to fetch token.
        email (str): Student email to validate with.
    Returns:
        str: Token retrieved from the API.
    Raises:
        ValueError: If there was a problem getting a response
    Example:
        >>> fetch_token('http://example.com/api', 'student@mail.dk')
        'student-5aai5QjHit6w-YKrKI4luA'
    """

    headers = {'Content-Type': 'application/json'}
    data = {'email': email}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        token = response.json().get('token')

        if not token:
            raise ValueError('Token missing')

        return token
    except Exception as err:
        raise ValueError(f'Unexpected error fetching API token: {err}') from err


def fetch_incidents(url: str, token: str) -> dict:
    """
    Fetches incident reports from provided url, using provided token to authenticate.
    Args:
        url (str): API URL to fetch data from.
        token (str): Token used to authenticate with.
    Returns:
        dict: Parsed JSON response containing incident data.
    Raises:
        ValueError: If there was a problem getting a response
    Example:
        >>> fetch_incidents('http://example.com/api', 'student-5aai5QjHit6w-YKrKI4luA')
        {incident_data_as_dict}
    """

    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        incident_data = response.json()

        if not incident_data:
            raise ValueError('Incident data missing?')

        return incident_data
    except Exception as err:
        raise ValueError(f'Unexpected error fetching data from API: {err}') from err


def db_exists(path: str, table: str) -> bool:
    """
    Checks if the provided table exists for the provided database filepath.
    Args:
        path (str): Filepath to the database file.
        table (str): Name of the database table.
    Returns:
        bool: True if table exists, False if not.
    Raises:
        ValueError: If there was a problem checking for the table.
    Example:
        >>> db_exists('./incidents/database.sqlite', 'table_name')
        True
        >>> db_exists('./incidents/database.sqlite', 'table_not_exist')
        False
    """
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table,))
            table_data = cur.fetchone()

            if table_data:
                return True
            else:
                print(f'[INFO] Table "{table}" doesn\'t exist. Proceeding as normal...')
                return False
    except Exception as err:
        raise ValueError(f'Unexpected error checking if table exists: {err}') from err


def db_drop_table(path: str, table: str) -> None:
    """
    Drops the provided table from the provided database filepath.
    Args:
        path (str): Filepath to the database file.
        table (str): Name of the database table.
    Raises:
        ValueError: If there was a problem dropping the table.
    Example:
        >>> db_drop_table('./incidents/database.sqlite', 'table_name')
    """
    try:
        choice = input(f'Table "{table}" already exists. Overwrite? (y/n): ').strip().lower()
        if choice == 'y':
            print(f'[INFO] Overwriting existing table, "{table}", and proceeding...')
            with sqlite3.connect(path) as conn:
                cur = conn.cursor()
                cur.execute(f'DROP TABLE {table}')
                conn.commit()
        else:
            print('[INFO] Operation canceled by user. Exiting with no changes.')
            sys.exit(0)
    except Exception as err:
        raise ValueError(f'Unexpected error dropping table: {err}') from err

def create_database(path: str, table: str) -> None:
    """
    Creates/uses a database file at the provided path, and makes a table.
    Args:
        path (str): Filepath to the database file.
        table (str): Name of the database table.
    Raises:
        ValueError: If there's an error creating / connecting to the database or creating the table.
    Example:
        >>> create_database('./incidents/database.sqlite', 'table_name')
    """

    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            query = f'''CREATE TABLE IF NOT EXISTS {table} (
                        uid INTEGER PRIMARY KEY AUTOINCREMENT,
                        incidentId TEXT,
                        createdTime TEXT,
                        alertId TEXT,
                        category TEXT,
                        machineId TEXT,
                        firstActivity TEXT,
                        detectionSource TEXT
                        )'''
            cur.execute(query)
            conn.commit()
    except Exception as err:
        raise ValueError(f'Unexpected error creating database table: {err}') from err


def populate_db(path: str, table: str, incidents: list) -> None:
    """
    Populate database at the provided path, using the provided incidents list for the data.
    Args:
        path (str): Filepath to the database file.
        table (str): Name of the database table.
        incidents (list): List of incidents, with each incident being a dict.
    Raises:
        ValueError: If there's an error connecting to the database, or populating the table.
    Example:
        >>> populate_db('./incidents/database.sqlite', 'table_name', [incident1_dict, incident2_dict])
    """

    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()

            query = f'''INSERT INTO {table} (
                        incidentId,
                        createdTime,
                        alertId,
                        category,
                        machineId,
                        firstActivity,
                        detectionSource
                        ) VALUES (?,?,?,?,?,?,?)'''

        for incident in incidents:
            alerts = incident.get('alerts', [])
            if not alerts:
                continue

            incident_id = incident.get('incidentId')
            created_time = incident.get('createdTime')

            for alert in alerts:
                alert_id = alert.get('alertId')
                category = alert.get('category')
                machine_id = alert.get('machineId')
                first_activity = alert.get('firstActivity')
                detection_source = alert.get('detectionSource')

                cur.execute(query, (
                    incident_id,
                    created_time,
                    alert_id,
                    category,
                    machine_id,
                    first_activity,
                    detection_source
                ))

        conn.commit()
    except Exception as err:
        raise ValueError(f'Unexpected error populating database table: {err}') from err


if __name__ == '__main__':
    # Check if database table already exists - if yes, ask to overwrite or cancel
    try:
        table_exists = db_exists(DB_PATH, DB_TABLE)
        if table_exists:
            db_drop_table(DB_PATH, DB_TABLE)
    except ValueError as err:
        print(f'[ERROR] {err}')
        sys.exit(1)

    # Fetch token and then incident data from API
    token_url = f'{BASE_URL}/api/auth/token'
    incident_url = f'{BASE_URL}/api/incidents'
    incident_data_final = []
    try:
        token = fetch_token(token_url, STUDENT_EMAIL)

        while incident_url:
            print(f'[INFO] Fetching data from url: {incident_url}')
            incident_data = fetch_incidents(incident_url, token)

            next_link = incident_data.get('@odata.nextLink')
            if next_link:
                incident_url = f'{BASE_URL}{next_link}'
            else:
                incident_url = None

            incident_data_final.extend(incident_data.get('value', []))

        if not incident_data_final:
            print('[ERROR] No incident data was found?')
            sys.exit(1)

        print(f'[INFO] Retrieved {len(incident_data_final)} incidents in total.')
    except ValueError as err:
        print(f'[ERROR] {err}')
        sys.exit(1)

    # Create database / table and populate with data
    try:
        create_database(DB_PATH, DB_TABLE)
        populate_db(DB_PATH, DB_TABLE, incident_data_final)
    except ValueError as err:
        print(f'[ERROR] {err}')
        sys.exit(1)
