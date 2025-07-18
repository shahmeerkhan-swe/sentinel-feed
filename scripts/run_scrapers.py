from app.scrapers.hacker_news import scrape_hacker_news
from app.scrapers.techcrunch import scrape_techcrunch
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

    all_articles = []

    try: 
        all_articles.extend(scrape_hacker_news())
        print("[✓] Hacker News scraped")
    except Exception as e: 
        print(f"[!] Hacker News failed: {e}")

    try: 
        all_articles.extend(scrape_techcrunch())
        print("[✓] TechCrunch scraped")
    except Exception as e: 
        print(f"[!] TechCrunch failed: {e}")

    save_articles(all_articles)
    print(f"[✓] {len(all_articles)} total articles saved.")