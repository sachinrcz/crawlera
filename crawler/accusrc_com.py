import logging
from app.base import Basic_Crawler
import os
from app import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Accusrc_Com(Basic_Crawler):

    def __init__(self, base_dir, csvfilename, base_domain):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename

    def get_mfg_urls(self):
        soup = self.get_soup('https://accusrc.com/manufacturers')
        mfg_urls = []
        for item in soup.select('div.manufacturer-list a'):
            if item.has_attr('href'):
                mfg_urls.append((item.text, self.base_domain+item['href']))
        logger.debug(f'{len(mfg_urls)} Manufactures Found')
        return mfg_urls

    def run(self):
        mfg_urls = self.get_mfg_urls()
        for mfg, mfg_url in mfg_urls:
            logger.debug('Loading {}'.format(mfg))
            self.save_products(mfg, mfg_url)

    def save_products(self, mfgname, mfgurl):
        soup = self.get_soup(mfgurl)
        headers = ['ProdcutName', 'Manufacturer', 'Description','Price', 'ProductURL']
        for row in soup.select('div.caption'):
            name = row.select_one('h3 a').text.strip()
            desc = row.select_one('div.productdiscrption').text.strip()
            price = row.select_one('span.newprice')
            if price:
                price = price.text
            prod_url = self.base_domain+row.select_one('h3 a')['href']
            data = {
                'ProdcutName': name,
                'Manufacturer': mfgname.split('(')[0].strip(),
                'Price': price,
                'Description':desc,
                'ProductURL': prod_url
            }
            self.save_to_csv(data, self.base_dir, headers, self.csvfilename)
        next = soup.find('a', text='Next')
        if next:
            next = self.base_domain+next['href']
            logger.debug('Moving to next page: {}'.format(next))
            self.save_products(mfgname, next)


if __name__ == '__main__':
    base_dir = settings.BASE_DIR + 'accusrc/'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    csvfilename = 'Accusrc_Data_Sample.csv'
    base_domain = 'https://accusrc.com/'
    app = Accusrc_Com(base_dir=base_dir, csvfilename=csvfilename, base_domain=base_domain)
    app.run()