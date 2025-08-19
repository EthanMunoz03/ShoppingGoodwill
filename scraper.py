from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import traceback
from datetime import date
import time
import urllib

router = APIRouter()

@router.get("/scrape")
def scrape_clothing(term: str = Query(...)):
    base_url = "https://shopgoodwill.com/categories/listing"
    item_base_url = "https://shopgoodwill.com"

    size_keywords = [
        "size s", "size small", " sz s", "sz sm", "sz small",
        "size - s", "sz - s", "sz - small", "Men's Small"
    ]

    results = []
    today_str = date.today().strftime("%m/%d/%Y")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-gpu',
                    '--disable-dev-shm-usage',
                    '--disable-setuid-sandbox',
                    '--no-sandbox',
                    '--disable-extensions'
                ]
            )
            page = browser.new_page()
            page.set_default_navigation_timeout(120000)
            page.set_default_timeout(30000)
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            })

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
            print(f"Navigating to: {full_url}")
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    page.goto(full_url, wait_until="load", timeout=150000)
                    break
                except Exception as e:
                    retry_count += 1
                    print(f"Navigation attempt {retry_count} failed: {str(e)}")
                    if retry_count == max_retries:
                        raise Exception(f"Failed to load page after {max_retries} attempts")
                    time.sleep(10)

            MAX_PAGES = 5
            pages_scraped = 0

            while pages_scraped < MAX_PAGES:
                try:
                    page.wait_for_selector("div.feat-item.ng-star-inserted", timeout=15000)
                except:
                    print(f"No items found on page {pages_scraped + 1}")
                    break

                items = page.query_selector_all("div.feat-item.ng-star-inserted")
                print(f"Page {pages_scraped + 1}: Found {len(items)} items")
                if not items:
                    break

                actual_count = 0

                for item in items:
                    title_el = item.query_selector("a.feat-item_name")
                    price_el = item.query_selector("p.feat-item_price")
                    img_el = item.query_selector("img.feat-item_img")
                    link_el = item.query_selector("a.feat-item_name")

                    title = title_el.get_attribute("title") if title_el else ""
                    if not any(keyword in title.lower() for keyword in size_keywords):
                        continue

                    actual_count += 1

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

                print(f"Found {actual_count} items in your size")

                pages_scraped += 1

                next_button = page.query_selector("button.p-paginator-next")
                if next_button and next_button.is_enabled():
                    print("Clicked next button")
                    next_button.click()
                    page.wait_for_selector("div.feat-item.ng-star-inserted", timeout=100000)
                    time.sleep(5)
                    page.wait_for_load_state("load", timeout=240000)
                else:
                    break

            browser.close()
            return JSONResponse(content=results)

    except Exception as e:
        print("Scraping failed:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
