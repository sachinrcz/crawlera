import logging
from app.base import Basic_Crawler
import re
import os
import pandas as pd
from app import settings
import csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Artistang_Com(Basic_Crawler):

    def __init__(self, base_dir , csvfilename, base_domain, inputfilename):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename
        self.inputfilename = inputfilename

    def read_csv(self):
        filename = os.path.join(self.base_dir, self.inputfilename)
        logger.debug('Reading: {}'.format(filename))
        with open(filename) as f:
            reader = csv.DictReader(f)
            for row in reader:
                product_name = row['Product_Name']
                product_url = row['Product_URL']
                self.extract_details(product_name, product_url)

    def extract_details(self, product_name, product_url):
        soup = self.get_soup(product_url)
        headers = ['Product_Name', 'Manufacturer','Description','Features','Stock_Number','Product_URL']
        mfg = soup.find('a', attrs={'href':re.compile('/Mfgr/')})
        if mfg:
            mfg = mfg.text
        description = soup.select_one('div.normaltext')
        if description:
            description = description.text
        features = soup.select_one('div.cpfeatures')
        if features:
            features = features.text.strip(' Features  ')
        stocknum = soup.select_one('span.sti')
        if stocknum:
            stocknum = stocknum.text

        data ={
            'Product_Name': product_name,
            'Manufacturer': mfg,
            'Description': description,
            'Features': features,
            'Stock_Number':stocknum,
            'Product_URL':product_url,
        }
        self.save_to_csv(data=data, base_dir=self.base_dir, headers=headers, filename=self.csvfilename)

if __name__ == '__main__':
    base_dir = settings.BASE_DIR
    csvfilename = 'Artistang_Data_1.csv'
    base_domain = 'https://www.artisantg.com'
    inputfilename = 'Artisian Ecotech.csv'
    app = Artistang_Com(base_dir=base_dir, csvfilename=csvfilename, base_domain=base_domain, inputfilename=inputfilename)
    app.read_csv()
