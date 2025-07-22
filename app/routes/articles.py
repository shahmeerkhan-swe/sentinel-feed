from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.article import Article
from app.crud.preference import get_preference
from app.schemas.article import ArticleOut

router = APIRouter()

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally: 
        db.close()

@router.get(
    "/feed",
    response_model=List[ArticleOut],
    summary="Get personalized article feed"
)

def get_personalized_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prefs = get_preference(db, current_user.id)
    if not prefs: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not set"
        )
    
    query = db.query(Article)

    if prefs.sources: 
        query = query.filter(Article.source.in_(prefs.sources))

    if prefs.topics: 

        from sqlalchemy import or_
        conditions = [
            Article.title.ilike(f"%{kw}") for kw in prefs.topics
        ]
        query = query.filter(or_(*conditions))

    articles = query.order_by(Article.scraped_at.desc()).all()

    return articles