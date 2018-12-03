import csv
import requests
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Basic_Crawler:

    @staticmethod
    def get_soup(url):
        logger.debug(f'Loading... {url}')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def save_to_csv(self, data, base_dir, headers, filename):
        exists = False
        filename = f'{base_dir}{filename}'
        # logger.debug('Path: '+filename)
        if os.path.exists(filename):
            exists = True
        with open(filename, 'a') as f:
            csvwriter = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
            if not exists:
                csvwriter.writeheader()
            csvwriter.writerow(data)
