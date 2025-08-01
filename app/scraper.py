import requests
from bs4 import BeautifulSoup

def scrape_clothing(keyword):
    # Construct the full URL manually
    search_url = (
        "https://shopgoodwill.com/categories/listing?"
        f"st={keyword}&sg=&c=28&s=&lp=0&hp=999999&sbn=&spo=false&snpo=false"
        "&socs=false&sd=false&sca=false&caed=7%2F31%2F2025&cadb=7&scs=false"
        "&sis=false&col=1&p=1&ps=40&desc=false&ss=0&UseBuyerPrefs=true"
        "&sus=false&cln=2&catIds=-1,10,28&pn=&wc=false&mci=false&hmt=false"
        "&layout=grid&ihp=true"
    )

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
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
