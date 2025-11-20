"""
Main code
"""

# Import
import argparse
import logging
import sys
import time

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
    """
    Main incident database script. The script will go through the following process:

    1) Initialize database tables ('incidents', 'alerts', 'iocs') in case they don't exist.
    2) Get row count of 'incidents' table.
    3) Fetch authentication token from API.
    4) Fetch incident data from API.
    5) Get count of incident data from fetched data.
    6) Compare row count of table and count of fetched data
       - If counts are the same, exit (no new data), otherwise continue.
    7) Get 'value' key from fetched data and use it to populate database.
    8) If necessary: Use next_link from API to check if there's more data available.
       - Repeat previous step until all data fetched and committed.
       - Small sleep timer prevents hitting API rate limits.
    """
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
        logger.info(f'Current incidents in table: {incident_table_length} | Current incident total from API: {total_incidents}')
        if total_incidents <= incident_table_length:
            logger.info('--- NO NEW INCIDENTS FOUND, EXITING ---\n\n')
            sys.exit(0)

        # Initial population from previous incident data (no need to fetch same data twice)
        incident_list = incident_data.get('value', [])
        db.populate_tables(conf.DB_FILENAME, incident_list)
        incident_counter = len(incident_list)
        next_link = incident_data.get('@odata.nextLink')
        if next_link:
            incident_url = f'{conf.BASE_URL}{next_link}'
        else:
            incident_url = False


        while incident_url:
            incident_data = api.fetch_incidents(incident_url, token)

            incident_list = incident_data.get('value', [])
            db.populate_tables(conf.DB_FILENAME, incident_list)
            incident_counter += len(incident_list)

            next_link = incident_data.get('@odata.nextLink')
            if next_link:
                incident_url = f'{conf.BASE_URL}{next_link}'
            else:
                incident_url = False
                break

            # Timer to prevent hitting API rate limits.
            # 50/minute, 1500/hour. 60/3 = 20/minute, giving a generous buffer.
            logger.debug('Waiting 3 seconds before next API request to avoid API rate limits.')
            time.sleep(3)

    except ValueError as err:
        logger.error(f'Unexpected error: {err}', exc_info=True)
        sys.exit(1)


    logger.info(f'{incident_counter} new incidents added to the database.')


    logger.info(f'--- FINISHED INCIDENT DATA GATHERER ---\n\n')


if __name__ == '__main__':
    main()
