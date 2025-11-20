"""
Module for handling API calls.
"""

import logging
import requests
logger = logging.getLogger(__name__)


def fetch_token(url: str, email: str) -> str:
    """
    Fetch authentication token from URL.
    Parameters:
        url (str): URL to request token from.
        email (str): Valid student email to authorize with.
    Returns:
        token (str): Authentication token.
    """
    headers = {'Content-Type': 'application/json'}
    data = {'email': email}

    logger.debug(f'Fetching auth token from API at url {url} ...')

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        token = response.json().get('token')

        if not token:
            raise ValueError('Token missing from API response.')

        logger.debug(f'Token retrieved from API: {token}')
        return token

    except Exception as err:
        raise ValueError(f'Error fetching API token: {err}') from err


def fetch_incidents(url: str, token: str, skip: int = None, top: int = None) -> dict:
    """
    Fetch incident data from URL.
    Parameters:
        url (str): URL to request data from.
        token (str): Token to authenticate with.
        skip (int): (optional) Amount of incidents to skip from API.
        top (int): (optional) Amount of incidents to request (1-100).
    Returns:
        data (dict): JSON response body converted to Python object.

    """
    headers = {'Authorization': f'Bearer {token}'}
    params = {'$skip': skip, '$top': top}

    logger.debug(f'Fetching incident data from API at url {url} ...')

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError('Data missing from API response.')

        if data.get('value'):
            logger.debug(f'Incident data retrieved from API, containing {len(data.get('value'))} incidents.')

        return data

    except Exception as err:
        raise ValueError(f'Error fetching data from API: {err}') from err
