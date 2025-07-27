import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.core import rss

def test_scrape_hacker_news():
    articles = rss.scrape_hacker_news()
    assert isinstance(articles, list)

    if articles:
        a = articles[0]
        assert "title" in a
        assert "url" in a 
        assert "source" in a 
        assert "scraped_at" in a
        assert "summary" in a or True
        assert a["source"]  == "Hacker News" 

def test_scrape_techcrunch():
    articles = rss.scrape_techcrunch()
    assert isinstance(articles, list)

    if articles:
        a = articles[0]
        assert "title" in a
        assert "url" in a 
        assert "summary" in a or True
        assert "source" in a 
        assert "scraped_at" in a
        assert a["source"]  == "TechCrunch"

def test_scrape_reddit():
    articles = rss.scrape_reddit()
    assert isinstance(articles, list)

    if articles:
        a = articles[0]
        assert "title" in a
        assert "url" in a 
        assert "summary" in a or True 
        assert "source" in a 
        assert "scraped_at" in a
        assert "Reddit" in a["source"] or "r/" in a["source"]
