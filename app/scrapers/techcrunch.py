import requests 
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_techcrunch():
    url = "https://techcrunch.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    articles = []
    posts = soup.select("a.post-block__title__link")

    for post in posts: 
        title = post.text.strip()
        link = post["href"]
        articles.append({
            "source": "TechCrunch",
            "title": title,
            "url": link,
            "scraped_at": datetime.utcnow().isoformat()
        })

    return articles