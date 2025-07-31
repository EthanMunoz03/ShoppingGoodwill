from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from app.scraper import scrape_clothing

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the ShopGoodwill scraper API!"}

@app.get("/scrape")
def scrape(keyword: str = Query(..., description="Search keyword for clothing")):
    try:
        results = scrape_clothing(keyword)
        return JSONResponse(content={"results": results})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
