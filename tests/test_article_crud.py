import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.article import Article
from app.crud.article import save_articles

SQL_ALCHEMY_TEST_DATABASE = "sqlite:///:memory:"
engine = create_engine(SQL_ALCHEMY_TEST_DATABASE)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_save_articles(db):
    articles = [
        {
            "title": "Article A",
            "url": "https://example.com/a",
            "summary": "First article",
            "source": "TechCrunch",
            "scraped_at": "2025-07-27T10:00:00"
        },
        {
            "title": "Article A (Duplicate)",
            "url": "https://example.com/a",
            "summary": "Duplicate article",
            "source": "TechCrunch",
            "scraped_at": "2025-07-27T10:05:00"
        },
        {
            "title": "Article B",
            "url": "https://example.com/b",
            "summary": "Second article",
            "source": "TechCrunch",
            "scraped_at": "2025-07-27T10:10:00"
        }
    ]

    save_articles(db, articles)

    all_articles = db.query(Article).all()
    assert len(all_articles) == 2
    urls = [a.url for a in all_articles]
    assert "https://example.com/a" in urls
    assert "https://example.com/b" in urls
       
