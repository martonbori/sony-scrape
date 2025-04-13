

import requests
from bs4 import BeautifulSoup
import logging
import sys

# Set up logging
log = logging.getLogger(__name__)

BASE_URL = "https://www.sony.co.uk/store/search?query=:relevance:normalSearch:true"

class Scraper:
    def __init__(self, base_url=BASE_URL, filters=["audio", "headphones"]):
        filter = ":".join([f"category:gwx-{filt}" for filt in filters])
        self.url = ":".join([base_url, filter])

    def get_products(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('sn-product-grid-item')
        return products
    
    def parse_products(self, products):
        for product in products:
            log.info(product.prettify())
            break

    
    def __call__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        page = 0
        status = 200
        while status == 200: 
            response = requests.get(f"{self.url}&currentPage={page}", headers=headers)
            products = self.get_products(response=response)
            parsed_prodcuts = self.parse_products(products=products)
            status = response.status_code
            log.info(status)
            page += 1

        return self


if __name__ == "__main__":
    log.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    log.addHandler(handler)

    product_scraper = Scraper()
    product_scraper = product_scraper()
