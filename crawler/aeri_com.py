import logging
from app.base import Basic_Crawler
import os
from app import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Aeri_Com(Basic_Crawler):

    def __init__(self, base_dir , csvfilename, base_domain):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename

    def get_mfg_urls(self):
        soup = self.get_soup('https://www.aeri.com/products/')
        mfg_urls = []
        for i in range(5, 9):
            col = soup.select('div.col-sm-3')[i]
            for item in col.select('a'):
                if item.has_attr('href'):
                    mfg_urls.append((item.text, 'http:' + item['href']))

        return mfg_urls

    def run(self):
        mfg_urls = self.get_mfg_urls()
        for mfg, mfg_url in mfg_urls:
            logger.debug('Loading {}:{}'.format(mfg, mfg_url))
            self.save_products(mfg, mfg_url)

    def save_products(self, mfgname, mfgurl):
        soup = self.get_soup(mfgurl)
        headers = ['PartNumber', 'Manufacturer', 'Description', 'Status', 'ProductURL']
        for row in soup.select('tr.result'):
            if len(row.select('td')) > 3:
                part_num = row.select('td')[0].text
                description = row.select('td')[1].text
                status = row.select('td')[2].text
                prod_url = self.base_domain + row.select_one('a')['href']
                data = {
                    'PartNumber':part_num,
                    'Manufacturer':mfgname,
                    'Description':description,
                    'Status':status,
                    'ProductURL':prod_url
                }
                self.save_to_csv(data,self.base_dir,headers,self.csvfilename)
        next = soup.find('a',text='Next »')
        if next:
            next = mfgurl.split('?')[0].strip() + next['href']
            logger.debug('Moving to next page: {}'.format(next))
            self.save_products(mfgname, next)

if __name__ == '__main__':
    base_dir = settings.BASE_DIR +'aeri/'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    csvfilename = 'Aeri_Data_Sample.csv'
    base_domain = 'https://www.aeri.com'
    app = Aeri_Com(base_dir=base_dir, csvfilename=csvfilename, base_domain=base_domain)
    app.run()

