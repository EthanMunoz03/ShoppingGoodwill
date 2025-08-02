from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import urllib.parse

router = APIRouter()

@router.get("/scrape")
def scrape_shopgoodwill(term: str = Query(...)):
    # Construct URL for search term (defaulting to men's clothing category)
    encoded_term = urllib.parse.quote_plus(term)

    base_url = "https://shopgoodwill.com/categories/listing"
    query_params = {
        "st": encoded_term,
        "sg": "",
        "c": "28",  # Men's clothing
        "s": "",
        "lp": "0",
        "hp": "999999",
        "sbn": "",
        "spo": "false",
        "snpo": "false",
        "socs": "false",
        "sd": "false",
        "sca": "false",
        "caed": "",
        "cadb": "7",
        "scs": "false",
        "sis": "false",
        "col": "1",
        "p": "1",
        "ps": "40",
        "desc": "false",
        "ss": "0",
        "UseBuyerPrefs": "true",
        "sus": "false",
        "cln": "2",
        "catIds": "-1,10,28",
        "pn": "",
        "wc": "false",
        "mci": "false",
        "hmt": "false",
        "layout": "grid",
        "ihp": ""
    }

    full_url = base_url + "?" + urllib.parse.urlencode(query_params)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(full_url)

        # Wait for listings
        page.wait_for_selector("div.product-grid", timeout=10000)

        items = page.query_selector_all("div.product-grid div.product-item")

        results = []
        for item in items[:10]:
            title = item.query_selector("div.product-title")
            price = item.query_selector("div.product-price")
            img = item.query_selector("img")

            results.append({
                "title": title.inner_text().strip() if title else "No title",
                "price": price.inner_text().strip() if price else "No price",
                "image": img.get_attribute("src") if img else None
            })

        browser.close()
        return JSONResponse(content=results)
