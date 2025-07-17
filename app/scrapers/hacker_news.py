import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_hacker_news(): 
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    articles = []

    for item in soup.select(".athing"):
        title = item.select_one(".titleline a").text
        link = item.select_one(".titleline a")["href"]
        articles.append({
            "source": "Hacker News",
            "title": title,
            "url": link,
            "scraped_at": datetime.utcnow().isoformat()
        })

    return articles
