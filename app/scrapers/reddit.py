import requests
from datetime import datetime

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