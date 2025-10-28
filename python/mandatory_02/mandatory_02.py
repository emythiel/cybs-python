# Mandatory 02 - Programming
# Emily, Natasha, Sigurd, Thomas

# Load environment variables for api url and student email
import sys, os, sqlite3
from pathlib import Path

import requests
from dotenv import load_dotenv

ENV_PATH = Path.cwd() / '.env'
load_dotenv(dotenv_path=ENV_PATH)

BASE_URL = os.getenv('BASE_URL')
STUDENT_EMAIL = os.getenv('STUDENT_EMAIL')

DB_PATH = Path.cwd() / 'database.sqlite'
DB_TABLE = 'incident_reports'


# Main code


def fetch_token(url: str, email: str) -> str:
    """
    Request authentication token from API.

    Args:
        url (str): API URL.
        email (str): Student email needed to get a token.

    Returns:
        str: The authentication token retrieved from the API.
    """

    headers = {'Content-Type': 'application/json'}
    data = {'email': email}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()  # Raise HTTPError for 4xx/5xx responses

        token = response.json().get('token')

        if not token:
            raise ValueError('Token missing from response?')

        return token
    except Exception as e:
        resp_text = getattr(response, "text", "No response text available.")  # If crash before a response text was available
        raise ValueError(f'Unexpected error fetching API token: {e}\nResponse text: {resp_text}') from e


def fetch_incidents(url: str, token: str) -> dict:
    """
    Fetch incident data from the API using the provided authentication token.

    Args:
        url(str): API URL.
        token (str): Bearer authentication token.

    Returns:
        dict: Parsed JSON resposne containing incident data.
    """

    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()  # Raise HTTPError for 4xx/5xx responses

        incidents_data = response.json()

        if not incidents_data:
            raise ValueError('Incident data could not be retrieved?')

        return incidents_data
    except Exception as e:
        resp_text = getattr(response, "text", "No response text available.")  # If crash before a response text was available
        raise ValueError(f'Unexpected error fetching incident data: {e}\nResponse text: {resp_text}') from e


def db_table_exists(db_path: str, table: str) -> None:
    """
    Check if a table already exists in the database.
    If it does, prompt the user to overwrite or cancel.

    Args:
        db_path (str): Path to the database file.
        table (str): Name of the database table.
    """

    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table,))
            table_data = cur.fetchone()

            if table_data:
                choice = input(f'Table "{table}" already exists. Overwrite? (y/n): ').strip().lower()
                if choice == 'y':
                    cur.execute(f'DROP TABLE {table}')
                    conn.commit()
                    print(f'[INFO] Overwriting existing table, "{table}", and proceeding...')
                else:
                    print('[INFO] Operation canceled by user. Exiting with no changes.')
                    sys.exit(0)
            else:
                print(f'[INFO] Table "{table}" doesn\'t exist. Proceeding as normal...')
    except Exception as e:
        raise ValueError(f'Unexpected error checking if table exists/dropping table: {e}') from e


def create_db_table(db_path: str, table: str) -> None:
    """
    Create a new database table if it does not already exist.

    Args:
        db_path (str): Path to the database file.
        table (str): Name of the database table.
    """

    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            query = f'''CREATE TABLE IF NOT EXISTS {table} (
                        uid INTEGER PRIMARY KEY AUTOINCREMENT,
                        incidentId TEXT,
                        createdTime TEXT,
                        alertId TEXT,
                        category TEXT,
                        machineId TEXT,
                        firstActivity TEXT,
                        severity TEXT,
                        detectionSource TEXT
                        )'''
            cur.execute(query)
            conn.commit()
    except Exception as e:
        raise ValueError(f'Unexpected database error: {e}') from e


def populate_db_table(db_path: str, table: str, incidents: list) -> None:
    """
    Populate the database table with the provided data.

    Args:
        db_path (str): Path to the database file.
        table (str): Name of the database table.
        incidents (list): List of incidents (each containing several 'alerts').
    """

    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()

            query = f'''INSERT INTO {table} (
                        incidentId,
                        createdTime,
                        alertId,
                        category,
                        machineId,
                        firstActivity,
                        severity,
                        detectionSource
                        ) VALUES (?,?,?,?,?,?,?,?)
                        '''

            for incident in incidents:
                alerts = incident.get('alerts', [])
                if not alerts:
                    continue  # Skip incidents with no alerts

                incident_id = incident.get('incidentId')
                created_time = incident.get('createdTime')

                for alert in alerts:
                    # Extract fields
                    alert_id = alert.get("alertId")
                    category = alert.get("category")
                    machine_id = alert.get("machineId")
                    first_activity = alert.get("firstActivity")
                    severity = alert.get("severity")
                    detection_source = alert.get("detectionSource")

                    # Insert into table
                    cur.execute(query, (
                        incident_id,
                        created_time,
                        alert_id,
                        category,
                        machine_id,
                        first_activity,
                        severity,
                        detection_source
                    ))

            conn.commit()
    except Exception as e:
        raise ValueError(f'Unexpected error populating database table: {e}') from e


if __name__ == '__main__':
    # Check if database table already exists - if yes, ask to overwrite otherwise exit
    try:
        db_table_exists(DB_PATH, DB_TABLE)
    except ValueError as e:
        print(f'[ERROR] {e}')
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

            page_data = incident_data.get('value', [])
            if not page_data:
                print('[ALERT] No incidents found on this page')
                continue

            incident_data_final.extend(page_data)

        print(f'[INFO] Retrieved {len(incident_data_final)} incidents in total.')
    except ValueError as e:
        print(f'[ERROR] {e}')
        sys.exit(1)


    if not incident_data_final:
        print('[ERROR] Could not find anything for the "value" key?')
        sys.exit(1)


    # Create database / table and populate with data
    try:
        create_db_table(DB_PATH, DB_TABLE)
        populate_db_table(DB_PATH, DB_TABLE, incident_data_final)
    except ValueError as e:
        print(f'[ERROR] {e}')
        sys.exit(1)
