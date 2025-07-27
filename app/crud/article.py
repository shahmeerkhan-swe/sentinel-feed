from app.models.article import Article
from app.database import SessionLocal
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

def save_articles(db: Session, articles):
    for art in articles: 
        try: 
            db.add(Article(
                url=art["url"],
                title=art["title"],
                source=art["source"],
                scraped_at=datetime.fromisoformat(art["scraped_at"])
            ))
            db.commit()
        except IntegrityError: 
            db.rollback()