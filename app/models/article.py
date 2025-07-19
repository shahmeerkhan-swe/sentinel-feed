from app.database import Base
from sqlalchemy import Column, String, DateTime

class Article(Base):
    __tablename__ = "article"
    
    url = Column(String, primary_key=True)
    title = Column(String)
    source = Column(String)
    scraped_at = Column(DateTime)