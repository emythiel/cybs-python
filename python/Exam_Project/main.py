"""
Main code
"""

# Import
import argparse
import datetime
import logging
import sys
import sqlite3
import time
from pathlib import Path

import requests

import config as conf
import handler_db as db
import handler_api as api

# Initialize argument parser
parser = argparse.ArgumentParser(
    description='Fetches incident data from a url, and inserts the data into a sqlite3 database'
)
parser.add_argument('-d', '--debug', action='store_true', help='run with debug mode enabled for extended logging')
args = parser.parse_args()

# Initialize logger
logger = logging.getLogger(__name__)

if args.debug:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(
    filename=conf.LOG_FILENAME,
    level=level,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y%m%d-%H:%M:%S'
)

def main():
    logger.info(f'--- STARTED INCIDENT DATA GATHERER ---')

    # Ensure database tables are initialized
    try:
        query_list = [
            db.make_create_table_query(table_name, columns)
            for table_name, columns in conf.DB_SCHEMA.items()
        ]
        db.init_tables(conf.DB_FILENAME, query_list)
        incident_table_length = db.table_length(conf.DB_FILENAME, next(iter(conf.DB_SCHEMA)))
    except ValueError as err:
        logger.error('Unexpected error while handling the sqlite database.', exc_info=True)
        sys.exit(1)

    # Fetch token and data from API
    token_url = f'{conf.BASE_URL}/api/auth/token'
    incident_summary_url = f'{conf.BASE_URL}/api/incidents/summary'
    incident_url = f'{conf.BASE_URL}/api/incidents'
    incident_data_final = list()

    try:
        token = api.fetch_token(token_url, conf.STUDENT_EMAIL)

        summary_data = api.fetch_incidents(incident_summary_url, token)
        total_incidents = summary_data.get('total_incidents')
        if total_incidents <= incident_table_length:
            logger.info(f'Current incidents in table: {incident_table_length} | Current incident total from API: {total_incidents}')
            logger.info('--- NO NEW INCIDENTS FOUND, EXITING ---')
            sys.exit(0)

        while incident_url:
            incident_data = api.fetch_incidents(incident_url, token, incident_table_length, 100)

            incident_data_final.extend(incident_data.get('value', []))

            next_link = incident_data.get('@odata.nextLink')
            if next_link:
                incident_url = f'{conf.BASE_URL}{next_link}'
            else:
                incident_url = False
                break

            logger.info('Waiting 3 seconds before next API request to avoid API limits.')
            time.sleep(3)  # Timer to prevent hitting API limits.

        if not incident_data_final:
            logger.critical('No incident data was saved, despite the fact we should be getting some?')
            sys.exit(1)

        logger.info(f'Fetched {len(incident_data_final)} new incidents in total from API.')
    except ValueError as err:
        logger.error('Unexpected error while fetching data from API.', exc_info=True)
        sys.exit(1)


    logger.info(f'--- FINISHED INCIDENT DATA GATHERER ---\n\n')


if __name__ == '__main__':
    main()
