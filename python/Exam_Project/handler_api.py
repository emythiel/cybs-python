"""
Module for handling API calls.
"""

import logging
import time
import requests

import config as conf

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_BACKOFF = 2  # multiplier for exponential backoff


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
        response = _request_with_retries("POST", url, headers=headers, json=data)
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
        response = _request_with_retries("GET", url, headers=headers, params=params)
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
            response = _request_with_retries("GET", url, headers=headers, params=params)
            response.raise_for_status()

            return response.json(), new_token  # return new token so we don't constantly refresh it

    except Exception as err:
        raise ValueError(f'Error fetching data from API: {err}') from err


def _request_with_retries(method: str, url: str, **kwargs):
    """
    Helper fuction ued by `fetch_token` and `fetch_incidents`.\n
    Handles sending requests with retry logic.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()

            return response

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            logger.warning(f'Network error on attempt {attempt}/{MAX_RETRIES} for {method} {url}: {err}')

            if attempt == MAX_RETRIES:
                raise ValueError(f'Network error after {MAX_RETRIES} attempts: {err}') from err

            sleep_time = RETRY_BACKOFF ** (attempt - 1)  # exponential sleep timer
            logger.debug(f'Sleeping {sleep_time}s before retrying...')
            time.sleep(sleep_time)

        except requests.exceptions.HTTPError as err:
            status = err.response.status_code

            # 5xx error, retry
            if 500 <= status < 600:
                if attempt == MAX_RETRIES:
                    raise ValueError(f'Server error {status} after {MAX_RETRIES} attempts.') from err

                logger.warning(f'Server error {status} {attempt}/{MAX_RETRIES}. Retrying...')

                sleep_time = RETRY_BACKOFF ** (attempt - 1)  # exponential sleep timer
                logger.debug(f'Sleeping {sleep_time}s before retrying...')
                time.sleep(sleep_time)
            elif status == 401:
                raise  # raise to the calling function
            else:
                raise ValueError(f'HTTP Error {status} fetching from API: {err}')

        except Exception as err:
            raise ValueError(f'Unexpected error during request: {err}') from err
