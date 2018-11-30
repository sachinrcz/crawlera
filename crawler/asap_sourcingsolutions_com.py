import logging
from app.base import Basic_Crawler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AsapSourcingSolutions_Com(Basic_Crawler):

    def __init__(self, base_dir, csvfilename, base_domain):
        self.base_domain = base_domain
        self.base_dir = base_dir
        self.csvfilename = csvfilename
        self.run()

    def get_product_links(self):
        soup = self.get_soup('https://www.asap-sourcingsolutions.com/manufacturer/')
        product_links = []
        for link in soup.select('a.capitalize'):
            product_links.append((link.text, self.base_domain + link['href']))
        product_links.sort()
        return product_links

    def run(self):
        product_links = self.get_product_links()
        logger.debug('Product Links: {}'.format(len(product_links)))


if __name__ == '__main__':
    app = AsapSourcingSolutions_Com(base_dir='',csvfilename='',base_domain='')