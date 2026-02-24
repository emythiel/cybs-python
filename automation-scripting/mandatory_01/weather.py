import logging
import datetime
import time
import os

import geocoder
import requests

path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f'{path}/weather.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y%m%d-%H:%M:%S'
)

now = datetime.datetime.now()

IP = geocoder.ip("me")
CITY = IP.city

while True:
    response = requests.get(f'http://wttr.in/{CITY}?format=3')
    response.raise_for_status()

    data = response.text

    logger.info(f'Here is current weather: {response.text}')

    time.sleep(120)
