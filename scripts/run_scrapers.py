from app.scrapers.hacker_news import scrape_hacker_news
from app.core.database import SessionLocal, Article
from datetime import datetime

def save_articles(articles):
    db = SessionLocal()
    for art in articles: 
        if not db.query(Article).filter_by(url=art["url"]).first():
            db.add(Article(
                url=art["url"],
                title=art["title"],
                source=art["source"],
                scraped_at=datetime.fromisoformat(art["scraped_at"])
            ))
    db.commit()
    db.close()

if __name__ == "__main__":
    articles = scrape_hacker_news()
    save_articles(articles)
    print(f"Scraped and saved {len(articles)} articles.")

