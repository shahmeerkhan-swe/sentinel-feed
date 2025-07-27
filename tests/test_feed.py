import json
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.models.article import Article
from app.models.preference import UserPreference
from app.auth import deps

from app.database import SessionLocal

# Override current user dependency
def override_get_current_user():
    return User(id=999, email="test@example.com", hashed_password="fakehash")

app.dependency_overrides[deps.get_current_user] = override_get_current_user
client = TestClient(app)

def test_articles_feed():
    db = SessionLocal()

    # Clean up in case rerun
    db.query(Article).delete()
    db.query(UserPreference).delete()
    db.query(User).delete()

    # Setup
    db.add(User(id=999, email="test@example.com", hashed_password="fakehash"))
    db.add(UserPreference(
        user_id=999,
        sources=["Hacker News", "TechCrunch"],
        topics=[],
        frequency=["daily"],
        preferred_time=["09:00"]
    ))
    db.add_all([
        Article(
            title="Feed Article A",
            url="https://feed.example.com/a",
            source="Hacker News",
            scraped_at=datetime.utcnow()
        ),
        Article(
            title="Feed Article B",
            url="https://feed.example.com/b",
            source="TechCrunch",
            scraped_at=datetime.utcnow()
        )
    ])
    db.commit()
    db.close()

    # Act
    response = client.get("/api/feed")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any("feed.example.com/a" in a["url"] for a in data)
    assert any("feed.example.com/b" in a["url"] for a in data)
