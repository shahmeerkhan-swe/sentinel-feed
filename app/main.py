from fastapi import FastAPI
from app.routes import user, scraper

app = FastAPI()
app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(scraper.router, prefix="/api", tags={"Scrapers"})

@app.get("/")
def root():
    return {"message": "Sentinel Feed API is live"}