import logging
from app.base import Basic_Crawler
import os
from app import settings
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Bellnw_Com(Basic_Crawler):

    def __init__(self, base_dir, csvfilename, base_domain):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename

    def get_mfg_urls(self):
        soup = self.get_soup(self.base_domain)
        mfg_urls = []
        for item in soup.findAll('a', attrs={'href': re.compile('/manufacturer/(\w+)/index.htm')}):
            mfg_urls.append(item['href'])
        mfg_urls = list(set(mfg_urls))
        mfg_urls.sort()
        logger.debug(f'{len(mfg_urls)} Manufactures Found')
        return mfg_urls

    def run(self):
        mfg_urls = self.get_mfg_urls()
        for mfg_url in mfg_urls:
            self.save_products_urls(mfg_url)

    def save_products_urls(self, mfgurl):
        soup = self.get_soup(mfgurl)
        headers = ['ProdcutName', 'Manufacturer', 'PartNumber', 'ShortDescription','Condition','ProductURL']
        mfg = soup.select_one('li.last').text
        for item in soup.select('table.productlistv2 tr')[1:]:
            product_url = item.select_one('td a')['href']
            product_name = item.select('td')[0].text.strip()
            short_desc = item.select('td')[1].text.strip()
            condition = item.select('td')[2].text.strip()
            logger.debug(product_url)
            partnum = re.search('/manufacturer/(\w+)/(.*).htm',product_url).group(2)

            data = {
                'ProdcutName': product_name,
                'Manufacturer': mfg,
                'ShortDescription': short_desc,
                'Condition': condition,
                'ProductURL': product_url,
                'PartNumber':partnum,
            }
            self.save_to_csv(data, self.base_dir, headers, self.csvfilename)


if __name__ == '__main__':
    base_dir = settings.BASE_DIR + 'bellnw/'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    csvfilename = 'BellNW_Data_Sample.csv'
    base_domain = 'https://www.bellnw.com'
    app = Bellnw_Com(base_dir=base_dir, csvfilename=csvfilename, base_domain=base_domain)
    app.run()