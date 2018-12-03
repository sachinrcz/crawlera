import logging
from app.base import Basic_Crawler
import os
from app import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Torontosurplus_Com(Basic_Crawler):

    def __init__(self, base_dir, csvfilename, base_domain):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename

    def get_mfg_urls(self):
        soup = self.get_soup('https://www.torontosurplus.com/manufacturerList/')
        mfg_urls = []
        for item in soup.select_one('div.box.best-selling table').select('a'):
            if item.has_attr('href'):
                mfg_urls.append((item.text, item['href']))
        logger.debug(f'{len(mfg_urls)} Manufactures Found')
        return mfg_urls

    def run(self):
        mfg_urls = self.get_mfg_urls()
        for mfg, mfg_url in mfg_urls:
            logger.debug('Loading {}'.format(mfg))
            self.page_count = 1
            self.save_products(mfg, mfg_url)


    def save_products(self, mfgname, mfgurl):
        soup = self.get_soup(mfgurl)
        headers = ['ProdcutName', 'Manufacturer', 'Price', 'ProductURL']
        for row in soup.select('div.listing-item'):
            name = row.select_one('h5 a')['title'].strip()
            price = row.select_one('span.price')
            if price:
                price = price.text
            prod_url = row.select_one('h5 a')['href']
            data = {
                'ProdcutName': name,
                'Manufacturer': mfgname,
                'Price': price,
                'ProductURL': prod_url
            }
            self.save_to_csv(data, self.base_dir, headers, self.csvfilename)
        self.page_count += 1
        next = soup.find('a', text=str(self.page_count))
        if next:
            next = next['href']
            logger.debug('Moving to next page: {}'.format(next))
            self.save_products(mfgname, next)


if __name__ == '__main__':
    base_dir = settings.BASE_DIR + 'torontosurplus/'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    csvfilename = 'Torontosurplus_Data_Sample.csv'
    base_domain = 'https://www.torontosurplus.com'
    app = Torontosurplus_Com(base_dir=base_dir, csvfilename=csvfilename, base_domain=base_domain)
    app.run()