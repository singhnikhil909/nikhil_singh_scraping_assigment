import requests
from bs4 import BeautifulSoup
import pandas as pd

class ChocolatScraper:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        self.base_url = "https://www.lechocolat-alainducasse.com"
        self.data = []

    def scrape(self):
        k = requests.get("https://www.lechocolat-alainducasse.com/uk/").text
        soup = BeautifulSoup(k, 'html.parser')
        productlist = soup.find_all("li", {"class": "homeCategoryPads__item"})

        for product in productlist:
            link = product.find("a", {"class": "homeCategoryPads__itemLink"}).get('href')
            k_2 = requests.get(self.base_url + link).text
            soup_2 = BeautifulSoup(k_2, 'html.parser')
            productlist_2 = soup_2.find_all("li", {"class": "subcategories__item"})
            productlist_2 = productlist_2[1:]
            for product_2 in productlist_2:
                link_2 = product_2.find("a", {"class": "categoryLink"}).get('href')
                k_3 = requests.get(link_2).text
                soup_3 = BeautifulSoup(k_3, 'html.parser')
                productlist_3 = soup_3.find_all("div", {"class": "productMiniature js-product-miniature"})
                for product_3 in productlist_3:
                    link_3 = product_3.find("a", {"class": "productMiniature__name"})
                    if link_3:
                        link_3 = link_3.get('href')
                        f = requests.get(link_3, headers=self.headers).text
                        hun = BeautifulSoup(f, 'html.parser')
                        price = hun.find("button", {"class": "productActions__addToCart button add-to-cart add"}).text.replace('Add', "").strip()
                        description = hun.find("div", {"class": "productDescription"}).text.strip()
                        shelf_life = hun.find("p", {"class": "consumeAdvices"}).text.strip()
                        weight = hun.find("p", {"class": "productCard__weight"}).text.strip()
                        name = hun.find("h1", {"class": "productCard__title"}).text.replace("\n", "").strip()
                        self.data.append([name, price, description, shelf_life, weight])

    def to_dataframe(self):
        df = pd.DataFrame(self.data, columns=['Name', 'Price', 'Description', 'Shelf Life', 'Weight'])
        return df

# Example usage:
scraper = ChocolatScraper()
scraper.scrape()
df = scraper.to_dataframe()
df.to_csv('scraped_data/chocolate_data.csv')