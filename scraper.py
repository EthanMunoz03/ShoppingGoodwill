from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import urllib.parse

router = APIRouter()

@router.get("/scrape")
def scrape_clothing(term: str = Query(...)):
    encoded_term = urllib.parse.quote_plus(term)

    base_url = "https://shopgoodwill.com/categories/listing"
    query_params = {
        "st": encoded_term,
        "sg": "",
        "c": "28",  # Men's clothing category
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

    # Define acceptable substrings for filtering by small sizes
    size_keywords = [
        "size s", "size small", " sz s", "sz sm", "sz small",
        "size - s", "sz - s", "sz - small"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(full_url, timeout=60000)

        # Wait for items to load
        page.wait_for_selector("div.feat-item", timeout=15000)

        items = page.query_selector_all("div.feat-item")

        results = []
        for item in items:
            title_el = item.query_selector("a.feat-item_name")
            price_el = item.query_selector("p.feat-item_price")
            img_el = item.query_selector("img.feat-item_img")

            title = title_el.get_attribute("title") if title_el else ""
            if not any(keyword in title.lower() for keyword in size_keywords):
                continue  # Skip if title does not match size small patterns

            price = price_el.inner_text().strip() if price_el else "No price"
            image = img_el.get_attribute("src") if img_el else None

            results.append({
                "title": title,
                "price": price,
                "image": image
            })

            if len(results) >= 10:
                break  # Limit to 10 matching results

        browser.close()
        return JSONResponse(content=results)