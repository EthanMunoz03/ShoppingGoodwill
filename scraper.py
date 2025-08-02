from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import urllib.parse
import traceback

router = APIRouter()

@router.get("/scrape")
def scrape_clothing(term: str = Query(...)):
    encoded_term = urllib.parse.quote_plus(term)

    base_url = "https://shopgoodwill.com/categories/listing"
    item_base_url = "https://shopgoodwill.com"

    size_keywords = [
        "size s", "size small", " sz s", "sz sm", "sz small",
        "size - s", "sz - s", "sz - small"
    ]

    results = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page_number = 1
            while True:
                query_params = {
                    "st": encoded_term,
                    "sg": "",
                    "c": "28",
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
                    "p": str(page_number),
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
                page.goto(full_url, timeout=60000)

                try:
                    page.wait_for_selector("div.feat-item", timeout=10000)
                except:
                    break  # No more results or failed to load

                items = page.query_selector_all("div.feat-item")
                if not items:
                    break

                for item in items:
                    title_el = item.query_selector("a.feat-item_name")
                    price_el = item.query_selector("p.feat-item_price")
                    img_el = item.query_selector("img.feat-item_img")
                    link_el = item.query_selector("a.feat-item_name")

                    title = title_el.get_attribute("title") if title_el else ""
                    if not any(keyword in title.lower() for keyword in size_keywords):
                        continue

                    price = price_el.inner_text().strip() if price_el else "No price"
                    image = img_el.get_attribute("src") if img_el else None
                    relative_link = link_el.get_attribute("href") if link_el else ""
                    full_link = item_base_url + relative_link if relative_link else None

                    results.append({
                        "title": title,
                        "price": price,
                        "image": image,
                        "link": full_link
                    })

                page_number += 1

            browser.close()
            return JSONResponse(content=results)

    except Exception as e:
        print("Scraping failed:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})