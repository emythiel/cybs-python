"""
Main configuration.
Save constants here for use with API Access and setting database filename and table names.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path.cwd() / '.env'
load_dotenv(dotenv_path=ENV_PATH)

# API Access
BASE_URL = os.getenv('BASE_URL')
STUDENT_EMAIL = os.getenv('STUDENT_EMAIL')


# Database
DB_FILENAME = 'incident_reports.sqlite'
DB_SCHEMA = {
    'incidents': [
        ('incidentId', 'TEXT PRIMARY KEY'),
        ('incidentName', 'TEXT'),
        ('severity', 'TEXT'),
        ('status', 'TEXT'),
        ('createdTime', 'TEXT'),
    ],
    'alerts': [
        ('alertId', 'TEXT'),
        ('incidentId', 'TEXT'),
        ('machineId', 'TEXT'),
        ('detectionSource', 'TEXT'),
        ('firstActivity', 'TEXT'),
    ],
    'iocs': [
        ('incidentId', 'TEXT'),
        ('type', 'TEXT'),
        ('value', 'TEXT'),
    ],
}


# Logging
LOG_FILENAME = 'incident_reports.log'
