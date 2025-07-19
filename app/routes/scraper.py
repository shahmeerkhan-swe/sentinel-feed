from fastapi import APIRouter
from app.core.rss import scrape_hacker_news

router = APIRouter()

@router.get("/scrape/hackernews")
def run_scraper():
    return scrape_hacker_news()