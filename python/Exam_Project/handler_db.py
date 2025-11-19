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

            query_incidents = f'''CREATE TABLE IF NOT EXISTS incidents (
                                  incidentId TEXT PRIMARY KEY,
                                  incidentName TEXT,
                                  severity TEXT,
                                  status TEXT,
                                  createdTime TEXT
                                  )'''
            query_alerts    = f'''CREATE TABLE IF NOT EXISTS alerts (
                                  alertId TEXT,
                                  incidentId TEXT,
                                  machineId TEXT,
                                  detectionSource TEXT,
                                  firstActivity TEXT
                                  )'''
            query_iocs      = f'''CREATE TABLE IF NOT EXISTS iocs (
                                  incidentId TEXT,
                                  type TEXT,
                                  value TEXT
                                  )'''
            queries = [query_incidents, query_alerts, query_iocs]

            for query in queries:
                cur.execute(query)

            conn.commit()
            logger.debug(f'Create table queries committed to the database.')
    except Exception as err:
        raise ValueError(f'Error creating tables: {err}') from err


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

            query_incident = f'''INSERT OR IGNORE INTO incidents (
                                 incidentId,
                                 incidentName,
                                 severity,
                                 status,
                                 createdTime
                                 ) VALUES (?,?,?,?,?)'''
            query_alert    = f'''INSERT OR IGNORE INTO alerts (
                                 alertId,
                                 incidentId,
                                 machineId,
                                 detectionSource,
                                 firstActivity
                                 ) VALUES (?,?,?,?,?)'''
            query_ioc      = f'''INSERT OR IGNORE INTO iocs (
                                 incidentId,
                                 type,
                                 value
                                 ) VALUES (?,?,?)'''

            for inc in incidents:
                inc_id = inc.get('incidentId')
                inc_name = inc.get('incidentName')
                inc_severity = inc.get('severity')
                inc_status = inc.get('status')
                inc_created_time = inc.get('createdTime')

                cur.execute(query_incident, (inc_id, inc_name, inc_severity,
                                             inc_status, inc_created_time))

                alerts = inc.get('alerts', [])
                for alert in alerts:
                    alert_id = alert.get('alertId')
                    alert_machine_id = alert.get('machineId')
                    alert_source = alert.get('detectionSource')
                    alert_first_activity = alert.get('firstActivity')

                    cur.execute(query_alert, (alert_id, inc_id, alert_machine_id,
                                              alert_source, alert_first_activity))

                    entities = alert.get('entities', {})
                    for key, value in entities.items():
                        for e in value:
                            cur.execute(query_ioc, (inc_id, key, e))
            conn.commit()
            logger.debug(f'{len(incidents)} incidents and their data commited to the database.')
    except Exception as err:
        raise ValueError(f'Error populating tables: {err}') from err
