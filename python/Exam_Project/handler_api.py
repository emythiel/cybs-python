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
        response = _request_with_retries("GET", url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        if data.get('value'):
            logger.debug(f'Incident data retrieved from API, containing {len(data.get('value', []))} incidents.')

        return data

    except requests.exceptions.HTTPError as err:
        status = err.response.status_code

        if status == 401:
            logger.warning("Token expired. Refreshing token...")

            new_token = fetch_token(f'{conf.BASE_URL}/api/auth/token', conf.STUDENT_EMAIL)

            # retry with new token
            headers['Authorization'] = f'Bearer {new_token}'
            response = _request_with_retries("GET", url, headers=headers, params=params)
            response.raise_for_status()

            return response.json()

    except Exception as err:
        raise ValueError(f'Error fetching data from API: {err}') from err


def _request_with_retries(method: str, url: str, **kwargs):
    """
    Helper fuction to send requests with retry logic on errors.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.request(method, url, timeout=30, **kwargs)

            # Retry on 5xx server errors
            if 500 <= response.status_code < 600:
                logger.warning(f'Server error {response.status_code} '
                               f'{attempt}/{MAX_RETRIES}. Retrying...')
                raise requests.exceptions.HTTPError(f'5xx {response.status_code}', response=response)

            response.raise_for_status()
            return response

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError) as err:
            logger.warning(
                f'Network error on attempt {attempt}/{MAX_RETRIES} '
                f'for {method.upper()} {url}: {err}'
            )

            if attempt == MAX_RETRIES:
                raise ValueError(f'Network error after {MAX_RETRIES} attempts: {err}') from err

            sleep_time = RETRY_BACKOFF ** (attempt - 1)
            logger.debug(f'Sleeping {sleep_time}s before retrying...')
            time.sleep(sleep_time)

        except requests.exceptions.HTTPError as err:
            status = err.response.status_code

            if 500 <= status < 600:
                if attempt == MAX_RETRIES:
                    raise ValueError(f'Server error {status} after {MAX_RETRIES} attempts.') from err

                sleep_time = RETRY_BACKOFF ** (attempt - 1)
                logger.debug(f'Sleeping {sleep_time}s before retrying...')
                time.sleep(sleep_time)
            else:
                raise

        except Exception as err:
            raise ValueError(f'Unexpected error during request: {err}') from err
