from fastapi import FastAPI
from app.routes import user, scraper, preference, articles

app = FastAPI(title="Sentinel Feed")

app.include_router(
    user.router, 
    prefix="/api/users",
    tags=["Users"],
)

app.include_router(
    scraper.router,
    prefix="/api/scrape",
    tags=["Scrapers"],
)

app.include_router(
    preference.router,
    prefix="/api",
    tags=["Preferences"]
)

app.include_router(
    articles.router,
    prefix="/api",
    tags=["Articles"]
)

@app.get("/")
def root():
    return {"message": "Sentinel Feed API is live"}