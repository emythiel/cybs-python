import logging
import time
import os

import requests

path = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=f'{path}/weather.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y%m%d-%H:%M:%S'
)

while True:
    response = requests.get('http://wttr.in/?format=3')
    response.raise_for_status()
    logger.info(f'Here is current weather: {response.text}')

    time.sleep(120)
