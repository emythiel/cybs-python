"""
Module for handling API calls.
"""

import logging
import requests
logger = logging.getLogger(__name__)


def fetch_token(url: str, email: str) -> str:
    """

    """
    headers = {'Content-Type': 'application/json'}
    data = {'email': email}

    logger.info(f'Fetching auth token from API at url {url} ...')

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        token = response.json().get('token')

        if not token:
            raise ValueError('Token missing from API response.')

        logger.info(f'Token retrieved from API.')
        logger.debug(token)
        return token
    except Exception as err:
        raise ValueError(f'Error fetching API token: {err}') from err


def fetch_incidents(url: str, token: str, skip: int = None, top: int = None) -> dict:
    """

    """
    headers = {'Authorization': f'Bearer {token}'}
    params = {'$skip': skip, '$top': top}

    logger.info(f'Fetching incident data from API at url {url} ...')

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError('Data missing from API response.')

        if data.get('value'):
            logger.info(f'Incident data retrieved from API, containing {len(data.get('value'))} incidents.')
        else:
            logger.info(f'Summary data retrieved from API.')

        return data
    except Exception as err:
        raise ValueError(f'Error fetching data from API: {err}') from err
