"""
Module for handling API calls.
"""

import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import config as conf

logger = logging.getLogger(__name__)

# Setup retry logic
retry_strategy = Retry(
    total = 3,
    status_forcelist=[429,500,502,503,504],
    allowed_methods=["GET","POST"],
    backoff_factor=2
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("http://", adapter)


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
        response = http.post(url, headers=headers, json=data)
        response.raise_for_status()

        token = response.json().get('token')

        if not token:
            raise ValueError('Token missing from API response.')

        logger.debug(f'Token retrieved from API: {token}')
        return token

    except Exception as err:
        raise ValueError(f'Error fetching API token: {err}') from err


def fetch_incidents(url: str, token: str, skip: int = None, top: int = None) -> tuple[dict, str]:
    """
    Fetch incident data from URL.
    Parameters:
        url (str): URL to request data from.
        token (str): Token to authenticate with.
        skip (int): (optional) Amount of incidents to skip from API.
        top (int): (optional) Amount of incidents to request (1-100).
    Returns:
        tuple[dict, str]: Response data and token in case it was refreshed.
    """
    headers = {'Authorization': f'Bearer {token}'}
    params = {'$skip': skip, '$top': top}

    logger.debug(f'Fetching incident data from API at url {url} ...')

    try:
        response = http.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get('value'):
            logger.debug(f'Incident data retrieved from API, containing {len(data.get("value", []))} incidents.')

        return data, token

    except requests.exceptions.HTTPError as err:
        status = err.response.status_code

        if status == 401:
            logger.warning('Token expired. Refreshing token...')

            new_token = fetch_token(f'{conf.BASE_URL}/api/auth/token', conf.STUDENT_EMAIL)

            # retry with new token
            headers['Authorization'] = f'Bearer {new_token}'
            response = http.get(url, headers=headers, params=params)
            response.raise_for_status()

            return response.json(), new_token  # return new token so we don't constantly refresh it

    except Exception as err:
        raise ValueError(f'Error fetching data from API: {err}') from err
