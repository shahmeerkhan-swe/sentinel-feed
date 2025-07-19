from app.models.article import Article
from app.database import SessionLocal
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