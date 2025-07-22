from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ArticleOut(BaseModel):
    url: HttpUrl
    title: str
    source: str
    scraped_at: datetime

    class Config:
        from_attributes: True