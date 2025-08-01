import requests
from bs4 import BeautifulSoup

def scrape_clothing(keyword):
    base_url = "https://www.shopgoodwill.com/categories/listing"
    params = {
        "st": keyword,
        "sg": "",
        "c": "28",
        "s": "",
        "lp": 0,
        "hp": 999999,
        "sbn": "",
        "spo": "false",
        "snpo": "false",
        "socs": "false",
        "sd": "false",
        "sca": "false",
        "caed": "7/31/2025",
        "cadb": 7,
        "scs": "false",
        "sis": "false",
        "col": 1,
        "p": 1,
        "ps": 40,
        "desc": "false",
        "ss": 0,
        "UseBuyerPrefs": "true",
        "sus": "false",
        "cln": 2,
        "catIds": "-1,10,28",
        "pn": "",
        "wc": "false",
        "mci": "false",
        "hmt": "false",
        "layout": "grid",
        "ihp": "true"
    }
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    items = []
    for item_div in soup.select("app-home-product-items"):
        title_tag = item_div.select_one(".feat-item_name")
        price_tag = item_div.select_one(".feat-item_price")
        img_tag = item_div.select_one("img.feat-item_img")

        if title_tag and price_tag:
            title = title_tag.text.strip()
            price = price_tag.text.strip()
            url = "https://www.shopgoodwill.com" + title_tag["href"]
            image_url = img_tag["src"] if img_tag else None

            items.append({
                "title": title,
                "url": url,
                "price": price,
                "image": image_url
            })

    print(soup.prettify()[:1000])

    return items
