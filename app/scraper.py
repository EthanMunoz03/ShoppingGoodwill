import requests
from bs4 import BeautifulSoup

def scrape_clothing(keyword):
    base_url = "https://www.shopgoodwill.com/categories/listing"
    params = {"st": keyword, "c": 28}  # category 28 = men's clothing
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    for item in soup.select(".product-info"):
        title = item.select_one(".product-title a")
        price = item.select_one(".price")
        if title and price:
            items.append({
                "title": title.text.strip(),
                "url": title["href"],
                "price": price.text.strip()
            })

    return items
