# Make a program that requests access to:
# https://testpages.eviltester.com/styled/auth/basic-auth-test.html
# Read the content of the page and find the "protected URL".
# Make your program access the protected URL, by setting a Basic Auth Header as part of the request.
# Response should contain "This page is the result of accessing the basic authentication protected page."
# Bonus: Make your program parse the values (username and password) from first response, and use in second request.

import requests, re
from requests.auth import HTTPBasicAuth

URL = 'https://testpages.eviltester.com/styled/auth/basic-auth-test.html'
SECRET_URL = 'https://testpages.eviltester.com/styled/auth/basic-auth-results.html'

def get_credentials(html):
    # Look for "username: value" and "password: value"
    user_m = re.search(r'username\s*:\s*([^\s<]+)', html, flags=re.IGNORECASE)
    pass_m = re.search(r'password\s*:\s*([^\s<]+)', html, flags=re.IGNORECASE)
    user = user_m.group(1) if user_m else None
    pwd = pass_m.group(1) if pass_m else None
    return user, pwd

def request_auth(user, pwd):
    response = requests.get(SECRET_URL, auth=(user, pwd))
    response.raise_for_status()
    if response.status_code == 200:
        print(response.text)
    else:
        print(f'[ERROR] Could not get a response, status code: {response.status_code}')

def request_basic():
    response = requests.get(URL)
    response.raise_for_status()
    if response.status_code == 200:
        html = response.text
        user, pwd = get_credentials(html)
        request_auth(user, pwd)
    else:
        print(f'[ERROR] Could not get a response, status code: {response.status_code}')

request_basic()
