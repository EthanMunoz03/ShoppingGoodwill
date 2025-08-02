from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from scraper import scrape_clothing
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from scraper import router

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
