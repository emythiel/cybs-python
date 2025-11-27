"""
Module for handling the sqlite3 database.
"""

import logging
import sqlite3
logger = logging.getLogger(__name__)

def table_length(path: str, table: str) -> int:
    """
    Get current length of sqlite database table.
    Parameters:
        path (str): Path/filename of the sqlite database file.
        table (str): Name of the table to check.
    Returns:
        count (int): Number of rows in the table.
    """
    logger.debug(f'Checking length of {table} table ...')
    try:
        with sqlite3.connect(path) as conn:
            return conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]

    except sqlite3.OperationalError as err:
        raise ValueError(f'Bad SQL or missing table "{table}": {err}') from err
    except Exception as err:
        raise ValueError(f'Error getting {table} table length: {err}') from err


def init_tables(path: str) -> None:
    """
    Create sqlite database tables if they don't exist.
    Parameters:
        path (str): Path/filename of the sqlite database file.
    """
    logger.debug(f'Creating tables if they don\'t already exist ...')
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()

            query_incidents = '''CREATE TABLE IF NOT EXISTS incidents (
                                 incidentId TEXT PRIMARY KEY,
                                 incidentName TEXT,
                                 severity TEXT,
                                 status TEXT,
                                 createdTime TEXT
                                 )'''
            query_alerts    = '''CREATE TABLE IF NOT EXISTS alerts (
                                 alertId TEXT PRIMARY KEY,
                                 incidentId TEXT,
                                 machineId TEXT,
                                 detectionSource TEXT,
                                 firstActivity TEXT,
                                 FOREIGN KEY(incidentId) REFERENCES incidents(incidentId)
                                 )'''
            query_iocs      = '''CREATE TABLE IF NOT EXISTS iocs (
                                 incidentId TEXT,
                                 type TEXT,
                                 value TEXT,
                                 FOREIGN KEY(incidentId) REFERENCES incidents(incidentId),
                                 CONSTRAINT ioc UNIQUE(incidentId,type,value)
                                 )'''
            queries = [query_incidents, query_alerts, query_iocs]

            for query in queries:
                cur.execute(query)

            conn.commit()
            logger.debug(f'Create table queries committed to the database.')

    except sqlite3.OperationalError as err:
        raise ValueError(f'Error creating tables: {err}') from err
    except Exception as err:
        raise ValueError(f'Unexpected error creating tables: {err}') from err


def populate_tables(path: str, incidents: list[dict]) -> None:
    """
    Populate sqlite database tables with incident data.
    Parameters:
        path (str): Path/filename of the sqlite database file.
        incidents (list[dict]): List of dictionaries with incident data.
    """
    logger.debug(f'Populating tables with list of data ...')
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()

            query_incident = '''INSERT OR IGNORE INTO incidents (
                                incidentId,
                                incidentName,
                                severity,
                                status,
                                createdTime
                                ) VALUES (?,?,?,?,?)'''
            query_alert    = '''INSERT OR IGNORE INTO alerts (
                                alertId,
                                incidentId,
                                machineId,
                                detectionSource,
                                firstActivity
                                ) VALUES (?,?,?,?,?)'''
            query_ioc      = '''INSERT OR IGNORE INTO iocs (
                                incidentId,
                                type,
                                value
                                ) VALUES (?,?,?)'''

            for incident in incidents:
                incident_id = incident.get('incidentId')

                if incident_id is None:
                    logger.warning('Skipping incident with missing incidentId')
                    continue

                cur.execute(query_incident, (
                    incident_id,
                    incident.get('incidentName'),
                    incident.get('severity'),
                    incident.get('status'),
                    incident.get('createdTime')
                ))

                logger.debug(f'Inserted incident {incident_id}')

                alerts = incident.get('alerts', [])
                for alert in alerts:
                    alert_id = alert.get('alertId')

                    if alert_id is None:
                        logger.warning(f'Skipping alert from incident {incident_id} with missing alertId')
                        continue

                    cur.execute(query_alert, (
                        alert_id,
                        incident_id,
                        alert.get('machineId'),
                        alert.get('detectionSource'),
                        alert.get('firstActivity')
                    ))

                    #logger.debug(f'Inserted alert {alert_id} for incident {incident_id}')

                    entities = alert.get('entities', {})
                    for key, value in entities.items():
                        for e in value:
                            cur.execute(query_ioc, (incident_id, key, e))
            logger.debug(f'Inserted incident data from incident ID {incident_id}')

            conn.commit()
            logger.debug(f'{len(incidents)} incidents and their data committed to the database.')

    except sqlite3.OperationalError as err:
        raise ValueError(f'SQLite Operational Error populating tables: {err}') from err
    except sqlite3.DatabaseError as err:
        raise ValueError(f'SQLite Database Error populating tables: {err}') from err
    except Exception as err:
        raise ValueError(f'Unexpected error populating tables: {err}') from err
