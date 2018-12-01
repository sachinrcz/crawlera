import logging
from app.base import Basic_Crawler
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AsapSourcingSolutions_Com(Basic_Crawler):

    def __init__(self, base_dir, csvfilename, base_domain):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename

    def get_product_links(self, url):
        soup = self.get_soup(url)
        product_links = []
        for link in soup.select('a.capitalize'):
            product_links.append((link.text, self.base_domain + link['href']))
        product_links.sort()
        return product_links

    def save_product_details(self, manufacturer, product_url):
        soup = self.get_soup(product_url)
        self.csvfilename = manufacturer + '.csv'
        headers = ['Manufacturer', 'Part_Number', 'Specification',
                   'NSN_Number', 'QTY', 'CAGE_NUMBER', 'Product_URL', 'Source_URL']
        cage_code = -1
        try:
            cage_code = re.search('(\d+)', soup.select('div.col-lg-9.rhs.m_t50 div span')[0].text).group(0)
        except:
            pass
        logger.debug('{} Products Found'.format(len(soup.select('table tr'))))
        for item in soup.select('table tr')[1:]:
            product_link = self.base_domain + item.select_one('a')['href']
            part_number = item.select_one('a').text
            specification = item.select('td')[1].text
            nsn_number = item.select('td')[2].text
            qty = item.select('td')[3].text
            data = {
                'Manufacturer': manufacturer,
                'Part_Number': part_number,
                'Specification': specification,
                'NSN_Number': nsn_number,
                'QTY': qty,
                'CAGE_NUMBER': cage_code,
                'Product_URL': product_link,
                'Source_URL': product_url
            }
            #         print(data)
            self.save_to_csv(data=data, base_dir=self.base_dir, filename=self.csvfilename, headers=headers)

        next_url = soup.select_one('a.pagination-next')
        if next_url:
            print('Loading Next Page')
            self.save_product_details(manufacturer, self.base_domain + next_url['href'])

    def run(self):
        url = 'https://www.asap-sourcingsolutions.com/manufacturer/'
        product_links = self.get_product_links(url)
        logger.debug('Product Links: {}'.format(len(product_links)))
        index = 0
        for i, item in enumerate(product_links[index:]):
            logger.debug('{}: Extracting: {} '.format(i + index + 1, item[0]))
            self.save_product_details(item[0], item[1])

        # soup = self.get_soup('https://www.asap-sourcingsolutions.com/manufacturer/')
        # for item in soup.select('ul#owl-demo03 a')[1:]:
        #     url = self.base_domain + item['href']
        #     logger.debug(url)
        #     product_links = self.get_product_links(url)
        #     logger.debug('Product Links: {}'.format(len(product_links)))
        #     index = 0
        #     for i, item in enumerate(product_links[index:100]):
        #         logger.debug('{}: Extracting: {} '.format(i + index + 1, item[0]))
        #         self.save_product_details(item[0], item[1])


if __name__ == '__main__':
    base_dir = 'data/'
    csvfilename = 'AsapSourcingSolutions_Com.csv'
    base_domain = 'https://www.asap-sourcingsolutions.com'
    app = AsapSourcingSolutions_Com(base_dir=base_dir, csvfilename=csvfilename, base_domain=base_domain)
    app.run()
