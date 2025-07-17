from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = "article"
    url = Column(String, primary_key=True)
    title = Column(String)
    source = Column(String)
    scraped_at = Column(DateTime)

engine = create_engine("sqlite:///data/scraped_articles.db")
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

