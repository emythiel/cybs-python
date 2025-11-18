"""
Module for handling the sqlite3 database.
"""

import logging
import sqlite3
logger = logging.getLogger(__name__)


def make_create_table_query(table_name: str, columns: list[tuple[str, str]]) -> str:
    """

    """
    try:
        columns_sql = ', '.join(f'{name} {column_type}' for name, column_type in columns)
        return f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})'
    except Exception as err:
        raise ValueError(f'Something unexpected happened while trying to generate create table query: {err}') from err


def make_insert_table_query(table_name: str, columns: list[tuple[str, str]]) -> str:
    """

    """
    try:
        column_names = [name for name, _ in columns]
        placeholders = ', '.join('?' for _ in column_names)
        column_list = ', '.join(column_names)
        return f'INSERT OR IGNORE INTO {table_name} ({column_list}) VALUES ({placeholders})'
    except Exception as err:
        raise ValueError(f'Something unexpected happened while trying to generate insert or ignore query: {err}') from err


def init_tables(path: str, queries: list[str]) -> None:
    """

    """
    logger.info(f'Creating tables if they don\'t already exist ...')
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            for query in queries:
                logger.debug(f'Running query:\n{query}')
                cur.execute(query)
            conn.commit()
            logger.debug(f'Queries committed to the database.')
    except Exception as err:
        raise ValueError(f'Error creating tables: {err}') from err


def table_length(path: str, table: str) -> int:
    """

    """
    logger.info(f'Checking length of {table} table ...')
    try:
        with sqlite3.connect(path) as conn:
            return conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    except Exception as err:
        raise ValueError(f'Error getting {table} table length: {err}') from err



def populate_tables(path: str, queries:list[str], data: list) -> None:
    """

    """
    logger.info(f'Populating tables with list of data ...')
