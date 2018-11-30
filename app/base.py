import csv
import requests
from bs4 import BeautifulSoup
import logging
import os

logger = logging.getLogger(__name__)


class Basic_Crawler:

    @staticmethod
    def get_soup(url):
        logger.debug(f'Loading... {url}')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def save_to_csv(self, data, headers, filename):
        exists = False
        filename = f'{self.DATA_FOLDER}{filename}.csv'
        if os.path.exists(filename):
            exists = True
        with open(filename, 'a') as f:
            csvwriter = csv.DictWriter(f, fieldnames=headers)
            if not exists:
                csvwriter.writeheader()
            csvwriter.writerow(data)
