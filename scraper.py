from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import urllib.parse
import traceback
import time
import datetime

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

            page.set_default_navigation_timeout(120000)
            page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"})

            today_str = datetime.now().strftime("%m/%d/%Y")

            MAX_PAGES = 10
            page_number = 1
            while page_number < MAX_PAGES:
                
                page = browser.new_page()
                page.set_default_navigation_timeout(120000)
                page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"})

                query_params = {
                    "st": term,
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
                    "caed": today_str,
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
                
                MAX_RETRIES = 3
                for attempt in range(MAX_RETRIES):
                    try:
                        time.sleep(2)
                        page.goto(full_url, wait_until="load") #run fly deploy again and check idk
                        break 

                    except Exception as e:
                        if attempt == MAX_RETRIES - 1:
                            # page.screenshot(path=f"error_page_{attempt}.png")
                            page.close()
                            raise e
                        else:
                            print(f"Retrying page.goto() attempt {attempt+1}")
                            # page.screenshot(path=f"error_page_{page_number}.png")
                            continue

                try:
                    page.wait_for_selector("div.feat-item", timeout=10000)
                except:
                    print(f"Timeout on page {page_number}")
                    page_number += 1
                    continue

                items = page.query_selector_all("div.feat-item")
                print(f"Page {page_number}: Found {len(items)} items")
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
                
                page.close()
                page_number += 1

            browser.close()
            return JSONResponse(content=results)

    except Exception as e:
        print("Scraping failed:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})