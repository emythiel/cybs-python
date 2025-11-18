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

    token_url = f'{conf.BASE_URL}/api/auth/token'
    incident_url = f'{conf.BASE_URL}/api/incidents'


    try:
        # Ensure database tables are initialized
        db.init_tables(conf.DB_FILENAME)
        incident_table_length = db.table_length(conf.DB_FILENAME, 'incidents')


        # Fetch token and data from API
        token = api.fetch_token(token_url, conf.STUDENT_EMAIL)


        # Fetch initial incident data and compare count with database table length
        incident_data = api.fetch_incidents(incident_url, token, incident_table_length, 100)
        total_incidents = incident_data.get('@odata.count')
        if total_incidents <= incident_table_length:
            logger.info(f'Current incidents in table: {incident_table_length} | Current incident total from API: {total_incidents}')
            logger.info('--- NO NEW INCIDENTS FOUND, EXITING ---')
            sys.exit(0)

        # Initial population from previous incident data (no need to fetch same data twice)
        incident_list = incident_data.get('value', [])
        db.populate_tables(conf.DB_FILENAME, incident_list)

        while incident_url:
            incident_data = api.fetch_incidents(incident_url, token, incident_table_length, 100)

            incident_list = incident_data.get('value', [])
            db.populate_tables(conf.DB_FILENAME, incident_list)

            next_link = incident_data.get('@odata.nextLink')
            if next_link:
                incident_url = f'{conf.BASE_URL}{next_link}'
            else:
                incident_url = False
                break

            logger.info('Waiting 3 seconds before next API request to avoid API limits.')
            time.sleep(3)  # Timer to prevent hitting API limits.

        #logger.info(f'Fetched {len(incident_data_final)} new incidents in total from API.')
    except ValueError as err:
        logger.error('Unexpected error: ', exc_info=True)
        sys.exit(1)


    logger.info(f'--- FINISHED INCIDENT DATA GATHERER ---\n\n')


if __name__ == '__main__':
    main()
