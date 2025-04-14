# Sony webshop scraper

This is a python script that scrapes sony's webshop (sony.co.uk/store) and extracts product data of all the available headphones in the store. The gathered data are then exported to a csv file.

In my solution I created a scraper class that is capable of extracting different types of products, not just headphones by changing the search filters of the request.

While scraping, I've found a product with no price listed. I've decided to store the product as the others, but left the price data empty

## Setup and run
 - If not already installed, download and install poetry from [here](https://github.com/python-poetry/install.python-poetry.org)
 - Navigate to the project root folder and run `poetry install`
 - Run the script with `poetry run python main.py`
