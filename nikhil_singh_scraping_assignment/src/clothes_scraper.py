import requests
from bs4 import BeautifulSoup
import pandas as pd

class ForeignFortuneScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.href_values = []

    def scrape(self):
        k = requests.get(self.base_url).text
        soup = BeautifulSoup(k, 'html.parser')
        productlist = soup.find_all("a", {"class": "site-nav__link site-nav__link--main"})

        if productlist:
            self.href_values = [self.base_url + tag['href'] for tag in productlist if 'href' in tag.attrs]

    def extract_data(self):
        data = []
        for link in self.href_values:
            f = requests.get(link).text
            soup_1 = BeautifulSoup(f, 'html.parser')
            productlist_1 = soup_1.find_all("div", {"class": "grid__item grid__item--collection-template small--one-half medium-up--one-quarter"})

            for product in productlist_1:
                product_link = product.find("a", {"class": "grid-view-item__link grid-view-item__image-container product-card__link"})
                if product_link:
                    product_link = self.base_url + product_link.get('href')
                    j = requests.get(product_link).text
                    hun = BeautifulSoup(j, 'html.parser')
                    price = hun.find("span", {"class": "product-price__price product-price__price-product-template"}).text.replace('Sale', '').strip()
                    description = hun.find("div", {"class": "product-single__description rte"}).text.strip()
                    name = hun.find("h1", {"class": "product-single__title"}).text.strip()
                    size = hun.find("select", {"class": "single-option-selector single-option-selector-product-template product-form__input", "id": "SingleOptionSelector-0"})
                    color = hun.find("select", {"class": "single-option-selector single-option-selector-product-template product-form__input", "id": "SingleOptionSelector-1"})
                    variant = hun.find("select", {"class": "single-option-selector single-option-selector-product-template product-form__input", "id": "SingleOptionSelector-2"})
                    if size:
                        size = size.text.replace('\n', ' ').strip()
                    else:
                        size = ""
                    if color:
                        color = color.text.replace('\n', ' ').strip()
                    else:
                        color = ""
                    if variant:
                        variant = variant.text.replace('\n', ' ').strip()
                    else:
                        variant = ""
                    if name:
                        name = name.replace('\n', ' ').strip()
                    else:
                        name = ""

                    data.append([name, price, description, size, color, variant])
        return data

    def to_dataframe(self, data):
        df = pd.DataFrame(data, columns=['Name', 'Price', 'Description', 'Size', 'Color', 'Variant'])
        return df


base_url = "https://foreignfortune.com"
scraper = ForeignFortuneScraper(base_url)
scraper.scrape()
data = scraper.extract_data()
df = scraper.to_dataframe(data)
df.to_csv('scraped_data/chocolate_data.csv')