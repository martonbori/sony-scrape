from __future__ import annotations

import logging
import sys

import pandas
import requests

from data import Product

# Set up logging
log = logging.getLogger(__name__)

API_BASE = 'https://www.sony.co.uk/commerceapi/rest/v2/sony-uk/products/'
STORE_BASE = 'https://www.sony.co.uk/store'


class ProductScraper:
    def __init__(
        self,
        api_base=API_BASE,
        store_base_url=STORE_BASE,
        filters=['audio', 'headphones'],
    ):
        filter = ':'.join([f"category:gwx-{filt}" for filt in filters])
        query = f':relevance:normalSearch:true:{filter}'
        search_term = f"search?query={query}&pageSize=12&lang=en_GB&curr=GBP"

        self.api_url = ''.join([api_base, search_term])
        self.store_url = store_base_url
        self.products = []

    def get_products(self, response):
        full_products = response.json()['products']
        products = []
        for fp in full_products:
            if ('price' in fp):
                price = fp['price']['value']
            else:
                price = None

            product = Product(
                name=fp['name'],
                price=price,
                mpn=fp['code'],
                url=f"{self.store_url}{fp['url']}",
            )
            products.append(product)
        return products

    def export_to_csv(self, file_path):
        dataframe = pandas.DataFrame(self.products)
        dataframe.to_csv(file_path, index=False)
        log.info(f"Data exported to {file_path}")

    def __call__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }

        log.info('Fetching products...')
        pagination = requests.get(
            f"{self.api_url}&fields=pagination(DEFAULT)", headers=headers,
        ).json()['pagination']

        log.info(f"Found {pagination['totalResults']} product.")
        for i in range(pagination['totalPages']):
            log.info(f"Fetching page {i}...")
            product_fields = ['name', 'price(value)', 'code', 'url']
            response = requests.get(
                f"{self.api_url}"
                f"&fields=products({','.join(product_fields)})"
                f"&currentPage={i}",
                headers=headers,
            )
            products = self.get_products(response=response)
            log.info(f"Extracted {len(products)} product.")
            self.products.extend(products)

        return self


def setup_logger():
    log.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    log.addHandler(handler)


if __name__ == '__main__':
    setup_logger()
    product_scraper = ProductScraper()
    product_scraper = product_scraper()
    product_scraper.export_to_csv('headphones.csv')
