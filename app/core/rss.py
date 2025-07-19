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

def scrape_reddit(subreddit="technology", limit=10):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {"User-Agent": "Mozilla/5.0 (sentinel-news-bot)"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    articles = []

    for post in data["data"]["children"]:
        post_data = post["data"]
        articles.append({
            "title": post_data["title"],
            "url": "https://www.reddit.com" + post_data["permalink"],
            "source": f"r/{subreddit}",
            "scraped_at": datetime.utcfromtimestamp(post_data["created_utc"]).isoformat() + "Z"
        })

    return articles