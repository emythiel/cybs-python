import json
from pathlib import Path
import requests
import sqlite3

# Init stuff
BASE_URL = 'http://209.38.211.219'
STUDENT_EMAIL = 'emko1000@stud.ek.dk'
DB_PATH = Path.cwd() / 'database.sqlite3'

# Step 1: Request a token
def fetch_token(url, email):
    headers = {'Content-Type': 'application/json'}
    data = {'email': email}

    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()

    token = response.json().get('token')

    if not token:
        raise ValueError('Token missing')

    return token

# Step 2: Fetch data
def fetch_incidents(url, token):
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    incident_data = response.json()

    if not incident_data:
        raise ValueError('Incident data missing?')

    return incident_data

# Step 3: Create database
def create_database(path):
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        query = f'''CREATE TABLE IF NOT EXISTS incident_reports (
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

# Step 4: Populate database
def populate_db(path, incidents):
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()

        query = f'''INSERT INTO incident_reports (
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


if __name__ == '__main__':
    token_url = f'{BASE_URL}/api/auth/token'
    token = fetch_token(token_url, STUDENT_EMAIL)

    incident_url = f'{BASE_URL}/api/incidents'
    incident_data = fetch_incidents(incident_url, token)

    create_database(DB_PATH)

    populate_db(DB_PATH, incident_data.get('value'))
